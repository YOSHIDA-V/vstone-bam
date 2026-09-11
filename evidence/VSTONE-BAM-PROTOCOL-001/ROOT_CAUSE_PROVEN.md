# VSTONE-BAM-PROTOCOL-001 root-cause evidence

- Timestamp UTC: `2026-09-11T03:07:30.5517030Z`
- Reproduction commit: `5e19110d0a0276176aa391a8d3c91581a990d132`
- Remote branch: `origin/codex/vstone-protocol`
- Remote commit: `5e19110d0a0276176aa391a8d3c91581a990d132`
- Repository search:
  - `VSTONE_FILE_COUNT=0`
  - `VSTONE_SOURCE_MATCH_COUNT=0`
- Existing manufacturer boundaries inspected:
  - `bam/dynamixel/actuator.py`
  - `bam/dynamixel/dynamixel.py`
  - `bam/feetech/actuator.py`
  - `bam/actuators.py`
- Proven cause: the upstream tree has no Vstone manufacturer package or
  registry entry. The failure is not caused by the generic actuator model or
  fitting implementation.
- Physical device access: not performed
- Servo command transmission: not performed

This evidence proves the cause of the offline import and packet-codec failure.
It does not prove protocol compatibility with a physical VS-S055.
