import tomllib
from importlib import import_module
from pathlib import Path


def test_cp2110_transport_contract_is_available():
    cp2110_transport = import_module("bam.vstone.cp2110")
    vstone = import_module("bam.vstone")

    assert hasattr(cp2110_transport, "Cp2110Transport")
    assert hasattr(vstone.VstoneBus, "open_cp2110")

    project = tomllib.loads(
        (Path(__file__).parents[1] / "pyproject.toml").read_text(encoding="utf-8")
    )
    assert "pycp2110==1.0.0" in project["project"]["optional-dependencies"][
        "identification"
    ]
