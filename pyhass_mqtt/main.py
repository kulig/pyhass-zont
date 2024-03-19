import typing as t
import paho.mqtt.client as mqtt
from . import models


class Entity:

    def __init__(self, id_: str, model_cls: type) -> None:
        self.node: t.Optional['Node'] = None
        self.model = model_cls()
        self.id = id_
        self.discovery_topic: str | None = None

    def set_node(self, node: t.Optional['Node']) -> None:
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
        Subscribe as:
            self.node.client.subscribe(topic)
            self.node.client.message_callback_add(topic, on_msg)
        Message handler like:
            def on_msg(client: mqtt.Client, userdata: t.Any, message: mqtt.MQTTMessage) -> None
        """
        if self.node is None:
            raise RuntimeError('Cannot subscribe entity without node')

    def unsubscribe(self) -> None:
        """
        Unsubscribe as:
            self.node.client.message_callback_remove(topic)
            self.node.client.unsubscribe(topic)
        """
        if self.node is None:
            raise RuntimeError('Cannot unsubscribe entity without node')

    def get_state(self) -> str:
        raise NotImplementedError('get_state')

    def publish_state(self) -> None:
        if self.node is None:
            raise RuntimeError('Cannot publish state of entity without node')
        self.node.client.publish(
            self.model.state_topic,
            self.get_state().encode(self.model.encoding),
            self.model.qos,
            self.model.retain
        )

    def publish_discovery(self) -> None:
        if self.node is None:
            raise RuntimeError('Cannot publish discovery of entity without node')
        self.node.client.publish(
            self.discovery_topic,
            self.model.json(exclude_none=True, exclude='discovery_class_'),
            1,
            False
        )

    def unpublish_discovery(self) -> None:
        if self.node is None:
            raise RuntimeError('Cannot un-publish discovery of entity without node')
        self.node.client.publish(self.discovery_topic, '', 1, False)


class Node:

    def __init__(self, id_: str, client: mqtt.Client, device: models.Device | None = None,
                 discovery_prefix: str = 'homeassistant') -> None:
        self.client: mqtt.Client = client
        self.id = id_
        self.device = device
        if self.device.identifiers is None:
            self.device.identifiers = [self.id]
        self.discovery_prefix = discovery_prefix
        self.entities = {}

    def add_entity(self, obj: Entity) -> None:
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
        if isinstance(obj, str):
            obj = self.entities[obj]
        obj.unpublish_discovery()
        obj.unsubscribe()
        obj.set_node(None)
        del self.entities[obj.unique_id]

    def publish_state(self) -> None:
        for obj in self.entities.values():
            obj.publish_state()

    def publish_discovery(self) -> None:
        for obj in self.entities.values():
            obj.publish_discovery()

    def unpublish_discovery(self) -> None:
        for obj in self.entities.values():
            obj.unpublish_discovery()

    def subscribe(self) -> None:
        for obj in self.entities.values():
            obj.subscribe()

    def unsubscribe(self) -> None:
        for obj in self.entities.values():
            obj.unsubscribe()
