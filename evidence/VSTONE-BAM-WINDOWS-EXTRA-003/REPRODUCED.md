# Windows identification-extra failure evidence

- Run ID: `VSTONE-BAM-WINDOWS-EXTRA-003-REPRO-20260911`
- Runtime: native Windows `win_amd64`, CPython 3.12, no WSL
- Base commit: `1541e4cafa1b5821474e49ec0732e5abb6e7d7c1`
- Command: `uv sync --extra identification`
- Exit status: nonzero
- Error: `pyqt5-qt5==5.15.19` has no source distribution or wheel for
  `win_amd64`.
- Root-cause check: the base `pyproject.toml` declares `PyQt5` without a
  Windows-compatible Qt runtime constraint.
- Control command: isolated installation of `PyQt5==5.15.11` and
  `PyQt5-Qt5==5.15.2`
- Control result: both packages installed and `PyQt5` imported on Windows.
- Hardware access: none

