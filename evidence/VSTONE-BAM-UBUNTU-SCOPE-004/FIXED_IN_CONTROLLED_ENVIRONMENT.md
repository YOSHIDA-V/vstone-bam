# Native-Ubuntu scope controlled evidence

- Run ID: `VSTONE-BAM-UBUNTU-SCOPE-004-CONTROLLED-20260911`
- Executed candidate commit:
  `f7c061a9ff707d8eb8f06f10d47a1b41db253d29`
- Remote candidate before run:
  `f7c061a9ff707d8eb8f06f10d47a1b41db253d29`
- Host: Windows; used only to run platform-neutral tests and Ubuntu-targeted
  dependency resolution
- Target resolver: Linux x86-64, CPython 3.12, no WSL
- Ubuntu dependency command: `uv pip compile pyproject.toml --extra
  identification --python-platform x86_64-unknown-linux-gnu --python-version
  3.12 --no-header`
- Ubuntu dependency result: exit `0`; selected `hidapi==0.15.0`,
  `PyQt5==5.15.11`, and `PyQt5-Qt5==5.15.19`.
- HID wheel-only dry run: `uv pip install --dry-run --python-platform
  x86_64-unknown-linux-gnu --python-version 3.12 --only-binary :all:
  hidapi==0.15.0`
- HID wheel-only result: resolved one package and would install
  `hidapi==0.15.0`.
- Lock evidence: CPython 3.12 manylinux2014/manylinux_2_17 x86-64 wheel SHA-256
  `cfdbc74d5c4b5fdeef58a246d80f7dbf4ca33fe741c889505a4a350dd2eb54fb`.
- Test command: `uv run --with pytest pytest -q`
- Test result: `20 passed`
- Static command: `uv run --with ruff ruff check bam/vstone tests`
- Static result: `All checks passed!`
- Build result: source distribution and wheel built successfully.
- Built wheel SHA-256:
  `C56FDAD364F1398D5A8C419DFA6613198D38FF543DEBE818A2C26C5F34A8CF4F`
- Scope limit: native Ubuntu execution, `hid` import on Ubuntu, USB permissions,
  and real CP2110/VS-S055 communication remain unverified.
