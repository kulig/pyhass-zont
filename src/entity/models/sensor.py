from typing import Optional

from . import enums
from .base import EntityModel


class SensorModel(EntityModel):
    """
    Датчик. Возвращает состояние.
    Внимание! Если установлено поле device_class, то обязательно
    следует указывать подходящие единицы измерения в поле unit_of_measurement.
    """

    discovery_class_: str = "sensor"

    expire_after: Optional[int] = None
    force_update: Optional[bool] = None
    device_class: Optional[enums.SensorEnum] = None
    last_reset_value_template: Optional[str] = None
    suggested_display_precision: Optional[int] = None
    state_class: Optional[enums.SensorStateEnum] = None
    unit_of_measurement: Optional[str] = None
    value_template: Optional[str] = None


class ThermoSensorDummyModel(SensorModel):
    """Датчик температуры. Заглушка для тестирования."""

    name: str = 'Dummy thermo sensor'
    expire_after: int = 600
    device_class: enums.SensorEnum = enums.SensorEnum.temperature
    unit_of_measurement: str = '°C'
    suggested_display_precision: int = 1
    icon: str = 'mdi:thermometer-water'
