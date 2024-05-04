from __future__ import annotations
import paho.mqtt.client as mqtt

from .entities.models import DeviceModel, EntityModel


__all__ = [
    'Device',
    'Entity',
]


class Device:
    """Класс, воплощающий Home Assistant MQTT устройство. Устройство состоит из множества сущностей."""

    def __init__(
        self,
        id_: str,
        mqtt_client: mqtt.Client,
        device_model: DeviceModel,
        discovery_prefix: str = 'homeassistant',
    ) -> None:
        """
        Инициализировать устройство

        Args:
            id_: Уникальный идентификатор устройства, используется для генерации object_id и топиков
            client: MQTT-клиент, экземпляр paho.mqtt.client.Client
            device_model: Модель, описывающая устройство для Home Assistant. Для всех сущностей этой устройства
                          поле "device" в discovery JSON будет равно этой модели
            discovery_prefix: Префикс для discovery топиков в Home Assistant
        """
        self.mqtt_client = mqtt_client
        self.id = id_
        self.device_model = device_model
        self.discovery_prefix = discovery_prefix
        self.entities: dict[str, Entity] = {}

    def add_entity(self, obj: Entity) -> None:
        """
        Добавить сущность в устройство.

        Args:
            obj: сущность
        """
        if obj.owner == self:
            return
        if obj.owner is not None:
            obj.owner.remove_entity(obj)
        if obj.uid in self.entities:
            raise KeyError(f'Duplicate entity "{obj.uid}"')
        self.entities[obj.uid] = obj
        obj.bind(self)
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
        obj.unbind()
        del self.entities[obj.uid]

    def publish_state_all(self) -> None:
        """Опубликовать состояния всех сущностей устройства."""
        for obj in self.entities.values():
            obj.publish_state()

    def publish_discovery_all(self) -> None:
        """Опубликовать дискавери сущностей устройства."""
        for obj in self.entities.values():
            obj.publish_discovery()

    def unpublish_discovery_all(self) -> None:
        """Отменить опубликование дискавери сущностей устройства."""
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


class Entity:
    """
    Базовый класс для определения MQTT-сущностей, которые понимаются Home Assistant.
    https://www.home-assistant.io/integrations/mqtt/
    """

    def __init__(
        self,
        uid: str,
        entity_model: EntityModel,
    ) -> None:
        """
        Инициализировать сущность.

        Args:
            uid: Строка, содержащая уникальный идентификатор сущности в рамках устройства.
            entity_model: Модель, описывающая сущность для Home Assistant.
        """
        self.uid = uid
        self.name = entity_model.name
        self.model = entity_model
        self.discovery_topic: str | None = None
        self.owner: Device | None = None

    def on_bind(self) -> None:
        pass

    def bind(
        self,
        device: Device,
    ) -> None:
        """
        Привязать сущность к устройству.

        Args:
            device: Устройство, частью которого будет эта сущность
        """
        self.owner = device
        self.model.device = self.owner.device_model
        self.model.object_id = self.model.unique_id = f"{self.owner.id}_{self.uid}"
        self.model.state_topic = f"{self.owner.id}/{self.uid}/state"
        self.discovery_topic = (
            f"{self.owner.discovery_prefix}/{self.model.discovery_class_}/{self.owner.id}/{self.uid}/config"
        )

        self.on_bind()

        self.subscribe()
        self.publish_discovery()
        self.publish_state()

    def unbind(self) -> None:
        """
        Отвязать сущность от устройства.

        Args:
            device_model: Модель устройства для Home Assistant.
            mqtt_client: MQTT-клиент, экземпляр paho.mqtt.client.Client
        """
        self.unpublish_discovery()
        self.unsubscribe()

        self.owner = None
        self.model.device = None
        self.model.object_id = self.model.unique_id = None
        self.model.state_topic = None
        self.discovery_topic = None

    def subscribe(self) -> None:
        """
        Подписаться на все интересующие топики.
        В наследниках этого класса при переопределении сначала желательно вызвать родителя.

        Чтобы подписаться, используем:
            self.owner.mqtt_client.subscribe(topic)
            self.owner.mqtt_client.message_callback_add(topic, on_msg)
        Обработчик должен быть таким:
            def on_message(
                mqtt_client: mqtt.Client,
                userdata: Any,
                message: mqtt.MQTTMessage
            ) -> None
        """
        if not self.owner:
            raise RuntimeError("Нельзя подписаться на топики без привязки к устройству")

    def unsubscribe(self) -> None:
        """
        Отписаться от всех топиков.
        В наследниках этого класса при переопределении сначала желательно вызвать родителя.

        Чтобы отписаться, используем:
            self.owner.mqtt_client.message_callback_remove(topic)
            self.owner.mqtt_client.unsubscribe(topic)
        """

        if not self.owner:
            raise RuntimeError("Нельзя отписаться от топиков без привязки к устройству")

    def get_state(self) -> str:
        """Получить состояние."""
        raise NotImplementedError('Метод "get_state" не определен')

    def publish_state(self) -> None:
        """Опубликовать состояние в state_topic"""
        if not self.owner:
            raise RuntimeError("Нельзя опубликовать состояние без привязки к устройству")

        self.owner.mqtt_client.publish(
            self.model.state_topic,
            self.get_state().encode(self.model.encoding),
            self.model.qos,
            self.model.retain,
        )

    def publish_discovery(self) -> None:
        """Опубликовать MQTT discovery JSON для Home Assistant в соответствующем топике."""
        if not self.owner:
            raise RuntimeError("Нельзя опубликовать MQTT discovery JSON без привязки к устройству")

        self.owner.mqtt_client.publish(
            self.discovery_topic,
            self.model.discovery_json(),
            1,
            False,
        )

    def unpublish_discovery(self) -> None:
        """Снять с публикации MQTT discovery JSON для Home Assistant."""
        if not self.owner:
            raise RuntimeError("Нельзя снять с публикации MQTT discovery JSON без привязки к устройству")

        self.owner.mqtt_client.publish(
            self.discovery_topic,
            "",
            1,
            False,
        )
