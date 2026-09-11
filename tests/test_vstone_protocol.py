import math
from importlib import import_module

import pytest


def protocol_module():
    return import_module("bam.vstone.protocol")


def test_short_packet_matches_futaba_goal_position_example():
    protocol = protocol_module()

    packet = protocol.encode_short_packet(
        servo_id=1,
        address=protocol.GOAL_POSITION,
        data=protocol.pack_i16_le(900),
    )

    assert packet == bytes.fromhex("FA AF 01 00 1E 02 01 84 03 9B")


def test_long_packet_matches_futaba_multi_servo_example():
    protocol = protocol_module()

    packet = protocol.encode_long_packet(
        address=protocol.GOAL_POSITION,
        servo_data={
            1: protocol.pack_i16_le(100),
            2: protocol.pack_i16_le(100),
            5: protocol.pack_i16_le(500),
        },
    )

    assert packet == bytes.fromhex("FA AF 00 00 1E 03 03 01 64 00 02 64 00 05 F4 01 ED")


def test_read_request_matches_futaba_arbitrary_address_example():
    protocol = protocol_module()

    packet = protocol.encode_read_request(
        servo_id=1,
        address=protocol.PRESENT_POSITION,
        length=2,
    )

    assert packet == bytes.fromhex("FA AF 01 0F 2A 02 00 26")


def test_return_packet_and_telemetry_match_futaba_example():
    protocol = protocol_module()
    packet = bytes.fromhex(
        "FD DF 01 00 2A 12 01 84 03 00 00 00 00 06 00 00 00 00 00 00 00 00 00 00 00 B9"
    )

    reply = protocol.decode_return_packet(packet)
    telemetry = protocol.decode_telemetry(reply)

    assert reply.servo_id == 1
    assert reply.address == protocol.PRESENT_POSITION
    assert telemetry.position == pytest.approx(math.pi / 2)
    assert telemetry.elapsed_s == 0.0
    assert telemetry.speed == 0.0
    assert telemetry.current_a == pytest.approx(0.006)
    assert telemetry.temperature_c == 0
    assert telemetry.input_volts == 0.0


def test_invalid_packets_and_values_are_rejected():
    protocol = protocol_module()

    with pytest.raises(ValueError):
        protocol.encode_short_packet(servo_id=0, address=0, data=b"")
    with pytest.raises(ValueError):
        protocol.radians_to_raw_position(math.radians(151))
    with pytest.raises(protocol.PacketError):
        protocol.decode_return_packet(bytes.fromhex("FD DF 01 00 2A 00 01 00"))
    with pytest.raises(protocol.PacketError):
        protocol.decode_return_packet(bytes.fromhex("FD DF 01"))
    with pytest.raises(protocol.PacketError):
        protocol.decode_return_packet(bytes.fromhex("FD DF 00 00 2A 00 01 2B"))
    with pytest.raises(ValueError):
        protocol.encode_long_packet(address=0, servo_data={1: b""})


def test_position_conversion_uses_signed_tenths_of_a_degree():
    protocol = protocol_module()

    assert protocol.radians_to_raw_position(math.pi / 2) == 900
    assert protocol.radians_to_raw_position(-math.pi / 2) == -900
    assert protocol.raw_position_to_radians(900) == pytest.approx(math.pi / 2)


class FakeSerial:
    def __init__(self, incoming: bytes = b""):
        self.incoming = bytearray(incoming)
        self.writes = []
        self.closed = False

    def write(self, data: bytes) -> int:
        self.writes.append(bytes(data))
        return len(data)

    def read(self, size: int = 1) -> bytes:
        chunk = self.incoming[:size]
        del self.incoming[:size]
        return bytes(chunk)

    def close(self) -> None:
        self.closed = True


def test_bus_construction_has_no_implicit_serial_write():
    from bam.vstone import VstoneBus

    transport = FakeSerial()
    bus = VstoneBus(transport)

    assert transport.writes == []
    bus.set_goal_position(1, math.pi / 2)
    assert transport.writes == [bytes.fromhex("FA AF 01 00 1E 02 01 84 03 9B")]


def test_bus_reads_telemetry_after_leading_echo_bytes():
    from bam.vstone import VstoneBus

    reply = bytes.fromhex(
        "FD DF 01 00 2A 12 01 84 03 00 00 00 00 06 00 00 00 00 00 00 00 00 00 00 00 B9"
    )
    transport = FakeSerial(bytes.fromhex("FA AF 01") + reply)

    telemetry = VstoneBus(transport).request_telemetry(1)

    assert transport.writes == [bytes.fromhex("FA AF 01 0F 2A 12 00 36")]
    assert telemetry.position == pytest.approx(math.pi / 2)
    assert telemetry.current_a == pytest.approx(0.006)


def test_bus_rejects_reply_from_another_servo():
    from bam.vstone import VstoneBus
    from bam.vstone.protocol import PacketError

    reply_from_servo_2 = bytes.fromhex(
        "FD DF 02 00 2A 12 01 84 03 00 00 00 00 06 00 00 00 00 00 00 00 00 00 00 00 BA"
    )

    with pytest.raises(PacketError, match="expected 1"):
        VstoneBus(FakeSerial(reply_from_servo_2)).request_telemetry(1)


@pytest.mark.parametrize(
    ("motor_name", "class_name", "servo_model"),
    [
        ("vstone_vs_s055", "VSS055Actuator", "VS-S055"),
        ("vstone_vs_s055c", "VSS055CActuator", "VS-S055C"),
    ],
)
def test_vstone_models_are_registered_but_have_no_bundled_parameters(
    motor_name, class_name, servo_model
):
    from bam.actuators import actuators
    from bam.model import Model, load_model

    actuator = actuators[motor_name]()
    model = Model()
    model.set_actuator(actuator)

    assert type(actuator).__name__ == class_name
    assert actuator.servo_model == servo_model
    assert actuator.vin == 7.4
    assert model.error_gain_ratio.optimize
    assert actuator.get_extra_inertia() == model.armature.value
    with pytest.raises(FileNotFoundError):
        load_model(motor_name=motor_name, model="m1")
