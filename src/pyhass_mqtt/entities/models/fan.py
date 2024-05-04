from .entity import EntityModel


class FanModel(EntityModel):
    """Вентилятор/вентиляционная система."""

    discovery_class_: str = "fan"

    state_value_template: str | None = None
    command_topic: str | None = None
    payload_off: str | None = None
    payload_on: str | None = None
    command_template: str | None = None
    direction_state_topic: str | None = None
    direction_value_template: str | None = None
    direction_command_topic: str | None = None
    direction_command_template: str | None = None
    oscillation_state_topic: str | None = None
    oscillation_value_template: str | None = None
    oscillation_command_topic: str | None = None
    oscillation_command_template: str | None = None
    payload_oscillation_off: str | None = None
    payload_oscillation_on: str | None = None
    percentage_state_topic: str | None = None
    percentage_value_template: str | None = None
    percentage_command_topic: str | None = None
    percentage_command_template: str | None = None
    payload_reset_percentage: str | None = None
    payload_reset_preset_mode: str | None = None
    preset_mode_command_topic: str | None = None
    preset_mode_command_template: str | None = None
    preset_mode_state_topic: str | None = None
    preset_mode_value_template: str | None = None
    preset_modes: list[str] | None = None
    speed_range_max: int | None = None
    speed_range_min: int | None = None
