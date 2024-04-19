from typing import Optional

from src.entities import enums

from .entity import EntityModel


class SensorModel(EntityModel):
    """
    Датчик. Возвращает состояние.
    Внимание! Если установлено поле device_class, то обязательно
    следует указывать подходящие единицы измерения в поле unit_of_measurement.
    """

    discovery_class_: str = "sensor"

    expire_after: Optional[None] = None
    force_update: Optional[bool] = None
    device_class: Optional[enums.SensorEnum] = None
    last_reset_value_template: Optional[str] = None
    suggested_display_precision: Optional[int] = None
    state_class: Optional[enums.SensorStateEnum] = None
    unit_of_measurement: Optional[str] = None
    value_template: Optional[str] = None
