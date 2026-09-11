# VSTONE-BAM-PROTOCOL-001 observed evidence

- Timestamp UTC: `2026-09-11T02:54:42.9625945Z`
- Run ID: `VSTONE-BAM-PROTOCOL-001-OBSERVED-20260911`
- Execution target: `offline_protocol_codec_only`
- Working directory:
  `C:\Users\yoshi\Documents\ChatGPT\robovie-z\vstone-bam`
- Base commit: `620a64fe67c1afe94fca81da73b128c7aed17c5f`
- Python: `3.12.13`
- uv: `0.11.15`
- Test SHA-256:
  `6B3E7C1AFD8E358D81BF544CE3DBF9CCD07164A3E5B6D8D73283DEBA2846054F`
- Futaba manual SHA-256:
  `E483B96F7D9865FE8F25CC2EC9C9AFB22B68CB1F25D2E2ABA5BDBF848BE0E04D`
- Command:
  `uv run --with pytest pytest -q tests/test_vstone_protocol.py`
- Result: exit code `1`; `6 failed in 0.40s`
- Reproduced failure: every test reaches
  `ModuleNotFoundError: No module named 'bam.vstone'`.
- Physical device access: not performed
- Servo command transmission: not performed

This evidence proves only that the upstream base lacks the declared Vstone
protocol boundary. It does not prove VS-S055 compatibility or identify servo
model parameters.

