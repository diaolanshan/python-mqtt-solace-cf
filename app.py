from flask import Flask
import os
import json
from solace_mqtt import MQTTClient

app = Flask(__name__)
app.config.from_object(__name__)

port = int(os.getenv('VCAP_APP_PORT', 8080))

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


@app.route('/mqtt/solace/publish', methods=['GET', 'POST'])
def publish_message():
    client = MQTTClient(mqtt_host=mqtt_host, mqtt_port=mqtt_port, mqtt_user=client_username, mqtt_pass=client_password)
    client.send_message("I am a test message")
    return "OK", 200


@app.route('/mqtt/solace/subscribe', methods=['GET', 'POST'])
def subscribe_message():
    client = MQTTClient(mqtt_host=mqtt_host, mqtt_port=mqtt_port, mqtt_user=client_username, mqtt_pass=client_password)
    client.subscribe_message()
    return "OK", 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=False)
