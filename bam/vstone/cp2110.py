"""Windows-native CP2110 HID transport for the Vstone/Futaba TTL bus."""

from __future__ import annotations

import importlib
import math
import time
from typing import Any, Self

CP2110_VENDOR_ID = 0x10C4
CP2110_PRODUCT_ID = 0xEA80
UART_ENABLE_REPORT_ID = 0x41
UART_ENABLE_REPORT_SIZE = 2
PURGE_FIFOS_REPORT_ID = 0x43
PURGE_BOTH_FIFOS = 0x02
UART_CONFIG_REPORT_ID = 0x50
UART_CONFIG_REPORT_SIZE = 9
PARITY_NONE = 0x00
FLOW_CONTROL_DISABLED = 0x00
DATA_BITS_EIGHT = 0x03
STOP_BITS_SHORT = 0x00
PIN_CONFIG_REPORT_ID = 0x66
PIN_CONFIG_REPORT_SIZE = 20
PIN_CONFIG_TX_INDEX = 11
TX_OPEN_DRAIN = 0x01
UART_PAYLOAD_MAX = 63


def _load_hid_module() -> Any:
    try:
        return importlib.import_module("hid")
    except ModuleNotFoundError as exc:
        raise RuntimeError(
            "hidapi is required for CP2110 access; install the "
            "'identification' extra"
        ) from exc


def _read_feature_report(device: Any, report_id: int, size: int) -> bytes:
    report = bytes(device.get_feature_report(report_id, size))
    if len(report) != size or report[0] != report_id:
        raise RuntimeError(
            "invalid CP2110 feature report: "
            f"id=0x{report_id:02x}, length={len(report)}, report={report.hex()}"
        )
    return report


def _purge_fifos(device: Any) -> None:
    report = bytes((PURGE_FIFOS_REPORT_ID, PURGE_BOTH_FIFOS))
    written = device.send_feature_report(report)
    if written != len(report):
        raise OSError(
            "short CP2110 FIFO-purge report: "
            f"expected={len(report)}, written={written}"
        )


def _select_device(
    hid_module: Any,
    *,
    serial_number: str | None,
) -> dict[str, Any]:
    devices = list(
        hid_module.enumerate(CP2110_VENDOR_ID, CP2110_PRODUCT_ID) or []
    )
    if serial_number is not None:
        devices = [
            device
            for device in devices
            if device.get("serial_number") == serial_number
        ]

    if not devices:
        suffix = (
            f" with serial number {serial_number!r}"
            if serial_number is not None
            else ""
        )
        raise RuntimeError(f"CP2110 10c4:ea80{suffix} was not found")
    if len(devices) > 1:
        raise RuntimeError(
            "multiple CP2110 devices were found; specify serial_number"
        )

    device_info = devices[0]
    if not device_info.get("path"):
        raise RuntimeError("CP2110 HID enumeration returned no device path")
    return device_info


