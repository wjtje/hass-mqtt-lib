from __future__ import annotations
from typing_extensions import NotRequired, TypedDict
from .node import Connection
import json


class SensorConfig(TypedDict):
    device_class: NotRequired[str]
    entity_category: NotRequired[str]
    expire_after: NotRequired[int]
    icon: NotRequired[int]
    json_attributes_template: NotRequired[str]
    json_attributes_topic: NotRequired[str]
    name: NotRequired[str]
    state_class: NotRequired[str]
    unit_of_measurement: NotRequired[str]


class Sensor():
    def __init__(self, connection: Connection, id: str, config: SensorConfig = {}) -> None:
        # Short reference to Connection class
        self._c = connection
        self._mc = self._c._mqtt_client
        self._ft = self._c.format_topic

        # Sensor data
        self._id = id
        self._config = config

        # Send discovery
        self._c.publish_on_connect(self._ft("sensor", self._id, "config"), json.dumps({
            **self._config,
            'device': self._c._device,
            'availability': {'topic': self._ft("sensor", "available", "state"), },
            'state_topic': self._ft("sensor", self._id, "state"),
            'unique_id': f"{self._c._id}-{self._id}",
        }), retain=True)

    def update(self, value) -> None:
        self._mc.publish(self._ft("sensor", self._id, "state"), value)
