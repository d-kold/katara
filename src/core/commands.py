from services.mqtt_service import MqttClient

from logger import LOGGER

mqtt_client: MqttClient


def switch(message: str):
    topic = f'katara/clients/solenoid/switch'
    mqtt_client.mqtt_client.publish(topic, message, qos=1, retain=True)
    # print(f"Published message '{message}' to topic '{topic}'")
    LOGGER.info(f"Published message '{message}' to topic '{topic}'")
