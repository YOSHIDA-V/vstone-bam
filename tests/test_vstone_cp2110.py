import sys
import tomllib
from collections import deque
from importlib import import_module
from pathlib import Path

import pytest

TELEMETRY_REPLY = bytes.fromhex(
    "FD DF 01 00 2A 12 01 84 03 00 00 00 00 06 00 "
    "00 00 00 00 00 00 00 00 00 00 B9"
)


class FakeRawHidDevice:
    def __init__(
        self,
        *,
        baud=115200,
        uart_enabled=True,
        tx_mode=1,
        transaction_payloads: list[bytes] | None = None,
    ):
        self.baud = baud
        self.uart_enabled = uart_enabled
        self.tx_mode = tx_mode
        self.transaction_payloads = deque(transaction_payloads or [])
        self.reports = deque()
        self.writes = []
        self.feature_writes = []
        self.opened_path = None
        self.nonblocking = None
        self.closed = False

    def open_path(self, path):
        self.opened_path = path

    def set_nonblocking(self, enabled):
        self.nonblocking = enabled

    def get_feature_report(self, report_id, size):
        report = bytearray(size)
        report[0] = report_id
        if report_id == 0x50:
            report[1:5] = self.baud.to_bytes(4, byteorder="big")
            report[5:9] = bytes((0, 0, 3, 0))
        elif report_id == 0x41:
            report[1] = int(self.uart_enabled)
        elif report_id == 0x66:
            report[11] = self.tx_mode
        return bytes(report)

    def send_feature_report(self, report):
        frame = bytes(report)
        self.feature_writes.append(frame)
        if frame == bytes((0x43, 0x02)):
            self.reports.clear()
        return len(frame)

    def write(self, report):
        frame = bytes(report)
        self.writes.append(frame)
        packet_length = frame[0]
        packet = frame[1 : packet_length + 1]
        payload = (
            self.transaction_payloads.popleft()
            if self.transaction_payloads
            else packet + TELEMETRY_REPLY
        )
        self.reports.append(bytes((len(payload),)) + payload)
        return len(frame)

    def read(self, _size):
        return self.reports.popleft() if self.reports else b""

    def close(self):
        self.closed = True


class FakeHidModule:
    def __init__(
        self,
        raw_device,
        *,
        device_infos: list[dict] | None = None,
    ):
        self.raw_device = raw_device
        self.device_infos = device_infos or [
            {"path": b"fake-cp2110", "serial_number": "CP2110-A"}
        ]
        self.enumerate_args = None

    def enumerate(self, vendor_id, product_id):
        self.enumerate_args = (vendor_id, product_id)
        return self.device_infos

    def device(self):
        return self.raw_device


def test_cp2110_transport_contract_is_available():
    cp2110_transport = import_module("bam.vstone.cp2110")
    vstone = import_module("bam.vstone")

    assert hasattr(cp2110_transport, "Cp2110Transport")
    assert hasattr(vstone.VstoneBus, "open_cp2110")

    project = tomllib.loads(
        (Path(__file__).parents[1] / "pyproject.toml").read_text(encoding="utf-8")
    )
    assert "hidapi==0.15.0" in project["project"]["optional-dependencies"][
        "identification"
    ]


def test_cp2110_module_does_not_load_optional_driver_on_import():
    sys.modules.pop("hid", None)

    import_module("bam.vstone.cp2110")

    assert "hid" not in sys.modules


def test_cp2110_transport_matches_verified_position_read_path():
    from bam.vstone import VstoneBus

    raw_device = FakeRawHidDevice()
    module = FakeHidModule(raw_device)

    bus = VstoneBus.open_cp2110(
        baudrate=115200,
        timeout=0.01,
        hid_module=module,
    )
    telemetry = bus.request_telemetry(1)

    request = bytes.fromhex("FA AF 01 0F 2A 12 00 36")
    assert raw_device.writes == [bytes((len(request),)) + request]
    assert raw_device.feature_writes == [bytes((0x43, 0x02))]
    assert raw_device.opened_path == b"fake-cp2110"
    assert raw_device.nonblocking == 1
    assert module.enumerate_args == (0x10C4, 0xEA80)
    assert telemetry.position == pytest.approx(3.141592653589793 / 2)
    assert telemetry.current_a == pytest.approx(0.006)


