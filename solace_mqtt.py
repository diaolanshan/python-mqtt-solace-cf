import paho.mqtt.client as mqtt
import time


class MQTTClient():
    def __init__(self, mqtt_host, mqtt_port, mqtt_user, mqtt_pass):
        self.mqttc = mqtt.Client()
        self.mqtt_host = mqtt_host
        self.mqtt_port = mqtt_port
        self.Connected = False

        self.mqttc.on_message = self.on_message
        self.mqttc.on_connect = self.on_connect
        self.mqttc.on_publish = self.on_publish
        self.mqttc.on_subscribe = self.on_subscribe
        self.mqttc.on_disconnect = self.on_disconnect

        self.mqttc.username_pw_set(mqtt_user, mqtt_pass)
        self.mqtt_topic = 'python_mqtt_topic_example'

    # Called when the broker responds to our connection request.
    def on_connect(self, mqttc, obj, flags, rc):
        if rc == 0:
            print("Connected to broker")
            self.Connected = True  # Signal connection
        else:
            print("Connection failed")

    def on_disconnect(self, mqttc, userdata, rc):
        self.Connected = False
        if rc != 0:
            print("Unexpected disconnection.")
        else:
            print("Connection closed")

    # Called when a message has been received on a topic that the client subscribes to and the message does not match
    # an existing topic filter callback
    def on_message(self, mqttc, obj, msg):
        print("Get message from topic: %s, qos of the message is %s and message body is: %s".format(msg.topic,
                                                                                                    str(msg.qos),
                                                                                                    str(msg.payload)))

    # Called when a message that was to be sent using the publish() call has completed transmission to the broker
    def on_publish(self, mqttc, obj, mid):
        print("Publish finished with mid = " + str(mid))

    # Called when the broker responds to a subscribe request. The mid variable matches the mid variable returned from the
    # corresponding subscribe() call
    def on_subscribe(self, mqttc, obj, mid, granted_qos):
        print("Subscribed: " + str(mid) + " " + str(granted_qos))

    def send_message(self, message):
        self.mqttc.connect(self.mqtt_host, int(self.mqtt_port), 60)
        self.mqttc.loop_start()  # start a new network trafic thread

        while self.Connected != True:  # Wait for connection
            time.sleep(0.5)

        (rc, mid) = self.mqttc.publish(topic=self.mqtt_topic, payload=str(message), retain=True)

        self.mqttc.disconnect()
        self.mqttc.loop_stop()

    def subscribe_message(self):
        self.mqttc.connect(self.mqtt_host, int(self.mqtt_port), 60)
        self.mqttc.loop_start()  # start a new network trafic thread

        while self.Connected != True:  # Wait for connection
            print("Not connected.")
            time.sleep(0.5)

        (rc, mid) = self.mqttc.subscribe(self.mqtt_topic, qos=1)
