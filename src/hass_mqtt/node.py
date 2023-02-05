import paho.mqtt.client as mqtt
from .device import Device


class Connection:
    def __init__(self, id: str, discovery_topic: str = "homeassistant", device: Device = {}) -> None:
        """Initialize a new Node that communication to home assistant.

        Args:
            id (str): A uniqe id for this node
            discovery_topic (str, optional): The mqtt topic prefix. Defaults to "homeassistant".
        """
        self._mqtt_client = mqtt.Client()
        self._id = id
        self._discovery_topic = discovery_topic
        self._connected = False
        self._device = device
        self._publish_on_connect: list[tuple[str, str, bool]] = []

        self._mqtt_client.on_connect = self.__on_connect
        self._mqtt_client.on_disconnect = self.__on_disconnect
        self._mqtt_client.on_message = self.__on_message

    def connect(self, host: str, port: int = 1883, username: str = "", password: str = "") -> None:
        """Connect to node to Home Assistant using mqtt.

        Args:
            host (str): The mqtt host
            port (int, optional): The mqtt port. Defaults to 1883.
            username (str, optional): The mqtt username. Defaults to "".
            password (str, optional): The mqtt password. Defaults to "".
        """
        if username != "" and password == "":
            self._mqtt_client.username_pw_set(username)
        if username != "" and password != "":
            self._mqtt_client.username_pw_set(username, password)

        self._mqtt_client.will_set(
            self.format_topic("sensor", "available", "state"), "offline", retain=True)

        self._mqtt_client.connect(host, port, keepalive=60)
        self._mqtt_client.loop_start()

    def __on_connect(self, client: mqtt.Client, userdata, flags, rc: int) -> None:
        print("Connected to MQTT Broker")
        self._connected = True

        # Send all the message
        for message in self._publish_on_connect:
            self._mqtt_client.publish(
                message[0], message[1], retain=message[2])

        self._mqtt_client.publish(
            self.format_topic("sensor", "available", "state"), "online", retain=True)

    def __on_disconnect(self, client: mqtt.Client, userdata, rc: int) -> None:
        print("Disconnect to MQTT Broker")
        self._connected = False

    def __on_message(self, client: mqtt.Client, userdata, message: mqtt.MQTTMessage) -> None:
        pass

    def format_topic(self, component: str, object_id: str, type: str) -> str:
        """Formats a component and object_id into a valid mqtt topic.

        Args:
            component (str): The component type e.g., sensor.
            object_id (str): A unique id for the sensor.
            type (str): The type of message you want to send e.g., state / config / etc.

        Returns:
            str: A valid mqtt topic.
        """
        return f"{self._discovery_topic}/{component}/{self._id}/{object_id}/{type}"

    def publish_on_connect(self, topic: str, payload, retain: bool = False) -> None:
        """Send a message when the connection to the mqtt broker has been made.

        Args:
            topic (str): The topic of the message
            payload (): The payload of the message
            retain (bool, optional): Defaults to False.
        """
        self._publish_on_connect.append((topic, payload, retain))
