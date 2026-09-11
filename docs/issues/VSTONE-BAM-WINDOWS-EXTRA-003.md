# VSTONE-BAM-WINDOWS-EXTRA-003

- State: `FIXED_IN_CONTROLLED_ENVIRONMENT`
- Observed behavior: on native 64-bit Windows with CPython 3.12,
  `uv sync --extra identification` cannot install the existing BAM
  identification dependencies.
- Failure run ID: `VSTONE-BAM-WINDOWS-EXTRA-003-REPRO-20260911`
- Execution target: `native_windows_win_amd64`
- Base commit: `1541e4cafa1b5821474e49ec0732e5abb6e7d7c1`
- Reproduction result: dependency resolution selects `pyqt5-qt5==5.15.19`,
  which has no `win_amd64` wheel or source distribution.
- Proven root cause: the `identification` extra declares unconstrained `PyQt5`.
  Its transitive Qt runtime can therefore resolve to a release that does not
  support Windows, preventing installation before Vstone code starts.
- Controlled check: `PyQt5==5.15.11` with `PyQt5-Qt5==5.15.2` imports
  successfully on this native Windows CPython 3.12 runtime.
- Files allowed to change:
  - `pyproject.toml`
  - Vstone acquisition documentation
  - this Issue contract and its evidence directory
- Files forbidden to change:
  - BAM actuator-model equations and parameters
  - Vstone packet encoding and CP2110 transport behavior
  - servo or CP2110 hardware state
- Controlled-environment pass criteria:
  - the Windows dependency graph selects `PyQt5-Qt5==5.15.2`.
  - `uv sync --extra identification` completes on native Windows.
  - both `PyQt5` and the compiled Windows `hidapi` module import.
  - the complete test suite and static checks remain green.
- Target pass criteria: none; this is an installation-only Issue and sends no
  command to physical hardware.
- Evidence progression:
  - `OBSERVED`: native Windows installation failed before Vstone code started.
  - `REPRODUCED`: the failure consistently selected unsupported
    `pyqt5-qt5==5.15.19`.
  - `ROOT_CAUSE_PROVEN`: an explicit Windows-compatible Qt runtime constraint
    made the isolated control installation succeed.
  - `FIXED_IN_CONTROLLED_ENVIRONMENT`: the complete `identification` extra now
    synchronizes, both native modules import, and all tests pass on Windows.