class Cp2110Transport:
    """Serial-like adapter over CP2110 HID UART reports.

    Opening validates the adapter's existing state and purges its FIFOs. It
    never enables UART or writes UART/pin configuration. Each write consumes
    and validates the local echo before returning, matching the previously used
    dual-arm VS-S055 acquisition path.
    """

    def __init__(self, device: Any, *, timeout: float) -> None:
        if not math.isfinite(timeout) or timeout <= 0.0:
            raise ValueError("CP2110 timeout must be positive and finite")
        self.device = device
        self.timeout = timeout
        self.pending = bytearray()
        self.closed = False

    @classmethod
    def open(
        cls,
        *,
        baudrate: int,
        timeout: float = 0.1,
        serial_number: str | None = None,
        hid_module: Any | None = None,
    ) -> Self:
        """Open one already configured CP2110 without changing UART state."""

        if not isinstance(baudrate, int) or baudrate <= 0:
            raise ValueError("baudrate must be a positive integer")
        if not math.isfinite(timeout) or timeout <= 0.0:
            raise ValueError("CP2110 timeout must be positive and finite")
        if serial_number is not None and not serial_number:
            raise ValueError("serial_number must not be empty")

        hid = hid_module or _load_hid_module()
        device_info = _select_device(hid, serial_number=serial_number)
        device = hid.device()
        try:
            device.open_path(device_info["path"])
            device.set_nonblocking(1)

            config = _read_feature_report(
                device,
                UART_CONFIG_REPORT_ID,
                UART_CONFIG_REPORT_SIZE,
            )
            actual_baudrate = int.from_bytes(config[1:5], byteorder="big")
            if (
                actual_baudrate != baudrate
                or config[5] != PARITY_NONE
                or config[6] != FLOW_CONTROL_DISABLED
                or config[7] != DATA_BITS_EIGHT
                or config[8] != STOP_BITS_SHORT
            ):
                raise RuntimeError(
                    "unexpected CP2110 UART configuration; refusing to communicate"
                )

            uart_enabled = _read_feature_report(
                device,
                UART_ENABLE_REPORT_ID,
                UART_ENABLE_REPORT_SIZE,
            )
            if uart_enabled[1] != 1:
                raise RuntimeError("CP2110 UART must already be enabled")

            pin_config = _read_feature_report(
                device,
                PIN_CONFIG_REPORT_ID,
                PIN_CONFIG_REPORT_SIZE,
            )
            if pin_config[PIN_CONFIG_TX_INDEX] != TX_OPEN_DRAIN:
                raise RuntimeError("CP2110 TX must already be open-drain")

            _purge_fifos(device)
            return cls(device, timeout=timeout)
        except Exception:
            device.close()
            raise

    def _require_open(self) -> None:
        if self.closed:
            raise RuntimeError("CP2110 transport is closed")

    def _read_exact(self, size: int) -> bytes:
        deadline = time.monotonic() + self.timeout
        while len(self.pending) < size and time.monotonic() < deadline:
            report = bytes(self.device.read(64))
            if not report:
                time.sleep(0.001)
                continue

            count = report[0]
            if count == 0:
                continue
            if count > UART_PAYLOAD_MAX or len(report) < count + 1:
                raise RuntimeError(
                    f"invalid CP2110 report: count={count}, report_len={len(report)}"
                )
            self.pending.extend(report[1 : count + 1])

        if len(self.pending) < size:
            raise TimeoutError(
                f"CP2110 UART timeout: expected={size}, received={len(self.pending)}"
            )

        result = bytes(self.pending[:size])
        del self.pending[:size]
        return result

    def write(self, data: bytes) -> int:
        """Write one UART payload and consume its exact local echo."""

        self._require_open()
        packet = bytes(data)
        if not packet or len(packet) > UART_PAYLOAD_MAX:
            raise ValueError(
                f"CP2110 UART packet length must be in [1, {UART_PAYLOAD_MAX}]"
            )

        report = bytes((len(packet),)) + packet
        written = self.device.write(report)
        if written != len(report):
            raise OSError(
                f"short CP2110 HID write: expected={len(report)}, written={written}"
            )

        echo = self._read_exact(len(packet))
        if echo != packet:
            raise RuntimeError(
                f"CP2110 local echo mismatch: tx={packet.hex()} rx={echo.hex()}"
            )
        return len(packet)

    def read(self, size: int = 1) -> bytes:
        """Read exactly *size* UART bytes from length-prefixed HID reports."""

        self._require_open()
        if not isinstance(size, int) or size < 0:
            raise ValueError("read size must be a non-negative integer")
        if size == 0:
            return b""
        return self._read_exact(size)

    def recover(self) -> None:
        """Discard partial data and purge both CP2110 FIFOs before a retry."""

        self._require_open()
        self.pending.clear()
        _purge_fifos(self.device)

    def close(self) -> None:
        if self.closed:
            return
        self.closed = True
        self.pending.clear()
        self.device.close()
