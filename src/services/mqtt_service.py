import time


import paho.mqtt.client as mqtt
from logger import LOGGER


class MqttClient:
    def __init__(self,
                 host: str,
                 port: int,
                 qos: int,
                 username: str,
                 password: str):
        self.host = host
        self.port = port
        self.qos = qos
        self.username = username
        self.password = password

        self.mqtt_client = None
        self.subscribed_topics = []

    def start(self):
        self.mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, clean_session=True)

        def on_connect(client, userdata, flags, rc):
            print(f"Connected with result code {rc}")
            for topic in self.subscribed_topics:
                client.subscribe(topic, qos=self.qos)

        def on_message(client, userdata, msg):
            print(f"Received message '{msg.payload.decode()}' on topic '{msg.topic}' with QoS {msg.qos}")
            # TODO: Add message processing logic here

        self.mqtt_client.on_connect = on_connect
        self.mqtt_client.on_message = on_message

        self.mqtt_client.username_pw_set(self.username, self.password)
        self.connect()

        LOGGER.info(f"MQTT client started with host '{self.host}' and port '{self.port}'")
        self.mqtt_client.loop_forever()

    def connect(self):
        try:
            self.mqtt_client.connect(self.host, port=self.port)
        except Exception as e:
            LOGGER.debug("Could not connect to MQTT broker, retry in 2 seconds: {}".format(e))
            time.sleep(2)
            self.connect()

    def _subscribe_to_topics(self):
        topic_list = [
            f'katara/status/#',
            f'katara/clients/solenoid/#'
        ]

        for topic in topic_list:
            self.mqtt_client.subscribe(topic, qos=self.qos)
            self.subscribed_topics.append(topic)
            LOGGER.info(f"Subscribed to topic '{topic}'")

    