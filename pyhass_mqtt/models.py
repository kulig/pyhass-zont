import typing as t
import pydantic
from .enums import *


class Model(pydantic.BaseModel):
    def discovery_json(self) -> str:
        return self.json(exclude_none=True, exclude={'discovery_class_'})


class Device(Model):
    configuration_url: str | None = None
    connections: list[tuple[str, str]] | None = None
    hw_version: str | None = None
    identifiers: str | list[str] | None = None
    manufacturer: str | None = None
    model: str | None = None
    name: str | None = None
    serial_number: str | None = None
    suggested_area: str | None = None
    sw_version: str | None = None
    via_device: str | None = None


class Availability(Model):
    payload_available: str | None = None
    payload_not_available: str | None = None
    topic: str | None = None
    value_template: str | None = None


class Entity(Model):
    unique_id: str | None = None
    object_id: str | None = None
    name: str | None = None
    device: Device | None = None
    qos: int | None = 0
    retain: bool = False
    encoding: str | None = 'utf-8'
    icon: str | None = None
    availability: list[Availability] | None = None
    availability_mode: Availability | None = None


class WaterHeater(Entity):
    discovery_class_: str = 'water_heater'

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
    state_topic: str | None = None
    payload_off: str | None = None
    payload_on: str | None = None
    power_command_template: str | None = None
    power_command_topic: str | None = None
    precision: float | None = None
    temperature_command_template: str | None = None
    temperature_command_topic: str | None = None
    temperature_state_template: str | None = None
    temperature_state_topic: str | None = None
    temperature_unit: t.Literal['C', 'F'] | None = None


class BinarySensor(Entity):
    discovery_class_: str = 'binary_sensor'

    expire_after: int | None = None
    force_update: bool | None = None
    off_delay: int | None = None
    device_class: BinarySensorDeviceClass | None = None
    state_topic: str | None = None
    payload_off: str | None = None
    payload_on: str | None = None
    value_template: str | None = None


class Sensor(Entity):
    discovery_class_: str = 'sensor'

    expire_after: int | None = None
    force_update: bool | None = None
    device_class: SensorDeviceClass | None = None
    last_reset_value_template: str | None = None
    suggested_display_precision: int | None = None
    state_class: SensorStateClass | None = None
    unit_of_measurement: str | None = None
    value_template: str | None = None
    state_topic: str | None = None


class Switch(Entity):
    discovery_class_: str = 'switch'

    command_topic: str | None = None
    device_class: SwitchDeviceClass | None = None
    optimistic: bool | None = None
    state_topic: str | None = None
    payload_off: str | None = None
    payload_on: str | None = None
    state_off: str | None = None
    state_on: str | None = None


class Fan(Entity):
    discovery_class_: str = 'fan'

    state_topic: str | None = None
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


class Light(Entity):
    discovery_class_: str = 'light'

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
    state_topic: str | None = None
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
    on_command_type: LightCommandType | None = None
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


class Number(Entity):
    discovery_class_: str = 'number'

    command_template: str | None = None
    command_topic: str | None = None
    state_topic: str | None = None
    device_class: SensorDeviceClass | None = None
    min: float | None = 1
    max: float | None = 100
    step: float | None = 1
    mode: NumberMode | None = None
    payload_reset: str | None = None
    unit_of_measurement: str | None = None
    value_template: str | None = None

