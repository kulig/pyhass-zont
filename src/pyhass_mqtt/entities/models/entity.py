from .base import BaseModel
from .device import DeviceModel


class AvailabilityModel(BaseModel):
    """Модель для описания состояния устройства."""

    payload_available: str | None = None
    payload_not_available: str | None = None
    topic: str | None = None
    value_template: str | None = None


class EntityModel(BaseModel):
    """Базовая модель для всех MQTT-сущностей HA."""

    discovery_class_: str

    unique_id: str | None = None
    object_id: str | None = None
    name: str | None = None
    device: DeviceModel | None = None
    state_topic: str | None = None
    qos: int = 0
    retain: bool = False
    encoding: str = "utf-8"
    icon: str | None = None
    availability: list[AvailabilityModel] | None = None
    availability_mode: AvailabilityModel | None = None
