"""Provisional BAM actuator boundary for the Vstone VS-S055."""

from bam.actuator import VoltageControlledActuator
from bam.parameter import Parameter
from bam.testbench import Testbench


class VSS055Actuator(VoltageControlledActuator):
    """Unidentified VS-S055 model prepared for BAM fitting.

    The voltage range is documented by Vstone. Motor and controller parameters
    are deliberately broad optimization seeds, not identified product values.
    """

    def __init__(self, testbench_class: Testbench):
        super().__init__(
            testbench_class,
            vin=7.4,
            kp=1.0,
            error_gain=1.0,
            max_pwm=1.0,
        )

    def initialize(self) -> None:
        self.model.kt = Parameter(0.5, 0.01, 3.0)
        self.model.R = Parameter(5.0, 0.1, 50.0)
        self.model.armature = Parameter(0.0001, 0.00001, 0.04)
        self.model.error_gain_ratio = Parameter(1.0, 0.001, 10.0)

    def compute_control(self, q_target, q, dq, dt):
        duty_cycle = (
            (q_target - q)
            * self.kp
            * self.error_gain
            * self.model.error_gain_ratio.value
        )
        duty_cycle = self.backend.clamp(duty_cycle, -self.max_pwm, self.max_pwm)
        self.duty_cycle = duty_cycle
        return self.vin * duty_cycle

    def get_extra_inertia(self) -> float:
        return self.model.armature.value
