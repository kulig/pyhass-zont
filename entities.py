from pyhass_mqtt import *
import paho.mqtt.client as mqtt
import typing as t
import random


class TemperatureSensor(Entity):

    def __init__(self, id_: str) -> None:
        super().__init__(id_, model_cls=models.Sensor)
        self.model.name = f'Dummy thermosensor from python {id_}'
        self.model.expire_after = 600
        self.model.device_class = enums.SensorDeviceClass.temperature
        self.model.suggested_display_precision = 1

    def get_state(self) -> str:
        return str(random.randrange(-300, +700) / 10)


class Relay(Entity):

    def __init__(self, id_: str) -> None:
        super().__init__(id_, model_cls=models.Switch)
        self.model.name = f'Dummy relay "{id_}"'
        self.model.optimistic = False   # это значит, что HA после отправки команды должен дождаться подтверждения от нас
        self.model.payload_off = 'OFF'  # это HA будет слать в командный топик, чтобы нас выключить
        self.model.payload_on = 'ON'    # это HA будет слать в командный топик, чтобы нас включить
        self.model.state_off = 'OFF'    # это мы пишем в топик состояния, когда выключаемся
        self.model.state_on = 'ON'      # это мы пишем в топик состояния, когда включаемся
        self.state = False              # это типа наше реле

    def get_state(self) -> str:
        return self.model.state_on if self.state else self.model.state_off

    def set_node(self, node: t.Optional['Node']) -> None:
        '''
        Перекроем метод, в котором устанавливается нода, чтобы сгененрировать командный топик.
        Можно вообще сделать суперуникальный командный топик и просто прописать его в модель в конструкторе.
        Но это как-то не кузяво.
        Метод set_node() дохуя важный и в перекрытом коде надо обязательно вызвать родительский
        '''
        super().set_node(node)
        if node:
            self.model.command_topic = f'{node.id}/{self.id}/command'
        else:
            self.model.command_topic = None

    def on_set_command(self, client: mqtt.Client, userdata: t.Any, msg: mqtt.MQTTMessage) -> None:
        '''
        Это собственнно обработчик сообщений в командном топике.
        Нас, собственно, интересует только аргумент msg. Он содержит все сообщение: топик, содержимое, хуе-мое.
        И топик, и содержимое - bytes! не str! Так что не забываем decode()
        '''
        # декодируем содержимое сообщения из bytes в str
        payload = msg.payload.decode(self.model.encoding)
        # радостно срем в консоль
        print(f'{self.model.name} got message "{payload}"')
        # Меняем свое унутреннее состояние (тут, если бы у нас была настоящая релюшка, я бы ее и переключил)
        self.state = payload == self.model.payload_on
        # Надо известить о своем новом состоянии
        self.publish_state()

    def subscribe(self) -> None:
        '''
        Это охуенно важный метод. В нем мы подписываемся на свой командный топик.
        Этот метод вызывается только нодой и она во время его выполнения гарантировано определена
        '''
        # Дернули папский метод (там тупо проверка)
        super().subscribe()
        # Сказали MQTT-клиенту, что желаем подписаться вот на этот топик
        self.node.client.subscribe(self.model.command_topic)
        # Сказали MQTT-клиенту, что, сука, не просто так подписались, а чтобы он коллбек дернул по факту сообщения
        self.node.client.message_callback_add(self.model.command_topic, self.on_set_command)

    def unsubscribe(self) -> None:
        '''
        Здесь иы отписывааемся к ебаной матери от всех топиков, на которые имели подписку.
        Подписался - отпишись.
        Метод, как и subscribe(), вызывается только нодой, не вручную.
        '''
        super().unsubscribe()
        self.node.client.message_callback_remove(self.model.command_topic)
        self.node.client.unsubscribe(self.model.command_topic)
