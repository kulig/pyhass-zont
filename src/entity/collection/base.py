from typing import Generic, Optional, TypeVar

import paho.mqtt.client as mqtt

from src.entity.models import EntityModel
from src.node.models import DeviceModel


EntityM = TypeVar("EntityM", bound=EntityModel)


class Entity(Generic[EntityM]):
    """
    Базовый класс для определения MQTT-сущностей, которые понимаются Home Assistant.
    https://www.home-assistant.io/integrations/mqtt/
    """

    def __init__(
        self,
        uid: str,
        model: EntityM,
    ) -> None:
        """
        Инициализировать сущность.

        Args:
            uid: Строка, содержащая уникальный идентификатор сущности в рамках устройства.
            entity_model: Модель, описывающая сущность для Home Assistant.
        """
        self.uid = uid
        self.model = model
        self.model.name = f"{self.model.name} ({self.uid})"
        self.discovery_topic: Optional[str] = None
        self.mqtt_client: Optional[mqtt.Client] = None
        self.node_uid: Optional[str] = None

    def bind(
        self,
        node_uid: str,
        device_model: DeviceModel,
        mqtt_client: mqtt.Client,
        discovery_prefix: str,
    ) -> None:
        """
        Привязать сущность к устройству.

        Args:
            node_model: Модель устройства для Home Assistant.
            mqtt_client: MQTT-клиент, экземпляр paho.mqtt.client.Client
            discovery_prefix: Префикс для discovery топиков в Home Assistant
        """
        self.mqtt_client = mqtt_client
        self.model.unique_id = f"{node_uid}_{self.uid}"
        self.model.object_id = self.model.unique_id
        self.model.state_topic = f"{node_uid}/{self.uid}/state"
        self.model.device = device_model
        self.discovery_topic = f"{discovery_prefix}/{self.model.discovery_class_}/{node_uid}/{self.uid}/config"
        self.node_uid = node_uid

        self.subscribe()
        self.publish_discovery()
        self.publish_state()

    def unbind(self) -> None:
        """Отвязать сущность от устройства."""
        self.unpublish_discovery()
        self.unsubscribe()

        self.mqtt_client = None
        self.model.object_id = None
        self.model.unique_id = None
        self.model.state_topic = None
        self.model.device = None
        self.discovery_topic = None
        self.node_uid = None

    def subscribe(self) -> None:
        """
        Подписаться на все интересующие топики.
        В наследниках этого класса при переопределении сначала желательно вызвать родителя.

        Чтобы подписаться, используем:
            self.mqtt_client.subscribe(topic)
            self.mqtt_client.message_callback_add(topic, on_msg)
        Обработчик должен быть таким:
            def on_message(
                mqtt_client: mqtt.Client,
                userdata: Any,
                message: mqtt.MQTTMessage
            ) -> None
        """
        if self.node_uid is None:
            raise RuntimeError("Нельзя подписаться на топики без привязки к устройству")

        if self.mqtt_client is None:
            raise RuntimeError("Нельзя подписаться на топики без mqtt клиента")

    def unsubscribe(self) -> None:
        """
        Отписаться от всех топиков.
        В наследниках этого класса при переопределении сначала желательно вызвать родителя.

        Чтобы отписаться, используем:
            self.mqtt_client.message_callback_remove(topic)
            self.mqtt_client.unsubscribe(topic)
        """

        if self.node_uid is None:
            raise RuntimeError("Нельзя отписаться от топиков без привязки к устройству")

        if self.mqtt_client is None:
            raise RuntimeError("Нельзя отписаться от топиков без mqtt клиента")

    def get_state(self) -> str:
        """Получить состояние."""
        raise NotImplementedError('Метод "get_state" не определен')

    def publish_state(self) -> None:
        """Опубликовать состояние в state_topic"""

        if self.node_uid is None:
            raise RuntimeError("Нельзя опубликовать состояние без привязки к устройству")

        if self.mqtt_client is None:
            raise RuntimeError("Нельзя опубликовать состояние без mqtt клиента")

        if self.model.state_topic is None:
            raise RuntimeError("Нельзя опубликовать состояние без mqtt топика")

        self.mqtt_client.publish(
            self.model.state_topic,
            self.get_state().encode(self.model.encoding),
            self.model.qos,
            self.model.retain,
        )

    def publish_discovery(self) -> None:
        """Опубликовать MQTT discovery JSON для Home Assistant в соответствующем топике."""

        if self.node_uid is None:
            raise RuntimeError("Нельзя опубликовать MQTT discovery JSON без привязки к устройству")

        if self.mqtt_client is None:
            raise RuntimeError("Нельзя опубликовать MQTT discovery JSON без mqtt клиента")

        if self.discovery_topic is None:
            raise RuntimeError("Нельзя опубликовать MQTT discovery JSON без discovery топика")

        self.mqtt_client.publish(
            self.discovery_topic,
            self.model.discovery_json(),
            1,
            False,
        )

    def unpublish_discovery(self) -> None:
        """Снять с публикации MQTT discovery JSON для Home Assistant."""

        if self.node_uid is None:
            raise RuntimeError("Нельзя снять с публикации MQTT discovery JSON без привязки к устройству")

        if self.mqtt_client is None:
            raise RuntimeError("Нельзя снять с публикации MQTT discovery JSON без mqtt клиента")

        if self.discovery_topic is None:
            raise RuntimeError("Нельзя снять с публикации MQTT discovery JSON без discovery топика")

        self.mqtt_client.publish(
            self.discovery_topic,
            "",
            1,
            False,
        )
