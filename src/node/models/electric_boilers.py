from .base import NodeModel


class ElectricBoilerModel(NodeModel):
    """Модель для работы с электрическим бойлером."""

    discovery_class_: str = "boiler"
