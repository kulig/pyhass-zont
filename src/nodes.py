import time

import paho.mqtt.client as mqtt

from src import config
from src.entity.collection import EntityThermoSensorDummy
from src.entity.models import ThermoSensorDummyModel
from src.node.collection import ElectricBoilerNode
from src.node.models import ElectricBoilerModel


def setup_electric_boiler(
    uid: str,
    mqtt_client: mqtt.Client,
) -> None:
    node = ElectricBoilerNode(
        uid=uid,
        mqtt_client=mqtt_client,
        discovery_prefix="homeassistant",
        model=ElectricBoilerModel(
            manufacturer="Protherm",
            name="Электрокотел",
            model="13 r2",
            sw_version="0.0.1",
        ),
    )
    thermo_sensor = EntityThermoSensorDummy(
        uid="boiler_temp",
        model=ThermoSensorDummyModel(),
    )
    node.bind_entity(entity=thermo_sensor)
    while True:
        time.sleep(5)
        node.publish_state_all()
