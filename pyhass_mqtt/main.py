import typing as t
import paho.mqtt.client as mqtt
from . import models


class Entity:
    """
    Базовый класс для определения MQTT-сущностей, которые понимаются Home Assistant.
    https://www.home-assistant.io/integrations/mqtt/
    """
    def __init__(self, id_: str, model_cls: type) -> None:
        """
        :param id_: Строка, содержащая уникальный идентификатор сущности в рамках Node.
        :param model_cls: Класс (фабрика) модели сущности. См. pyhass_mqtt.models или
                          https://www.home-assistant.io/integrations/mqtt/
        """
        self.node: t.Optional['Node'] = None
        self.model = model_cls()
        self.id = id_
        self.discovery_topic: str | None = None

    def set_node(self, node: t.Optional['Node']) -> None:
        """
        В этом методе устанавливается node, владеющая данной сущностью.
        В наследниках этого класса следует переопределять этот метод для вычисления имен топиков и прочего,
        зависящего от ноды или ее имени. При переопределении обязательно сначала вызвать родительскую реализацию метода.

        :param node: Экземпляр класса Node или None
        """
        self.node = node
        if node is not None:
            self.model.object_id = self.model.unique_id = f'{node.id}_{self.id}'
            self.model.state_topic = f'{node.id}/{self.id}/state'
            self.model.device = node.device
            self.discovery_topic = f'{node.discovery_prefix}/{self.model.discovery_class_}/{node.id}/{self.id}/config'
        else:
            self.model.unique_id = None
            self.model.object_id = None
            self.model.state_topic = None
            self.model.device = None
            self.discovery_topic = None

    def subscribe(self) -> None:
        """
        Этот метод вызывается нодой, чтобы данная сущность подписалась на все интересующие ее топики.
        В наследниках этого класса при переопределении сначала желательно вызвать родительскую реализацию.

        Чтобы подписаться, используем:
            self.node.client.subscribe(topic)
            self.node.client.message_callback_add(topic, on_msg)
        Обработчик должен быть таким:
            def on_msg(client: mqtt.Client, userdata: t.Any, message: mqtt.MQTTMessage) -> None
        """
        if self.node is None:
            raise RuntimeError('Cannot subscribe entity without node')

    def unsubscribe(self) -> None:
        """
        Этот метод вызывается нодой, чтобы сущность отписалась от всех топиков, на которые была подписана.
        В наследниках этого класса при переопределении сначала желательно вызвать родительскую реализацию.

        Чтобы отписаться, используем:
            self.node.client.message_callback_remove(topic)
            self.node.client.unsubscribe(topic)
        """
        if self.node is None:
            raise RuntimeError('Cannot unsubscribe entity without node')

    def get_state(self) -> str:
        """
        Этот метод обязателен к переопределению в наследниках класса.

        :return: Текущее состояние (state) сущности.
        """
        raise NotImplementedError('get_state')

    def publish_state(self) -> None:
        """
        При вызове этого метода, сущность опубликует в своем state_topic свое состояние (см. get_state())
        """
        if self.node is None:
            raise RuntimeError('Cannot publish state of entity without node')
        self.node.client.publish(
            self.model.state_topic,
            self.get_state().encode(self.model.encoding),
            self.model.qos,
            self.model.retain
        )

    def publish_discovery(self) -> None:
        """
        Этот метод публикует MQTT discovery JSON для Home Assistant в соответствующем топике.
        Метод вызывается нодой.
        Для генерации discovery JSON используется экземпляр модели сущности (см. конструктор)
        """
        if self.node is None:
            raise RuntimeError('Cannot publish discovery of entity without node')
        self.node.client.publish(self.discovery_topic, self.model.discovery_json(), 1, False)

    def unpublish_discovery(self) -> None:
        """
        Этот метод публикует пустую строку для Home Assistant в топике для MQTT discovery.
        Метод вызывается нодой.
        """
        if self.node is None:
            raise RuntimeError('Cannot un-publish discovery of entity without node')
        self.node.client.publish(self.discovery_topic, '', 1, False)


class Node:
    """
    Класс, воплощающий Home Assistant MQTT device.
    """
    def __init__(self, id_: str, client: mqtt.Client, device: models.Device | None = None,
                 discovery_prefix: str = 'homeassistant') -> None:
        """
        :param id_: Уникальный идентификатор ноды, используется для генерации object_id и топиков
        :param client: MQTT-клиент, экземпляр paho.mqtt.client.Client
        :param device: Модель, описывающая устройство для Home Assistant. Для всех сущностей этой ноды
                       поле device в discovery JSON будет равно этой модели
        :param discovery_prefix: Префикс для discovery топиков в Home Assistant
        """
        self.client: mqtt.Client = client
        self.id = id_
        self.device = device
        if self.device.identifiers is None:
            self.device.identifiers = [self.id]
        self.discovery_prefix = discovery_prefix
        self.entities = {}

    def add_entity(self, obj: Entity) -> None:
        """
        Добавить сущность в ноду.

        :param obj: Экземпляр класса, отнаследованного от Entity
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

    def remove_entity(self, obj: str | Entity) -> None:
        """
        Удалить сущность из ноды

        :param obj: Строка с id сущности или сама сущность
        """
        if isinstance(obj, str):
            obj = self.entities[obj]
        obj.unpublish_discovery()
        obj.unsubscribe()
        obj.set_node(None)
        del self.entities[obj.unique_id]

    def publish_state_all(self) -> None:
        for obj in self.entities.values():
            obj.publish_state()

    def publish_discovery_all(self) -> None:
        for obj in self.entities.values():
            obj.publish_discovery()

    def unpublish_discovery_all(self) -> None:
        for obj in self.entities.values():
            obj.unpublish_discovery()

    def subscribe_all(self) -> None:
        for obj in self.entities.values():
            obj.subscribe()

    def unsubscribe_all(self) -> None:
        for obj in self.entities.values():
            obj.unsubscribe()
