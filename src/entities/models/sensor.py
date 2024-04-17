from typing import Optional

from src.entities import enums

from .entity import Entity


class Sensor(Entity):
    """
    Датчик. Возвращает состояние.
    Внимание! Если установлено поле device_class, то обязательно
    следует указывать подходящие единицы измерения в поле unit_of_measurement.
    """

    discovery_class_: str = "sensor"

    expire_after: Optional[None] = None
    force_update: Optional[bool] = None
    device_class: enums.SensorEnum | None = None
    last_reset_value_template: Optional[str] = None
    suggested_display_precision: int | None = None
    state_class: Optional[enums.SensorStateEnum] = None
    unit_of_measurement: Optional[str] = None
    value_template: Optional[str] = None
    state_topic: Optional[str] = None
