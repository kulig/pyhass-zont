from typing import List, Optional

from src.entities import Entity, enums


class Light(Entity):
    """Освещение, в т.ч. регулируемой яркости и цвета."""

    discovery_class_: str = "light"

    brightness_command_topic: Optional[str] = None
    brightness_command_template: Optional[str] = None
    brightness_scale: Optional[int] = None
    brightness_state_topic: Optional[str] = None
    brightness_value_template: Optional[str] = None
    color_mode_state_topic: Optional[str] = None
    color_mode_value_template: Optional[str] = None
    color_temp_command_template: Optional[str] = None
    color_temp_command_topic: Optional[str] = None
    color_temp_state_topic: Optional[str] = None
    color_temp_value_template: Optional[str] = None
    command_topic: Optional[str] = None
    payload_off: Optional[str] = None
    payload_on: Optional[str] = None
    state_topic: Optional[str] = None
    state_value_template: Optional[str] = None
    effect_command_topic: Optional[str] = None
    effect_command_template: Optional[str] = None
    effect_list: Optional[List[str]] = None
    effect_state_topic: Optional[str] = None
    effect_value_template: Optional[str] = None
    hs_command_template: Optional[str] = None
    hs_command_topic: Optional[str] = None
    hs_state_topic: Optional[str] = None
    hs_value_template: Optional[str] = None
    max_mireds: Optional[int] = None
    min_mireds: Optional[int] = None
    on_command_type: Optional[enums.LightCommandType] = None
    rgb_command_template: Optional[str] = None
    rgb_command_topic: Optional[str] = None
    rgb_state_topic: Optional[str] = None
    rgb_value_template: Optional[str] = None
    rgbw_command_template: Optional[str] = None
    rgbw_command_topic: Optional[str] = None
    rgbw_state_topic: Optional[str] = None
    rgbw_value_template: Optional[str] = None
    rgbww_command_template: Optional[str] = None
    rgbww_command_topic: Optional[str] = None
    rgbww_state_topic: Optional[str] = None
    rgbww_value_template: Optional[str] = None
    white_command_topic: Optional[str] = None
    white_scale: Optional[int] = None
    xy_command_template: Optional[str] = None
    xy_command_topic: Optional[str] = None
    xy_state_topic: Optional[str] = None
    xy_value_template: Optional[str] = None
