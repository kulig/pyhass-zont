from typing import Optional

from src.models import Base

from src.devices import Device


class Availability(Base):
    payload_available: Optional[str] = None
    payload_not_available: Optional[str] = None
    topic: Optional[str] = None
    value_template: Optional[str] = None


class Entity(Base):
    """
    Базовая модель для всех MQTT-сущностей HA
    """

    unique_id: Optional[str] = None
    object_id: Optional[str] = None
    name: Optional[str] = None
    device: Optional[Device] = None
    qos: Optional[int] = 0
    retain: bool = False
    encoding: Optional[str] = "utf-8"
    icon: Optional[str] = None
    availability: Optional[list[Availability]] = None
    availability_mode: Optional[Availability] = None
