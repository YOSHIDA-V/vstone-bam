# VSTONE-BAM-CP2110-002 reproduced

- Timestamp UTC: `2026-09-11T04:18:04.7884747Z`
- Branch: `codex/vstone-cp2110-transport`
- Base commit: `d090afe6e6d94d09c9480c215dbcdb494e8e1228`
- Run ID: `VSTONE-BAM-CP2110-002-REPRO-20260911`
- Target: `controlled_fake_cp2110_only`
- Command: `uv run --with pytest pytest -q tests/test_vstone_cp2110.py`
- Exit code: `1`
- Result: `1 failed`
- Failure:
  `ModuleNotFoundError: No module named 'bam.vstone.cp2110'`
- Structural search result: `bam/vstone/bus.py` contains the only concrete
  Vstone transport construction, `serial.Serial`; no `cp2110` or
  `open_cp2110` implementation exists.
- Physical hardware access: not performed
- Servo command transmission: not performed

This run reproduces only the missing CP2110 transport boundary. It does not
qualify a physical adapter or any torque or position command.
