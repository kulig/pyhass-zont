from typing import Optional

from src.entities import enums

from .entity import EntityModel


class NumberModel(EntityModel):
    """Эффектор с float-состоянием."""

    discovery_class_: str = "number"

    command_template: Optional[str] = None
    command_topic: Optional[str] = None
    device_class: Optional[enums.SensorEnum] = None
    min: Optional[float] = 1
    max: Optional[float] = 100
    step: Optional[float] = 1
    mode: Optional[enums.NumberModeEnum] = None
    payload_reset: Optional[str] = None
    unit_of_measurement: Optional[str] = None
    value_template: Optional[str] = None
