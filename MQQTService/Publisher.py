import time
import uuid
import paho.mqtt.client as mqtt
from termcolor import colored
import json
import time


class Publisher:

    def __init__(self, client_id=None, name='MQTT publisher client'):
        self.client_id = client_id
        self.name = name
        self.username = None
        self.password = None
        self.host = ''
        self.port = 1883
        self.connected = False

        if client_id is None:
            self.client_id = uuid.uuid1()

        self.client = mqtt.Client(client_id=str(self.client_id))
        self.client.on_connect = self.on_connect

    def set_username_password(self, username, password):
        self.username = username
        self.password = password

    def on_connect(self, client, user_data, flags, rc):
        if rc == 0:
            print(colored('connected OK', 'green'))
            self.connected = True
        else:
            self.connected = False
            if rc == 1:
                error = 'Connection refused – incorrect protocol version'
            elif rc == 2:
                error = 'Connection refused – invalid client identifier'
            elif rc == 3:
                error = 'Connection refused – server unavailable'
            elif rc == 4:
                error = 'Connection refused – bad username or password'
            elif rc == 5:
                error = 'Connection refused – not authorised'
            else:
                error = 'Currently unused'
            print(colored("connection failure with code {}: {}"
                          .format(rc, error), 'red'))

    def on_disconnect(self, client, user_data, rc):
        self.connected = False
        print(colored("disconnected with result code {0}".format(str(rc)), 'red'))
        # self.connect(host=self.host, port=self.port)

    def connect(self, host, port=1883, keep_alive=60):
        self.host = host
        self.port = port
        self.client.username_pw_set(username=self.username, password=self.password)
        self.client.connect(host=host, port=port, keepalive=keep_alive)
        self.client.loop_start()
        time.sleep(1)

    def publish(self, topic, message, qos=0, retain=False):
        # print(self.client.is_connected())
        if self.connected:
            print(colored('publishing message "{}" on topic "{}"'
                          .format(message, topic)))
            self.client.publish(topic=topic, payload=message, qos=qos, retain=retain)
        else:
            print(colored('client not connected to broker. can not publish the message!', 'red'))


def publish_message_to_client(data=None, topic='/status'):
    host = '136.243.210.26'
    port = 1883
    username = "mark"
    password = "1234"

    p = Publisher()
    p.set_username_password(username=username, password=password)
    p.connect(host=host, port=port)
    message = json.dumps(data)
    p.publish(topic=topic, message=message)
    time.sleep(0.01)



# data = {
#     "serial": "001",
#     "type_name": "Switch",
#     "state": False,
# }
# publish_message_to_client(data=data)