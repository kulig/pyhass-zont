import dotenv
import os


dotenv.load_dotenv(".env")


MQTT_HOST: str = os.getenv("MQTT_HOST", "192.168.1.131")
MQTT_PORT: int = int(os.getenv("MQTT_PORT", 1883))
MQTT_USER: str = os.getenv("MQTT_USER", "node")
MQTT_PASSWD: str = os.getenv("MQTT_PASSWD", "node")

NODE_DEVICE_MANUFACTURER: str = os.getenv("NODE_DEVICE_MANUFACTURER", "MANUFACTURER")
NODE_DEVICE_MODEL: str = os.getenv("NODE_DEVICE_MODEL", "MODEL")
NODE_DEVICE_NAME: str = os.getenv("NODE_DEVICE_NAME", "DEVICE")
