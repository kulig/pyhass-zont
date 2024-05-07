from .. import enums

from .entity import EntityModel


class BinarySensorModel(EntityModel):
    """Двоичный датчик. Может возвращать только два состояния"""

    discovery_class_: str = "binary_sensor"

    expire_after: int | None = None
    force_update: bool | None = None
    off_delay: int | None = None
    device_class: enums.BinarySensorDeviceClass | None = None
    payload_off: str | None = None
    payload_on: str | None = None
    value_template: str | None = None
