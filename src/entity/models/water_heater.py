from typing import List, Literal, Optional

from .base import EntityModel


class WaterHeaterModel(EntityModel):
    """Водонагреватель, бойлер."""

    discovery_class_: str = "water_heater"

    current_temperature_template: Optional[str] = None
    current_temperature_topic: Optional[str] = None
    initial: Optional[float] = None
    min_temp: Optional[float] = None
    max_temp: Optional[float] = None
    mode_command_template: Optional[str] = None
    mode_command_topic: Optional[str] = None
    mode_state_template: Optional[str] = None
    mode_state_topic: Optional[str] = None
    modes: Optional[List[str]] = None
    optimistic: Optional[bool] = None
    payload_off: Optional[str] = None
    payload_on: Optional[str] = None
    power_command_template: Optional[str] = None
    power_command_topic: Optional[str] = None
    precision: Optional[float] = None
    temperature_command_template: Optional[str] = None
    temperature_command_topic: Optional[str] = None
    temperature_state_template: Optional[str] = None
    temperature_state_topic: Optional[str] = None
    temperature_unit: Optional[Literal["C", "F"]] = None
