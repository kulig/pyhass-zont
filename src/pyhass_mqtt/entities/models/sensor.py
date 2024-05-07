from .. import enums

from .entity import EntityModel


class SensorModel(EntityModel):
    """
    Датчик. Возвращает состояние.
    Внимание! Если установлено поле device_class, то обязательно
    следует указывать подходящие единицы измерения в поле unit_of_measurement.
    """

    discovery_class_: str = "sensor"

    expire_after: int | None = None
    force_update: bool | None = None
    device_class: enums.SensorDeviceClass | None = None
    last_reset_value_template: str | None = None
    suggested_display_precision: int | None = None
    state_class: enums.SensorState | None = None
    unit_of_measurement: str | None = None
    value_template: str | None = None
