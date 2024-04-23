from typing import List, Optional, Tuple

from src.models import Base


class DeviceModel(Base):
    """Базовая модель ноды."""

    name: str
    manufacturer: str
    model: str
    sw_version: Optional[str]
    identifiers: Optional[List[str]] = None
    hw_version: Optional[str] = None
    serial_number: Optional[str] = None
    suggested_area: Optional[str] = None
    configuration_url: Optional[str] = None
    connections: Optional[List[Tuple[str, str]]] = None
    via_device: Optional[str] = None


class NodeModel(DeviceModel):
    """Базовая модель устройства."""

    discovery_class_: str = "boiler"
