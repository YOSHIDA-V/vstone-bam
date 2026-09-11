# VSTONE-BAM-PROTOCOL-001

- State: `OBSERVED`
- Observed behavior: Rhoban/bam has no `bam.vstone` communication package and
  cannot encode or decode the Futaba-compatible TTL packets specified for the
  Vstone VS-S055.
- Failure run ID: `VSTONE-BAM-PROTOCOL-001-OBSERVED-20260911`
- Execution target: `offline_protocol_codec_only`
- Base commit: `620a64fe67c1afe94fca81da73b128c7aed17c5f`
- Runtime hashes: not applicable before the first controlled test run
- Reproduction values:
  - `import bam.vstone.protocol` fails on the base commit.
  - No `vstone` key exists in `bam/actuators.py`.
  - The base tree has no encoder for `FA AF` short/long packets or decoder for
    `FD DF` return packets.
- Root-cause hypothesis: Vstone is a new manufacturer integration. The generic
  BAM model and fitting code are present, but the manufacturer-specific
  transport boundary is absent.
- Values that would prove the cause:
  - A base-commit import failure for `bam.vstone.protocol`.
  - Exact byte comparison against the RS303MR/RS304MD manual examples.
- Files allowed to change:
  - `bam/vstone/**`
  - `bam/actuators.py`
  - `pyproject.toml`
  - `tests/test_vstone_protocol.py`
  - `docs/identification/acquisition.rst`
  - `docs/usage/actuators.rst`
  - `README.md`
  - this Issue contract and evidence for this Issue
- Files forbidden to change:
  - Existing manufacturer drivers
  - BAM friction equations and fitting algorithms
  - Bundled identified parameter files
  - Robovie-Z workspace code and configuration
  - Servo ROM values, IDs, baud-rate settings, or physical hardware state
- Controlled-environment pass criteria:
  - Short, long, read-request, and return-packet tests match the published
    Futaba examples byte-for-byte.
  - Invalid checksum, truncated frame, invalid ID, and out-of-range angle are
    rejected.
  - Position, speed, current, temperature, and voltage conversions are tested.
  - The full upstream test suite and Ruff checks pass without hardware access.
- Target pass criteria:
  - A user-approved single VS-S055 test bench returns a valid `FD DF` telemetry
    packet for the same immutable candidate.
  - Position and voltage agree with independently observed bench values under
    user-supplied tolerances.
  - Torque enable/disable and motion tests require a separate explicit physical
    command authorization; they are not authorized by this Issue contract.
- Previously verified behavior that must not regress:
  - Existing Dynamixel, Feetech, eRob, Waveshare, and Unitree model loading.
  - Installation without the `identification` extra must not import the serial
    dependency.

## Sources and claim boundary

Vstone documents the VS-S055 as a serial-only, TTL half-duplex servo using a
Futaba-compatible command set, with a maximum communication rate of 230.4 kbps.
The detailed frame and memory-map values used by the offline tests come from
the Futaba RS303MR/RS304MD user manual version 1.19. Compatibility with the
actual VS-S055 remains unverified until the target criteria above are met.

