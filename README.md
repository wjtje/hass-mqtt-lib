# Home Assistant MQTT Python Lib

Easly create python scripts that publish sensor data to home assistant

> This project is still work in progress

## Getting started

First you need to build the python wheel package using `python -m build` (if the module doesn't exsist, run `pip install -r requirements.txt` first). Then you can install the newly build module using `pip install {name}`, look inside the dist folder for the file name.

### Example

```python
import hass_mqtt

# Step 1 - Create a connection
connection = hass_mqtt.Connection('device_id', device={
    name: 'My own device name'
})

# Step 2 - Create sensor (or other components in the future)
my_sensor = hass_mqtt.Sensor(connection, 'sensor_id', {
    name: 'My sensor'
})

# Step 3 - Connect to the mqtt broker
connection.connect('broker_address')

# Step 4 - Publish data
while True:
    my_sensor.publish(68.99) # Real sensor data
```
