"""Futaba-compatible packet codec used by the Vstone VS-S055.

This module is deliberately independent from serial-port libraries so packet
construction and parsing can be tested without hardware.
"""

from __future__ import annotations

import math
from collections.abc import Mapping
from dataclasses import dataclass
from functools import reduce
from operator import xor

SHORT_HEADER = bytes((0xFA, 0xAF))
RETURN_HEADER = bytes((0xFD, 0xDF))

# RAM addresses in the Futaba RS303MR/RS304MD command set.
GOAL_POSITION = 0x1E
GOAL_TIME = 0x20
MAX_TORQUE = 0x23
TORQUE_ENABLE = 0x24
PRESENT_POSITION = 0x2A
PRESENT_TIME = 0x2C
PRESENT_SPEED = 0x2E
PRESENT_CURRENT = 0x30
PRESENT_TEMPERATURE = 0x32
PRESENT_VOLTAGE = 0x34

READ_FLAG = 0x0F
BROADCAST_ID = 0xFF
TELEMETRY_LENGTH = 18

POSITION_UNIT_DEGREES = 0.1
GOAL_POSITION_LIMIT_DEGREES = 150.0


class PacketError(ValueError):
    """Raised when a received packet is malformed or fails its checksum."""


@dataclass(frozen=True)
class ReturnPacket:
    """Decoded return packet."""

    servo_id: int
    flags: int
    address: int
    length: int
    count: int
    data: bytes


@dataclass(frozen=True)
class Telemetry:
    """VS-S055 telemetry converted to SI units where applicable."""

    position: float
    elapsed_s: float
    speed: float
    current_a: float
    temperature_c: int
    input_volts: float


def _validate_byte(name: str, value: int) -> None:
    if not isinstance(value, int) or not 0 <= value <= 0xFF:
        raise ValueError(f"{name} must be an integer in [0, 255]")


def _validate_servo_id(servo_id: int, *, broadcast: bool = False) -> None:
    valid = 1 <= servo_id <= 0x7F or (broadcast and servo_id == BROADCAST_ID)
    if not valid:
        suffix = " or 255 (broadcast)" if broadcast else ""
        raise ValueError(f"servo_id must be in [1, 127]{suffix}")


def xor_checksum(data: bytes) -> int:
    """Return the XOR checksum of *data*."""

    return reduce(xor, data, 0)


def pack_i16_le(value: int) -> bytes:
    """Encode a signed 16-bit integer in little-endian order."""

    if not isinstance(value, int) or not -(2**15) <= value < 2**15:
        raise ValueError("value must fit in a signed 16-bit integer")
    return value.to_bytes(2, byteorder="little", signed=True)


def _unpack_i16_le(data: bytes, offset: int) -> int:
    return int.from_bytes(data[offset : offset + 2], byteorder="little", signed=True)


def _unpack_u16_le(data: bytes, offset: int) -> int:
    return int.from_bytes(data[offset : offset + 2], byteorder="little", signed=False)


def encode_short_packet(
    servo_id: int,
    address: int,
    data: bytes = b"",
    *,
    flags: int = 0,
    count: int = 1,
    length: int | None = None,
) -> bytes:
    """Encode a Futaba short packet.

    ``length`` is inferred from ``data`` for ordinary one-servo writes. Reads
    use ``count=0`` and an explicit requested ``length``.
    """

    _validate_servo_id(servo_id, broadcast=True)
    _validate_byte("flags", flags)
    _validate_byte("address", address)
    _validate_byte("count", count)
    payload = bytes(data)

    if length is None:
        if count != 1:
            raise ValueError("length is required when count is not 1")
        length = len(payload)
    _validate_byte("length", length)
    if len(payload) != length * count:
        raise ValueError("data size must equal length * count")

    body = bytes((servo_id, flags, address, length, count)) + payload
    return SHORT_HEADER + body + bytes((xor_checksum(body),))


