from typing import Literal

from .entity import EntityModel


class WaterHeaterModel(EntityModel):
    """Водонагреватель, бойлер."""

    discovery_class_: str = "water_heater"

    current_temperature_template: str | None = None
    current_temperature_topic: str | None = None
    initial: float | None = None
    min_temp: float | None = None
    max_temp: float | None = None
    mode_command_template: str | None = None
    mode_command_topic: str | None = None
    mode_state_template: str | None = None
    mode_state_topic: str | None = None
    modes: list[str] | None = None
    optimistic: bool | None = None
    payload_off: str | None = None
    payload_on: str | None = None
    power_command_template: str | None = None
    power_command_topic: str | None = None
    precision: float | None = None
    temperature_command_template: str | None = None
    temperature_command_topic: str | None = None
    temperature_state_template: str | None = None
    temperature_state_topic: str | None = None
    temperature_unit: Literal["C", "F"] | None = None
