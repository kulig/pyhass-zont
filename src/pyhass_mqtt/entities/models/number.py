from .. import enums

from .entity import EntityModel


class NumberModel(EntityModel):
    """Эффектор с float-состоянием."""

    discovery_class_: str = "number"

    command_template: str | None = None
    command_topic: str | None = None
    device_class: enums.SensorDeviceClass | None = None
    min: float | None = 1
    max: float | None = 100
    step: float | None = 1
    mode: enums.NumberMode | None = None
    payload_reset: str | None = None
    unit_of_measurement: str | None = None
    value_template: str | None = None
