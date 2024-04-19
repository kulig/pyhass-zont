from src.entities import enums
from src.entities import Entity
from src.entities.models import SensorModel


class TemperatureSensor(Entity[SensorModel]):
    name = 'Thermosensor from python {id_}'
    expire_after = 600
    device_class = enums.SensorEnum.temperature
    suggested_display_precision = 1