def test_cp2110_transport_rejects_non_open_drain_without_mutation():
    from bam.vstone.cp2110 import Cp2110Transport

    raw_device = FakeRawHidDevice(tx_mode=0)
    module = FakeHidModule(raw_device)

    with pytest.raises(RuntimeError, match="open-drain"):
        Cp2110Transport.open(
            baudrate=115200,
            timeout=0.01,
            hid_module=module,
        )

    assert raw_device.feature_writes == []
    assert raw_device.writes == []
    assert raw_device.closed


@pytest.mark.parametrize(
    ("baud", "uart_enabled", "message"),
    [
        (57600, True, "UART configuration"),
        (115200, False, "already be enabled"),
    ],
)
def test_cp2110_transport_rejects_unverified_uart_state(
    baud,
    uart_enabled,
    message,
):
    from bam.vstone.cp2110 import Cp2110Transport

    raw_device = FakeRawHidDevice(
        baud=baud,
        uart_enabled=uart_enabled,
    )
    module = FakeHidModule(raw_device)

    with pytest.raises(RuntimeError, match=message):
        Cp2110Transport.open(
            baudrate=115200,
            timeout=0.01,
            hid_module=module,
        )

    assert raw_device.feature_writes == []
    assert raw_device.writes == []
    assert raw_device.closed


def test_cp2110_transport_requires_serial_for_multiple_adapters():
    from bam.vstone.cp2110 import Cp2110Transport

    raw_device = FakeRawHidDevice()
    module = FakeHidModule(
        raw_device,
        device_infos=[
            {"path": b"cp2110-a", "serial_number": "A"},
            {"path": b"cp2110-b", "serial_number": "B"},
        ],
    )

    with pytest.raises(RuntimeError, match="specify serial_number"):
        Cp2110Transport.open(
            baudrate=115200,
            timeout=0.01,
            hid_module=module,
        )

    transport = Cp2110Transport.open(
        baudrate=115200,
        timeout=0.01,
        serial_number="B",
        hid_module=module,
    )
    assert raw_device.opened_path == b"cp2110-b"
    transport.close()


def test_cp2110_transport_retries_after_local_echo_mismatch():
    from bam.vstone import VstoneBus

    request = bytes.fromhex("FA AF 01 0F 2A 12 00 36")
    bad_echo = bytes((request[0] ^ 0x01,)) + request[1:]
    raw_device = FakeRawHidDevice(
        transaction_payloads=[
            bad_echo + TELEMETRY_REPLY,
            request + TELEMETRY_REPLY,
        ]
    )
    module = FakeHidModule(raw_device)
    bus = VstoneBus.open_cp2110(
        baudrate=115200,
        timeout=0.01,
        read_attempts=2,
        hid_module=module,
    )

    telemetry = bus.request_telemetry(1)

    assert len(raw_device.writes) == 2
    assert raw_device.feature_writes == [
        bytes((0x43, 0x02)),
        bytes((0x43, 0x02)),
    ]
    assert telemetry.position == pytest.approx(3.141592653589793 / 2)


def test_cp2110_transport_rejects_payload_over_hid_limit():
    from bam.vstone.cp2110 import Cp2110Transport

    raw_device = FakeRawHidDevice()
    module = FakeHidModule(raw_device)
    transport = Cp2110Transport.open(
        baudrate=115200,
        timeout=0.01,
        hid_module=module,
    )

    with pytest.raises(ValueError, match="63"):
        transport.write(bytes(64))

    assert raw_device.writes == []
