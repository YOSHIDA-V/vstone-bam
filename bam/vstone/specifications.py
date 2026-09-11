"""Manufacturer-published product specifications for Vstone servos.

These values are reference metadata. They are not BAM-identified electrical,
controller, inertia, or friction parameters and must not be used as substitutes
for physical identification.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class VstoneServoSpecification:
    """Published product data kept separate from BAM model parameters."""

    model_name: str
    cable_type: str
    listed_price_jpy_before_tax: int
    dimensions_mm: tuple[float, float, float]
    mass_g: float
    output_torque_kgf_cm: float
    output_torque_voltage_v: float
    speed_s_per_60_deg: float
    speed_voltage_v: float
    motion_range_deg: float
    supply_voltage_range_v: tuple[float, float]
    listed_control_methods: tuple[str, ...]
    max_baudrate_bps: int
    serial_electrical_interface: str
    serial_command_compatibility: str
    sensor_information: tuple[str, ...]
    calibration_points: int
    package_contents: tuple[str, ...]
    source_url: str


VS_S055_SPECIFICATION = VstoneServoSpecification(
    model_name="VS-S055",
    cable_type="normal cable",
    listed_price_jpy_before_tax=4_000,
    dimensions_mm=(19.6, 35.8, 25.0),
    mass_g=19.6,
    output_torque_kgf_cm=5.5,
    output_torque_voltage_v=7.2,
    speed_s_per_60_deg=0.16,
    speed_voltage_v=7.4,
    motion_range_deg=300.0,
    supply_voltage_range_v=(4.8, 7.4),
    listed_control_methods=("TTL command", "PWM"),
    max_baudrate_bps=230_400,
    serial_electrical_interface="TTL half-duplex",
    serial_command_compatibility="Futaba serial command compatible",
    sensor_information=("angle", "torque", "temperature"),
    calibration_points=31,
    package_contents=(
        "servo",
        "servo horn",
        "servo horn screw",
        "ADH servo connector (200 mm)",
    ),
    source_url="https://www.vstone.co.jp/products/vs_s055/index.html",
)
