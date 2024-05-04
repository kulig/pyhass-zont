import time
import paho.mqtt.client as mqtt

from pyhass_mqtt.objects import Device
from pyhass_mqtt.entities import models

import config
import entities


def init_device(id_: str) -> Device:
    # Создаем экземпляр MQTT-клиента
    client = mqtt.Client(
        callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
        client_id=id_,
        clean_session=False,
        reconnect_on_failure=True,
    )
    # Подключаемся к MQTT и запускаем thread с внутренним циклом MQTT-клиента
    client.username_pw_set(config.MQTT_USER, config.MQTT_PASSWD)
    client.connect(
        host=config.MQTT_HOST,
        port=config.MQTT_PORT,
    )
    client.loop_start()

    # Создаем собственно устройство
    return Device(
        id_=id_,
        mqtt_client=client,
        device_model=models.DeviceModel(
            manufacturer=config.NODE_DEVICE_MANUFACTURER,
            name=config.NODE_DEVICE_NAME,
            model=config.NODE_DEVICE_MODEL,
            sw_version='0.0.1'
        )
    )


def main() -> None:
    node = init_device('TEST_NODE')

    boiler_temp = entities.TemperatureSensor('boiler_temp')
    boiler_temp.model.icon = 'mdi:thermometer-water'
    boiler_temp.model.name = 'Температура бойлера'
    node.add_entity(boiler_temp)

    home_temp = entities.TemperatureSensor('home_temp')
    home_temp.model.icon = 'mdi:home-thermometer-outline'
    home_temp.model.name = 'Температура в доме'
    node.add_entity(home_temp)

    outdoor_temp = entities.TemperatureSensor('outdoor_temp')
    outdoor_temp.model.icon = 'mdi:sun-thermometer'
    outdoor_temp.model.name = 'Уличная температура'
    node.add_entity(outdoor_temp)

    gate = entities.Relay('gate_switch')
    gate.model.icon = 'mdi:boom-gate-up'
    gate.model.name = 'Ворота'
    node.add_entity(gate)

    street_lamp = entities.Relay('street_lamp')
    street_lamp.model.icon = 'mdi:outdoor-lamp'
    street_lamp.model.name = 'Уличное освещение'
    node.add_entity(street_lamp)

    while (True):
        time.sleep(5)
        boiler_temp.publish_state()
        home_temp.publish_state()
        outdoor_temp.publish_state()


if __name__ == '__main__':
    main()
