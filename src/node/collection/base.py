from typing import Any, Dict, Generic, TypeVar

import paho.mqtt.client as mqtt

from src.entity.collection import Entity
from src.entity.models import EntityModel
from src.node.models import DeviceModel, NodeModel


NodeM = TypeVar("NodeM", bound=NodeModel)


class Node(Generic[NodeM]):
    """Класс, воплощающий Home Assistant MQTT устройство."""

    def __init__(
        self,
        uid: str,
        mqtt_client: mqtt.Client,
        model: NodeM,
        discovery_prefix: str,
    ) -> None:
        """
        Инициализировать устройство.

        Args:
            mqtt_client: MQTT-клиент, экземпляр paho.mqtt.client.Client
            model: Модель, описывающая устройство для Home Assistant. Для всех сущностей этой устройства
                    поле device в discovery JSON будет равно этой модели
            discovery_prefix: Префикс для discovery топиков в Home Assistant
        """
        self.uid = uid
        self.mqtt_client = mqtt_client
        self.model = model
        self.entities: Dict[str, Entity[Any]] = {}
        self.discovery_prefix = discovery_prefix
        if self.model.identifiers is None:
            self.model.identifiers = [uid]

    def bind_entity(
        self,
        entity: Entity[EntityModel],
    ) -> None:
        """
        Привязать сущность к устройству.

        Args:
            entity: сущность
        """
        if entity.uid in self.entities:
            raise KeyError(f'Сущность с идентификатором "{entity.uid}" уже привязана к устройству')

        entity.bind(
            node_uid=self.uid,
            device_model=DeviceModel(**self.model.model_dump()),
            mqtt_client=self.mqtt_client,
            discovery_prefix=self.discovery_prefix,
        )
        self.entities[entity.uid] = entity

    def unbind_entity(
        self,
        entity: Entity[EntityModel],
    ) -> None:
        """
        Отвязать сущность от устройства.

        Args:
            entity: Сущность
        """
        entity.unbind()
        self.entities.pop(entity.uid)

    def publish_state_all(self) -> None:
        """Опубликовать состояния всех сущностей устройства."""
        for entity in self.entities.values():
            entity.publish_state()

    def publish_discovery_all(self) -> None:
        """Опубликовать дискорд сущностей устройства."""
        for entity in self.entities.values():
            entity.publish_discovery()

    def unpublish_discovery_all(self) -> None:
        """Отменить опубликование дискорд сущностей устройства."""
        for entity in self.entities.values():
            entity.unpublish_discovery()

    def subscribe_all(self) -> None:
        """Подписаться на события всех сущностей устройства."""
        for entity in self.entities.values():
            entity.subscribe()

    def unsubscribe_all(self) -> None:
        """Отменить подписку на события всех сущностей устройства."""
        for entity in self.entities.values():
            entity.unsubscribe()
