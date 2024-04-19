from typing import Optional

from src.devices.models import DeviceModel
from src.models import Base


class AvailabilityModel(Base):
    """Модель для описания состояния устройства."""

    payload_available: Optional[str] = None
    payload_not_available: Optional[str] = None
    topic: Optional[str] = None
    value_template: Optional[str] = None


class EntityModel(Base):
    """Базовая модель для всех MQTT-сущностей HA."""

    discovery_class_: str

    unique_id: Optional[str] = None
    object_id: Optional[str] = None
    name: Optional[str] = None
    device: Optional[DeviceModel] = None
    state_topic: Optional[str] = None
    qos: int = 0
    retain: bool = False
    encoding: str = "utf-8"
    icon: Optional[str] = None
    availability: Optional[list[AvailabilityModel]] = None
    availability_mode: Optional[AvailabilityModel] = None
