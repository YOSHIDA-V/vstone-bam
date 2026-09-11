# VSTONE-BAM-PROTOCOL-001 controlled run

- Status: `PASSED`
- Timestamp UTC: `2026-09-11T03:15:40.2656796Z`
- Run ID: `VSTONE-BAM-PROTOCOL-001-CONTROLLED-20260911`
- Execution target: `offline_protocol_codec_only`
- Implementation commit: `d973adbf7088b6e2944601a8d82a1d8974c85250`
- Execution commit: `cbd4adb28132b032c9823686640c6740d445fd87`
- Python: `3.12.13`
- uv: `0.11.15`
- Test SHA-256:
  `92EE2CBEE30CCF317838F20B1D4DE1BDB93A122C05DD746998DFAE93732671B6`
- Protocol SHA-256:
  `9B7436420C485B857ADFBDC55F9BFB76A545C791E7DDD43DF3AF84B956E0BC3D`
- Bus SHA-256:
  `744C9819972DF5E01FEDD7D7F8941BA45F20A42F437B8706E195724CDAF566FE`
- Futaba manual SHA-256:
  `E483B96F7D9865FE8F25CC2EC9C9AFB22B68CB1F25D2E2ABA5BDBF848BE0E04D`
- Planned commands:
  - `uv run --with pytest pytest -q`
  - `uvx ruff check bam/vstone bam/actuators.py tests/test_vstone_protocol.py`
  - `uvx ruff format --check bam/vstone bam/actuators.py tests/test_vstone_protocol.py`
  - `uv run python -m compileall -q bam/vstone`
  - `uv build`
  - isolated wheel import with no `serial` module import
- Results:
  - pytest: exit `0`; `10 passed in 0.46s`
  - changed-scope Ruff check: exit `0`; all checks passed
  - changed-scope Ruff format check: exit `0`; six files already formatted
  - compileall: exit `0`
  - build: exit `0`; sdist and wheel built
  - isolated wheel import: exit `0`; Vstone registry present and
    `SERIAL_IMPORT=absent`
  - worktree during run: clean
- Artifact hashes:
  - wheel:
    `A15F2436F16A163D275625C6A3E5DE769A8788EB7458B3DB26525317F787A1D6`
  - sdist:
    `49422C71BE142349C69228E46E8981B31BCEA6E33BC2F8A95B78258F128DA419`
- Repository-wide non-regression checks:
  - candidate Ruff: 104 pre-existing-style findings
  - upstream `620a64fe67c1afe94fca81da73b128c7aed17c5f` Ruff: 105 findings
  - Sphinx HTML: exit `0`; 19 warnings remain in the upstream documentation
- Claim boundary: offline protocol and packaging are verified. A physical
  VS-S055, its configured baud rate, telemetry semantics, torque, and motion
  remain unverified.
- Physical device access: not performed
- Servo command transmission: not performed
