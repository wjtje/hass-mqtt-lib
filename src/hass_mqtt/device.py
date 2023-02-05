from __future__ import annotations
from typing import Union
from typing_extensions import NotRequired, TypedDict


class Device(TypedDict):
    """Device information, see: https://www.home-assistant.io/integrations/sensor.mqtt/#device"""
    configuration_url: NotRequired[str]
    """A link to the webpage that can manage the configuration of this device. Can be either an HTTP or HTTPS link."""
    hw_version: NotRequired[str]
    """The hardware version of the device."""
    identifiers: NotRequired[Union[str, list[str]]]
    """A list of IDs that uniquely identify the device. For example a serial number."""
    manufacturer: NotRequired[str]
    """The manufacturer of the device."""
    model: NotRequired[str]
    """The model of the device."""
    name: NotRequired[str]
    """The name of the device."""
    suggested_area: NotRequired[str]
    """Suggest an area if the device isn’t in one yet."""
    sw_version: NotRequired[str]
    """The firmware version of the device."""
    via_device: NotRequired[str]
    """Identifier of a device that routes messages between this device and Home Assistant. Examples of such devices are hubs, or parent devices of a sub-device. This is used to show device topology in Home Assistant."""
