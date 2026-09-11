# VSTONE-BAM-CP2110-002

- State: `FIXED_IN_CONTROLLED_ENVIRONMENT`
- Observed behavior: the previously used VS-S055 path communicates through a
  CP2110 HID adapter with 115200 baud, 8N1, disabled flow control, open-drain TX,
  length-prefixed HID reports, local-echo validation, and FIFO recovery. The
  current `VstoneBus.open` path only opens a pyserial port and the package has no
  CP2110 transport.
- Failure run ID: `VSTONE-BAM-CP2110-002-REPRO-20260911`
- Execution target: `controlled_fake_cp2110_only`
- Base commit: `d090afe6e6d94d09c9480c215dbcdb494e8e1228`
- Reference repository commit: `eea97c3bd874ef3ca6bdeb8fb0a638970c158e1f`
- Reference `protocol.py` SHA-256:
  `f149f45490715c07f66baea4f3730bc021eb4aa24ba761efe5bbf1e601e207bf`
- Reference `sources.py` SHA-256:
  `21f9b7703d3c4e8298c5e0b10ef407daf9a318bb01eff0c00d26f4e1258e3450`
- Current `bam/vstone/bus.py` SHA-256:
  `744c9819972df5e01fedd7d7f8941ba45f20a42f437b8706e195724cdaf566fe`
- Reproduction values:
  - `bam.vstone.cp2110` cannot be imported.
  - `VstoneBus` has no `open_cp2110` constructor.
  - the `identification` extra does not declare `pycp2110`.
- Proven root cause: the packet codec was added, but the CP2110 physical
  transport used by the existing dual-arm reader was not added at the transport
  boundary.
- Values that would prove the cause:
  - a failing import/contract test at the base commit;
  - repository search showing pyserial as the only concrete Vstone transport.
- Evidence progression:
  - `OBSERVED`: the known CP2110 workflow is absent from `bam.vstone`.
  - `REPRODUCED`: the contract test fails with
    `ModuleNotFoundError: No module named 'bam.vstone.cp2110'`.
  - `ROOT_CAUSE_PROVEN`: source search finds only the pyserial import and
    `serial.Serial` construction in `bam/vstone/bus.py`; no CP2110 transport or
    constructor exists.
  - `FIXED_IN_CONTROLLED_ENVIRONMENT`: the platform-neutral fake-HID suite
    passes, and the built wheel contains both the CP2110 module and its optional
    dependency metadata.
- Files allowed to change:
  - `bam/vstone/cp2110.py`
  - `bam/vstone/bus.py`
  - `bam/vstone/__init__.py`
  - `pyproject.toml`
  - `tests/test_vstone_cp2110.py`
  - Vstone acquisition documentation
  - this Issue contract and its evidence directory
- Files forbidden to change:
  - `bam/vstone/protocol.py` packet encoding, addresses, and unit conversions
  - actuator-model equations and parameters
  - existing manufacturer drivers
  - servo ROM, IDs, baud setting, torque state, and physical hardware
- Controlled-environment pass criteria:
  - `hidapi==0.15.0` is an optional identification dependency and is imported
    only when CP2110 access is requested.
  - no WSL runtime or `pycp2110` wrapper is required.
  - the CP2110 transport validates an already-enabled UART at the explicitly
    requested baud, 8 data bits, no parity, one stop bit, and no flow control.
  - TX must already be open-drain; a mismatched adapter is closed and rejected
    without writing feature reports or enabling/changing UART configuration.
  - multiple adapters require an explicit CP2110 serial number.
  - both FIFOs are purged before the first transaction and during retry recovery.
  - UART writes use the CP2110 one-byte length prefix and reject payloads over
    63 bytes.
  - local echo must match byte-for-byte and is removed before the `FD DF` response
    reaches `VstoneBus`.
  - the verified position-read request remains
    `FA AF 01 0F 2A 02 00 26`.
  - existing pyserial construction and all upstream tests do not regress.
- Target pass criteria:
  - after separate explicit hardware authorization on native Ubuntu, the same
    immutable candidate reads one valid `FD DF` response through CP2110 without
    sending torque or target-position commands.
- Previously verified behaviors that must not regress:
  - the existing dual-arm CP2110 reader remains the rollback reference and is not
    modified.
  - constructing a Vstone bus performs no implicit torque or motion command.
  - importing the base package does not require a hardware dependency.