def encode_long_packet(address: int, servo_data: Mapping[int, bytes]) -> bytes:
    """Encode one same-address write for multiple servos."""

    _validate_byte("address", address)
    if not servo_data:
        raise ValueError("servo_data must not be empty")
    if len(servo_data) > 0xFF:
        raise ValueError("servo_data cannot contain more than 255 servos")

    records = bytearray()
    record_length: int | None = None
    for servo_id, raw_data in servo_data.items():
        _validate_servo_id(servo_id)
        data = bytes(raw_data)
        if record_length is None:
            record_length = len(data)
            if not 1 <= record_length <= 0xFE:
                raise ValueError("record length must be in [1, 254]")
        elif len(data) != record_length:
            raise ValueError("all servo_data values must have the same length")
        records.append(servo_id)
        records.extend(data)

    assert record_length is not None
    body = bytes((0, 0, address, record_length + 1, len(servo_data))) + records
    return SHORT_HEADER + body + bytes((xor_checksum(body),))


def encode_read_request(servo_id: int, address: int, length: int) -> bytes:
    """Encode an arbitrary-address RAM read request."""

    _validate_servo_id(servo_id)
    if not 1 <= length <= 0xFF:
        raise ValueError("length must be in [1, 255]")
    return encode_short_packet(
        servo_id,
        address,
        flags=READ_FLAG,
        count=0,
        length=length,
    )


def decode_return_packet(packet: bytes) -> ReturnPacket:
    """Validate and decode a complete ``FD DF`` return packet."""

    raw = bytes(packet)
    if len(raw) < 8:
        raise PacketError("return packet is truncated")
    if raw[:2] != RETURN_HEADER:
        raise PacketError("invalid return packet header")

    servo_id, flags, address, length, count = raw[2:7]
    try:
        _validate_servo_id(servo_id)
    except ValueError as exc:
        raise PacketError(str(exc)) from exc
    expected_size = 8 + length * count
    if len(raw) != expected_size:
        raise PacketError(f"return packet size is {len(raw)}, expected {expected_size}")
    if xor_checksum(raw[2:-1]) != raw[-1]:
        raise PacketError("return packet checksum mismatch")
    return ReturnPacket(servo_id, flags, address, length, count, raw[7:-1])


def radians_to_raw_position(position: float) -> int:
    """Convert a goal position in radians to signed 0.1-degree units."""

    degrees = math.degrees(position)
    if not -GOAL_POSITION_LIMIT_DEGREES <= degrees <= GOAL_POSITION_LIMIT_DEGREES:
        raise ValueError("goal position must be in [-150, 150] degrees")
    return round(degrees / POSITION_UNIT_DEGREES)


def raw_position_to_radians(raw_position: int) -> float:
    """Convert signed 0.1-degree position units to radians."""

    if not isinstance(raw_position, int) or not -(2**15) <= raw_position < 2**15:
        raise ValueError("raw_position must fit in a signed 16-bit integer")
    return math.radians(raw_position * POSITION_UNIT_DEGREES)


def decode_telemetry(reply: ReturnPacket) -> Telemetry:
    """Decode telemetry starting at ``PRESENT_POSITION`` into engineering units."""

    if reply.address != PRESENT_POSITION:
        raise PacketError(f"telemetry must start at address 0x{PRESENT_POSITION:02X}")
    if reply.count != 1 or len(reply.data) < 12:
        raise PacketError("telemetry requires one record with at least 12 bytes")

    return Telemetry(
        position=raw_position_to_radians(_unpack_i16_le(reply.data, 0)),
        elapsed_s=_unpack_u16_le(reply.data, 2) * 0.01,
        speed=math.radians(_unpack_i16_le(reply.data, 4)),
        current_a=_unpack_i16_le(reply.data, 6) * 0.001,
        temperature_c=_unpack_i16_le(reply.data, 8),
        input_volts=_unpack_u16_le(reply.data, 10) * 0.01,
    )
