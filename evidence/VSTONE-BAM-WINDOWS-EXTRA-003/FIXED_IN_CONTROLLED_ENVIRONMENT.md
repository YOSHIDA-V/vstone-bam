# Windows identification-extra controlled evidence

- Run ID: `VSTONE-BAM-WINDOWS-EXTRA-003-CONTROLLED-20260911`
- Runtime: native Windows `win_amd64`, CPython 3.12, no WSL
- Command: `uv lock`
- Result: Windows marker selects `pyqt5-qt5==5.15.2`.
- Command: `uv sync --extra identification`
- Result: completed successfully.
- Import results:
  - `hidapi==0.15.0` loaded from `hid.cp312-win_amd64.pyd`
  - `PyQt5==5.15.11`
  - `PyQt5-Qt5==5.15.2`
- Command: `uv run --extra identification --with pytest pytest -q`
- Result: `19 passed`
- Command: `uv run --with ruff ruff check bam/vstone
  tests/test_vstone_cp2110.py`
- Result: `All checks passed!`
- Hardware access: none
