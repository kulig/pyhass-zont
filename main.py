import time

from pyhass_mqtt import *
import paho.mqtt.client as mqtt
import config
import entities


def init_node(id_: str) -> Node:
    # Создаем экземпляр MQTT-клиента
    client = mqtt.Client(
        callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
        client_id=id_,
        clean_session=False,
        reconnect_on_failure=True,
    )
    # Создаем собственно node
    res = Node(
        id_=id_,
        client=client,
        device=models.Device(
            manufacturer=config.NODE_DEVICE_MANUFACTURER,
            name=config.NODE_DEVICE_NAME,
            model=config.NODE_DEVICE_MODEL,
            sw_version='0.0.1'
        )
    )
    # Подключаемся к MQTT и запускаем thread с внутренним циклом MQTT-клиента
    client.username_pw_set(config.MQTT_USER, config.MQTT_PASSWD)
    client.connect(
        host=config.MQTT_HOST,
        port=config.MQTT_PORT,
    )
    client.loop_start()

    return res


def main() -> None:
    node = init_node('TEST_NODE')
    sensor1 = entities.ThermoSensor('temp1')
    sensor2 = entities.ThermoSensor('temp2')
    node.add_entity(sensor1)
    node.add_entity(sensor2)
    node.add_entity(entities.Relay('relay1'))
    node.add_entity(entities.Relay('relay2'))

    while (True):
        time.sleep(5)
        sensor1.publish_state()
        sensor2.publish_state()


if __name__ == '__main__':
    main()
