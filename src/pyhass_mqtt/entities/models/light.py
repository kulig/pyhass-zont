from .. import enums

from .entity import EntityModel


class LightModel(EntityModel):
    """Освещение, в т.ч. регулируемой яркости и цвета."""

    discovery_class_: str = "light"

    brightness_command_topic: str | None = None
    brightness_command_template: str | None = None
    brightness_scale: int | None = None
    brightness_state_topic: str | None = None
    brightness_value_template: str | None = None
    color_mode_state_topic: str | None = None
    color_mode_value_template: str | None = None
    color_temp_command_template: str | None = None
    color_temp_command_topic: str | None = None
    color_temp_state_topic: str | None = None
    color_temp_value_template: str | None = None
    command_topic: str | None = None
    payload_off: str | None = None
    payload_on: str | None = None
    state_value_template: str | None = None
    effect_command_topic: str | None = None
    effect_command_template: str | None = None
    effect_list: list[str] | None = None
    effect_state_topic: str | None = None
    effect_value_template: str | None = None
    hs_command_template: str | None = None
    hs_command_topic: str | None = None
    hs_state_topic: str | None = None
    hs_value_template: str | None = None
    max_mireds: int | None = None
    min_mireds: int | None = None
    on_command_type: enums.LightCommand | None = None
    rgb_command_template: str | None = None
    rgb_command_topic: str | None = None
    rgb_state_topic: str | None = None
    rgb_value_template: str | None = None
    rgbw_command_template: str | None = None
    rgbw_command_topic: str | None = None
    rgbw_state_topic: str | None = None
    rgbw_value_template: str | None = None
    rgbww_command_template: str | None = None
    rgbww_command_topic: str | None = None
    rgbww_state_topic: str | None = None
    rgbww_value_template: str | None = None
    white_command_topic: str | None = None
    white_scale: int | None = None
    xy_command_template: str | None = None
    xy_command_topic: str | None = None
    xy_state_topic: str | None = None
    xy_value_template: str | None = None
