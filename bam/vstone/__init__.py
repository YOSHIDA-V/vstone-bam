"""Vstone VS-S055 support for BAM."""

from .actuator import VSS055Actuator
from .bus import VstoneBus

__all__ = ["VSS055Actuator", "VstoneBus"]
