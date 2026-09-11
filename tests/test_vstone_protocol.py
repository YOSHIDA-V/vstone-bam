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

    assert packet == bytes.fromhex(
        "FA AF 00 00 1E 03 03 01 64 00 02 64 00 05 F4 01 ED"
    )


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
        "FD DF 01 00 2A 12 01 "
        "84 03 00 00 00 00 06 00 00 00 00 00 00 00 00 00 00 00 B9"
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


def test_position_conversion_uses_signed_tenths_of_a_degree():
    protocol = protocol_module()

    assert protocol.radians_to_raw_position(math.pi / 2) == 900
    assert protocol.radians_to_raw_position(-math.pi / 2) == -900
    assert protocol.raw_position_to_radians(900) == pytest.approx(math.pi / 2)
