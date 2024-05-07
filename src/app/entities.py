from pyhass_mqtt.objects import Entity
from pyhass_mqtt.entities import models, enums
import paho.mqtt.client as mqtt
import typing as t
import random


class TemperatureSensor(Entity):
    def __init__(self, uid: str) -> None:
        super().__init__(uid, entity_model=models.SensorModel())
        self.model.name = f"Dummy thermosensor from python {uid}"
        self.model.expire_after = 600
        self.model.device_class = enums.SensorDeviceClass.temperature
        self.model.unit_of_measurement = "C"
        self.model.suggested_display_precision = 1

    def get_state(self) -> str:
        return str(random.randrange(-300, +700) / 10)


class Relay(Entity):
    def __init__(self, uid: str) -> None:
        super().__init__(uid, entity_model=models.SwitchModel())
        self.model.name = f'Dummy relay "{uid}"'
        self.model.optimistic = False  # это значит, что HA после отправки команды должен дождаться подтверждения от нас
        self.model.payload_off = "OFF"  # это HA будет слать в командный топик, чтобы нас выключить
        self.model.payload_on = "ON"  # это HA будет слать в командный топик, чтобы нас включить
        self.model.state_off = "OFF"  # это мы пишем в топик состояния, когда выключаемся
        self.model.state_on = "ON"  # это мы пишем в топик состояния, когда включаемся
        self.state = False  # это типа наше реле

    def get_state(self) -> str:
        return self.model.state_on if self.state else self.model.state_off

    def on_bind(self) -> None:
        self.model.command_topic = f"{self.owner.id}/{self.uid}/command"

    def on_set_command(self, client: mqtt.Client, userdata: t.Any, msg: mqtt.MQTTMessage) -> None:
        """
        Это собственнно обработчик сообщений в командном топике.
        Нас, собственно, интересует только аргумент msg. Он содержит все сообщение: топик, содержимое, хуе-мое.
        И топик, и содержимое - bytes! не str! Так что не забываем decode()
        """
        # декодируем содержимое сообщения из bytes в str
        payload = msg.payload.decode(self.model.encoding)
        # радостно срем в консоль
        print(f'{self.model.name} got message "{payload}"')
        # Меняем свое унутреннее состояние (тут, если бы у нас была настоящая релюшка, я бы ее и переключил)
        self.state = payload == self.model.payload_on
        # Надо известить о своем новом состоянии
        self.publish_state()

    def subscribe(self) -> None:
        """
        Это охуенно важный метод. В нем мы подписываемся на свой командный топик.
        Этот метод вызывается только устройством (self.owner)
        """
        # Дернули папский метод (там тупо проверка)
        super().subscribe()
        # Сказали MQTT-клиенту, что желаем подписаться вот на этот топик
        self.owner.mqtt_client.subscribe(self.model.command_topic)
        # Сказали MQTT-клиенту, что, сука, не просто так подписались, а чтобы он коллбек дернул по факту сообщения
        self.owner.mqtt_client.message_callback_add(self.model.command_topic, self.on_set_command)

    def unsubscribe(self) -> None:
        """
        Здесь иы отписывааемся к ебаной матери от всех топиков, на которые имели подписку.
        Подписался - отпишись.
        Метод, как и subscribe(), вызывается только устройством, не вручную.
        """
        super().unsubscribe()
        self.owner.mqtt_client.message_callback_remove(self.model.command_topic)
        self.owner.mqtt_client.unsubscribe(self.model.command_topic)
