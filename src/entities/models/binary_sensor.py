from typing import Optional

from src.entities import enums

from .entity import Entity


class BinarySensor(Entity):
    """Двоичный датчик. Может возвращать только два состояния"""

    discovery_class_: str = "binary_sensor"

    expire_after: Optional[int] = None
    force_update: Optional[bool] = None
    off_delay: Optional[int] = None
    device_class: Optional[enums.BinarySensorEnum] = None
    state_topic: Optional[str] = None
    payload_off: Optional[str] = None
    payload_on: Optional[str] = None
    value_template: Optional[str] = None
