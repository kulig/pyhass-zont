from typing import List, Optional

from .entity import Entity


class Fan(Entity):
    """Вентилятор/вентиляционная система."""

    discovery_class_: str = "fan"

    state_topic: Optional[str] = None
    state_value_template: Optional[str] = None
    command_topic: Optional[str] = None
    payload_off: Optional[str] = None
    payload_on: Optional[str] = None
    command_template: Optional[str] = None
    direction_state_topic: Optional[str] = None
    direction_value_template: Optional[str] = None
    direction_command_topic: Optional[str] = None
    direction_command_template: Optional[str] = None
    oscillation_state_topic: Optional[str] = None
    oscillation_value_template: Optional[str] = None
    oscillation_command_topic: Optional[str] = None
    oscillation_command_template: Optional[str] = None
    payload_oscillation_off: Optional[str] = None
    payload_oscillation_on: Optional[str] = None
    percentage_state_topic: Optional[str] = None
    percentage_value_template: Optional[str] = None
    percentage_command_topic: Optional[str] = None
    percentage_command_template: Optional[str] = None
    payload_reset_percentage: Optional[str] = None
    payload_reset_preset_mode: Optional[str] = None
    preset_mode_command_topic: Optional[str] = None
    preset_mode_command_template: Optional[str] = None
    preset_mode_state_topic: Optional[str] = None
    preset_mode_value_template: Optional[str] = None
    preset_modes: Optional[List[str]] = None
    speed_range_max: Optional[int] = None
    speed_range_min: Optional[int] = None
