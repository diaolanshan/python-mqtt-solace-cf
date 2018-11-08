A *Python* app which target to demo how to use MQTT to connect to a solace instance in the cloud foundry platform.

The app use the paho lib, so add [paho-mqtt](https://github.com/eclipse/paho.mqtt.python) in your *requirements.txt*

**How to use it:**

- Download and push the app to the cloud foundry platform.
- Provision and solace instance and bind to the app.
- Restart/Restage the app.

**How to test it:**

The app contains to url,

- http://{link_to_app}/mqtt/solace/subscribe add a new subscriber to the topic: _python_mqtt_topic_example_
- http://{link_to_app}/mqtt/solace/subscribe publish a message to the topic: _python_mqtt_topic_example_

and check the app log and the connections in the soladmin/gui to verify.
 
To get the technical information which can be used to setup the connection:

```python
    vcap_services = json.loads(os.environ['VCAP_SERVICES'])
    for service in vcap_services.keys():
        if 'solace-pubsub' in vcap_services[service][0]['tags']:
            # Use the first 'solace' service just in case more than one solace are been binded to this app.
            mqtt_uris = vcap_services[service][0]['credentials']['mqttUris'][0]  # format is tcp://ip_address:port
            mqtt_host = mqtt_uris[6:].split(":")[0]
            mqtt_port = mqtt_uris[6:].split(":")[1]
            client_username = vcap_services[service][0]['credentials']['clientUsername']
            client_password = vcap_services[service][0]['credentials']['clientPassword']
            break
```

Add a subscriber to the topic:
```python
    def subscribe_message(self):
        self.mqttc.connect(self.mqtt_host, int(self.mqtt_port), 60)
        self.mqttc.loop_start()  # start a new network trafic thread

        while self.Connected != True:  # Wait for connection
            print("Not connected.")
            time.sleep(0.5)

        (rc, mid) = self.mqttc.subscribe(self.mqtt_topic, qos=1)
```

Publish a message to solace:
```python
    def send_message(self, message):
        self.mqttc.connect(self.mqtt_host, int(self.mqtt_port), 60)
        self.mqttc.loop_start()  # start a new network trafic thread

        while self.Connected != True:  # Wait for connection
            time.sleep(0.5)

        (rc, mid) = self.mqttc.publish(topic=self.mqtt_topic, payload=str(message), retain=True)

        self.mqttc.disconnect()
        self.mqttc.loop_stop()
```