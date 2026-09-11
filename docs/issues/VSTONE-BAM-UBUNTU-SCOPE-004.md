# VSTONE-BAM-UBUNTU-SCOPE-004

- State: `FIXED_IN_CONTROLLED_ENVIRONMENT`
- Observed behavior: the CP2110 candidate is described as Windows-native and
  adds a Windows-only Qt dependency constraint, while the requested deployment
  target is native Ubuntu without WSL.
- Failure run ID: `VSTONE-BAM-UBUNTU-SCOPE-004-REPRO-20260911`
- Execution target: `source_contract_at_8d2289c`
- Base commit: `8d2289ce8ea7adcceacd078c45b3ad809810202c`
- Reproduction values:
  - `bam/vstone/cp2110.py` says `Windows-native`.
  - `VstoneBus.open_cp2110` says `Windows-native`.
  - the identification extra directly constrains `PyQt5-Qt5` on Windows.
  - acquisition documentation describes Windows installation.
- Root-cause hypothesis: an ambiguous sentence was resolved to Windows instead
  of waiting for the now-provided native-Ubuntu correction.
- Values that would prove the cause:
  - a source-contract test fails on the Windows-specific implementation and
    dependency declarations at the base commit;
  - Git history identifies those declarations as the prior scope change.
- Files allowed to change:
  - `bam/vstone/cp2110.py`
  - `bam/vstone/bus.py`
  - `pyproject.toml`
  - `tests/test_vstone_platform_scope.py`
  - Vstone acquisition and Issue/evidence documentation
  - removal of the Windows-only Issue/evidence files introduced by the
    incorrect scope
- Files forbidden to change:
  - `bam/vstone/protocol.py` packet encoding, addresses, and unit conversions
  - actuator-model equations and parameters
  - servo ROM, IDs, baud setting, torque state, and physical hardware
- Controlled-environment pass criteria:
  - no Vstone source or acquisition documentation claims a Windows-only target.
  - no Windows-only runtime dependency remains in the identification extra.
  - `hidapi==0.15.0` remains the CP2110 dependency and resolves to a CPython
    3.12 manylinux x86-64 wheel for Ubuntu.
  - CP2110 framing, local-echo, FIFO-recovery, and protocol tests do not regress.
- Target pass criteria:
  - on a separate native Ubuntu machine, install the identification extra and
    read one valid `FD DF` reply through CP2110 without torque or motion writes.
- Previously verified behaviors that must not regress:
  - constructing a Vstone bus performs no implicit torque or motion command.
  - UART and pin configuration are validated but not changed.
  - importing the base package does not require the optional HID dependency.
- Evidence progression:
  - `OBSERVED`: Windows-only language and dependency configuration are present.
  - `REPRODUCED`: the native-Ubuntu source-contract test fails on the direct
    `PyQt5-Qt5` Windows constraint.
  - `ROOT_CAUSE_PROVEN`: commit history and source inspection tie all failing
    declarations to the prior Windows interpretation.
  - `FIXED_IN_CONTROLLED_ENVIRONMENT`: the clean candidate removes the
    Windows-only declarations, resolves its complete identification dependency
    set for Linux x86-64, resolves `hidapi` from a wheel-only source, and passes
    all tests and static checks.
