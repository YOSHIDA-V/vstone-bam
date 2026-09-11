import tomllib
from pathlib import Path

ROOT = Path(__file__).parents[1]


def test_vstone_cp2110_target_is_native_ubuntu_without_windows_constraints():
    project = tomllib.loads(
        (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    )
    dependencies = project["project"]["optional-dependencies"]["identification"]
    source_text = "\n".join(
        (ROOT / path).read_text(encoding="utf-8")
        for path in ("bam/vstone/cp2110.py", "bam/vstone/bus.py")
    )
    acquisition = (ROOT / "docs/identification/acquisition.rst").read_text(
        encoding="utf-8"
    )

    assert not any(
        dependency.lower().startswith("pyqt5-qt5")
        for dependency in dependencies
    )
    assert "Windows-native" not in source_text
    assert "native Windows" not in acquisition
    assert "Ubuntu" in acquisition
    assert "does not require WSL" in acquisition
