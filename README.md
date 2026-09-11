<p align="center">
  <img src="docs/_static/BAM_logo.png" alt="BAM logo" width="60%">
</p>

# Vstone-BAM

This repository is a fork of [Rhoban/BAM](https://github.com/Rhoban/bam) that
adds Vstone manufacturer boundaries for the VS-S055 and VS-S055C servos while
preserving the upstream model and fitting pipeline.

Current Vstone support includes a hardware-independent Futaba-compatible packet
codec, an explicit serial bus API, and the unparameterized `vstone_vs_s055` and
`vstone_vs_s055c` actuator entries used by BAM fitting. No identified VS-S055 or
VS-S055C friction parameters are bundled yet. The protocol implementation
remains scoped to VS-S055; VS-S055C communication compatibility has not been
verified. Importing the package does not open a serial port, enable torque, or
send a goal position.

Protocol references:

- [Vstone VS-S055 product specifications](https://www.vstone.co.jp/products/vs_s055/index.html)
- [Futaba RS303MR/RS304MD command manual](https://www.rc.futaba.co.jp/downloads/shop/WCI00000307N2511071447xdvub.pdf?mode=view)

Manufacturer-published VS-S055 product data:

| Item | VS-S055 (normal cable) |
| --- | --- |
| Listed price | JPY 4,000 before tax |
| Dimensions | 19.6 (W) × 35.8 (D) × 25.0 (H) mm |
| Mass | Approximately 19.6 g |
| Servo output torque | 5.5 kgf·cm at 7.2 V |
| Operating speed | 0.16 s/60° at 7.4 V |
| Motion range | 300° |
| Supply voltage | 4.8–7.4 V |
| Control methods listed by Vstone | TTL command and PWM |
| Serial interface | Up to 230.4 kbps, TTL half-duplex, Futaba serial command compatible |
| Sensor information | Angle, torque, temperature |
| Calibration | 31 points |
| Package contents | Servo, horn, horn screw, ADH servo connector (200 mm) |

The same values are available as immutable reference metadata through
`bam.vstone.VS_S055_SPECIFICATION`. They are not identified BAM values for
`kt`, winding resistance, controller gain, armature inertia, or friction. The
current `VstoneBus` implements only the TTL serial command path; listing PWM in
the product table does not mean that this package implements a PWM transport.
Equivalent numerical specifications have not been assigned to VS-S055C because
a standalone manufacturer specification has not been confirmed.

The protocol implementation and its evidence are tracked in
[`VSTONE-BAM-PROTOCOL-001`](docs/issues/VSTONE-BAM-PROTOCOL-001.md).

## Upstream BAM

Accurate models of servo actuators are essential for the simulation of robotic systems. It is particularly important while performing Reinforcement Learning (RL) on real robots, as the precision of the model impacts directly the transferability of the learned policy.

The friction model generally implemented in widely used simulators like MuJoCo or IsaacGym is the Coulomb-Viscous, which is too simplistic to accurately represent complex friction phenomena like Stribeck, load-dependence or quadratic effects (read [this article](https://arxiv.org/pdf/2410.08650v1) for more details).

**BAM** aims at making servo-actuator simulation more faithful by:

- proposing an identification pipeline to fit friction models from recorded trajectories,
- providing a set of extended friction models that capture complex friction phenomena,
- sharing a library of identified models for common servos:
  - Dynamixel MX-64
  - Dynamixel MX-106
  - Dynamixel XL-320
  - Dynamixel XL330-M288-T
  - eRob80:50
  - eRob80:100
  - Feetech STS3215
- providing a simple API to use these models in MuJoCo CPU and MuJoCo Warp.

## 📖 Documentation

Please refer to the [documentation](https://bam.readthedocs.io/en/latest/) for more details on how to use BAM and the provided friction models.

## 📚 Citation

If you use BAM or the friction models provided in this repository for your scientific work, please cite the following publication:

```bibtex
@inproceedings{duclusaud2025extended,
  title={Extended Friction Models for the Physics Simulation of Servo Actuators},
  author={Duclusaud, Marc and Passault, Gr{\'e}goire and Padois, Vincent and Ly, Olivier},
  booktitle={2025 IEEE International Conference on Robotics and Automation (ICRA)},
  pages={12091--12097},
  year={2025},
  organization={IEEE}
}
```

If you also wish to cite the software directly, you may use:

```bibtex
@software{BAM,
  title = {{BAM: Better Actuator Models}},
  author = {Duclusaud, Marc and Passault, Grégoire},
  license = {Apache-2.0},
  url = {https://github.com/Rhoban/bam},
  version = {0.0.1},
  year = {2024}
}
```
