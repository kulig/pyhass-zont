from pydantic import BaseModel as PydanticModel


class BaseModel(PydanticModel):
    """Базовый класс для моделей устройств и сущностей"""

    def discovery_json(self) -> str:
        """
        Выгрузить JSON-описание, совместимое с Home Assistant MQTT discovery

        Returns:
            Строка, содержащая JSON discovery-пакета
        """
        return self.model_dump_json(
            exclude_none=True,
            exclude={"discovery_class_"},
        )
