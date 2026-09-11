"""Explicit serial bus operations for the Vstone VS-S055."""

from __future__ import annotations

from typing import Any, Protocol, Self

from .protocol import (
    GOAL_POSITION,
    PRESENT_POSITION,
    RETURN_HEADER,
    TELEMETRY_LENGTH,
    TORQUE_ENABLE,
    PacketError,
    ReturnPacket,
    Telemetry,
    decode_return_packet,
    decode_telemetry,
    encode_read_request,
    encode_short_packet,
    pack_i16_le,
    radians_to_raw_position,
)


class SerialLike(Protocol):
    """Small transport surface required by :class:`VstoneBus`."""

    def write(self, data: bytes) -> int | None: ...

    def read(self, size: int = 1) -> bytes: ...

    def close(self) -> None: ...


class VstoneBus:
    """VS-S055 bus with no implicit torque or motion command.

    Constructing this object around an existing transport has no side effects.
    Use :meth:`open` when a real serial port should be opened explicitly.
    """

    def __init__(self, transport: SerialLike, *, read_attempts: int = 1):
        if not isinstance(read_attempts, int) or read_attempts < 1:
            raise ValueError("read_attempts must be a positive integer")
        self.transport = transport
        self.read_attempts = read_attempts

    @classmethod
    def open(
        cls,
        port: str,
        *,
        baudrate: int,
        timeout: float = 0.1,
        read_attempts: int = 1,
    ) -> Self:
        """Open pyserial without changing servo ROM or assuming its baud rate."""

        try:
            import serial
        except ImportError as exc:
            raise RuntimeError(
                "pyserial is required for hardware access; install the "
                "'identification' extra"
            ) from exc
        return cls(
            serial.Serial(port=port, baudrate=baudrate, timeout=timeout),
            read_attempts=read_attempts,
        )

    @classmethod
    def open_cp2110(
        cls,
        *,
        baudrate: int,
        timeout: float = 0.1,
        read_attempts: int = 8,
        serial_number: str | None = None,
        hid_module: Any | None = None,
    ) -> Self:
        """Open the Windows-native CP2110 open-drain transport explicitly."""

        from .cp2110 import Cp2110Transport

        transport = Cp2110Transport.open(
            baudrate=baudrate,
            timeout=timeout,
            serial_number=serial_number,
            hid_module=hid_module,
        )
        return cls(transport, read_attempts=read_attempts)

    def close(self) -> None:
        self.transport.close()

    def _write(self, packet: bytes) -> None:
        written = self.transport.write(packet)
        if written is not None and written != len(packet):
            raise OSError(f"serial transport wrote {written} of {len(packet)} bytes")

    def _read_exact(self, size: int) -> bytes:
        data = bytearray()
        while len(data) < size:
            chunk = self.transport.read(size - len(data))
            if not chunk:
                raise TimeoutError(f"serial read timed out after {len(data)} bytes")
            data.extend(chunk)
        return bytes(data)

    def read_return_packet(self) -> ReturnPacket:
        """Read one return packet, ignoring bytes before the ``FD DF`` header."""

        previous = None
        while True:
            value = self._read_exact(1)[0]
            if previous == RETURN_HEADER[0] and value == RETURN_HEADER[1]:
                break
            previous = value

        metadata = self._read_exact(5)
        payload_size = metadata[3] * metadata[4]
        packet = RETURN_HEADER + metadata + self._read_exact(payload_size + 1)
        return decode_return_packet(packet)

    def set_goal_position(self, servo_id: int, position: float) -> None:
        """Send a goal position; this method does not enable torque."""

        raw_position = radians_to_raw_position(position)
        self._write(
            encode_short_packet(
                servo_id,
                GOAL_POSITION,
                pack_i16_le(raw_position),
            )
        )

    def set_torque(self, servo_id: int, enabled: bool) -> None:
        """Explicitly enable or disable servo torque."""

        self._write(
            encode_short_packet(
                servo_id,
                TORQUE_ENABLE,
                bytes((1 if enabled else 0,)),
            )
        )

    def request_telemetry(self, servo_id: int) -> Telemetry:
        """Request and decode the contiguous telemetry block."""

        for attempt in range(self.read_attempts):
            try:
                self._write(
                    encode_read_request(
                        servo_id,
                        PRESENT_POSITION,
                        TELEMETRY_LENGTH,
                    )
                )
                reply = self.read_return_packet()
                if reply.servo_id != servo_id:
                    raise PacketError(
                        f"received servo ID {reply.servo_id}, expected {servo_id}"
                    )
                return decode_telemetry(reply)
            except (OSError, RuntimeError, TimeoutError, PacketError):
                if attempt + 1 >= self.read_attempts:
                    raise
                recover = getattr(self.transport, "recover", None)
                if not callable(recover):
                    raise
                recover()

        raise AssertionError("unreachable")
