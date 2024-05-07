from .. import enums

from .entity import EntityModel


class SwitchModel(EntityModel):
    """Простейший эффектор с двумя состояниями."""

    discovery_class_: str = "switch"

    command_topic: str | None = None
    device_class: enums.Switch | None = None
    optimistic: bool | None = None
    payload_off: str | None = None
    payload_on: str | None = None
    state_off: str | None = None
    state_on: str | None = None
