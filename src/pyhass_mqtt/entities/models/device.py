from .base import BaseModel


class DeviceModel(BaseModel):
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
