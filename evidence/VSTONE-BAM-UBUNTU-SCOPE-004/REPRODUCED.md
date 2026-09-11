# Native-Ubuntu scope mismatch evidence

- Run ID: `VSTONE-BAM-UBUNTU-SCOPE-004-REPRO-20260911`
- Runtime: Windows host used only for the source-contract reproduction; no WSL
- Executed source commit: `8d2289ce8ea7adcceacd078c45b3ad809810202c`
- Execution target: source declarations, not Ubuntu runtime qualification
- Command: `uv run --with pytest pytest -q
  tests/test_vstone_platform_scope.py`
- Result: `1 failed`
- Failure: the identification extra contains a direct dependency beginning
  with `PyQt5-Qt5`.
- Additional source observations:
  - `bam/vstone/cp2110.py` contains `Windows-native`.
  - `bam/vstone/bus.py` contains `Windows-native`.
  - acquisition documentation contains native-Windows instructions.
- Physical hardware access: none
