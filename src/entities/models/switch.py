from typing import Optional

from src.entities import enums

from .entity import EntityModel


class SwitchModel(EntityModel):
    """Простейший эффектор с двумя состояниями."""

    discovery_class_: str = "switch"

    command_topic: Optional[str] = None
    device_class: Optional[enums.SwitchEnum] = None
    optimistic: Optional[bool] = None
    payload_off: Optional[str] = None
    payload_on: Optional[str] = None
    state_off: Optional[str] = None
    state_on: Optional[str] = None
