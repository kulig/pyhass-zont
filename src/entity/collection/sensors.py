import random

from src.entity.models import SensorModel

from .base import Entity


class EntityThermoSensorDummy(Entity[SensorModel]):
    """Класс реализации датчика температуры. Заглушка для тестирования."""

    def get_state(self) -> str:
        return str(random.randrange(-300, +700) / 10)  # noqa: S311
