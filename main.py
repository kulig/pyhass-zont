from threading import Thread

import paho.mqtt.client as mqtt

import config
from src.nodes import setup_electric_boiler


def main() -> None:
    client = mqtt.Client(
        callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
        client_id="TEST_NODE",
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

    process = Thread(target=setup_electric_boiler, kwargs={"uid": "TEST_NODE", "mqtt_client": client})
    process.start()


if __name__ == "__main__":
    main()
