from typing import Dict
import paho.mqtt.client as mqtt
from src.devices import models
from src.entities import Entity


class Device:
    """Класс, воплощающий Home Assistant MQTT устройство."""

    def __init__(
        self,
        id_: str,
        client: mqtt.Client,
        device: models.Device,
        discovery_prefix,
    ) -> None:
        """
        Инициализировать устройство

        Args:
            id_: Уникальный идентификатор устройства, используется для генерации object_id и топиков
            client: MQTT-клиент, экземпляр paho.mqtt.client.Client
            device: Модель, описывающая устройство для Home Assistant. Для всех сущностей этой устройства
                    поле device в discovery JSON будет равно этой модели
            discovery_prefix: Префикс для discovery топиков в Home Assistant
        """
        self.client: mqtt.Client = client
        self.id = id_
        self.device = device
        self.discovery_prefix = discovery_prefix
        self.entities: Dict[str, Entity] = {}

    def add_entity(self, obj: Entity) -> None:
        """
        Добавить сущность в устройство.

        Args:
            obj: сущность
        """
        if obj.node == self:
            return
        if obj.node is not None:
            obj.node.remove_entity(obj)
        if obj.id in self.entities:
            raise KeyError(f'Duplicate entity "{obj.id}"')
        self.entities[obj.id] = obj
        obj.set_node(self)
        obj.subscribe()
        obj.publish_discovery()
        obj.publish_state()

    def remove_entity(self, obj: Entity) -> None:
        """
        Удалить сущность из устройства

        Args:
            obj: Сущность
        """
        obj.unpublish_discovery()
        obj.unsubscribe()
        obj.set_node(None)
        del self.entities[obj.unique_id]

    def publish_state_all(self) -> None:
        """Опубликовать состояния всех сущностей устройства."""
        for obj in self.entities.values():
            obj.publish_state()

    def publish_discovery_all(self) -> None:
        """Опубликовать дискорд сущностей устройства."""
        for obj in self.entities.values():
            obj.publish_discovery()

    def unpublish_discovery_all(self) -> None:
        """Отменить опубликование дискорд сущностей устройства."""
        for obj in self.entities.values():
            obj.unpublish_discovery()

    def subscribe_all(self) -> None:
        """Подписаться на события всех сущностей устройства."""
        for obj in self.entities.values():
            obj.subscribe()

    def unsubscribe_all(self) -> None:
        """Отменить подписку на события всех сущностей устройства."""
        for obj in self.entities.values():
            obj.unsubscribe()
