# Controlled CP2110 transport evidence

- Run ID: `VSTONE-BAM-CP2110-002-CONTROLLED-20260911-WINDOWS`
- Runtime: native Windows, CPython 3.12, no WSL
- Hardware target: `controlled_fake_cp2110_only`
- Physical commands: none
- Result: `uv run --with pytest pytest -q` -> `19 passed`
- Result: `uv run --with ruff ruff check bam/vstone
  tests/test_vstone_cp2110.py` -> `All checks passed!`
- Result: `uv run --with hidapi==0.15.0 python ...` -> loaded
  `hid.cp312-win_amd64.pyd` and imported `Cp2110Transport`
- Result: `uv build` -> source distribution and wheel built successfully
- Wheel SHA-256:
  `56F58060FA29D6A2295EB556C3AB58FE878CBD9F70470A012B4E208B3367C486`
- Wheel inspection:
  - contains `bam/vstone/cp2110.py`
  - contains `Requires-Dist: hidapi==0.15.0; extra == "identification"`
- Scope limit: no CP2110 or VS-S055 was opened. Windows physical telemetry is
  not verified by this run.
