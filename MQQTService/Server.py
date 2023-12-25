import random
import time
import os
import sys
import django
import paho.mqtt.client as mqttClient
from pathlib import Path

# ------------------------------------define django setting to access project model-------------------------------------
base_dir = os.getcwd()
project_path = Path(base_dir).parent
sys.path.append(f"{project_path}")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Aragon.settings")
django.setup()
# ----------------------------------------------------------------------------------------------------------------------
# from SayalSanjesh.models import WaterMeters

# ------------------------------------------------get meters serial-----------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------

Connected = False


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to broker")
        global Connected
        Connected = True
    else:
        print("Connection failed")

def on_message(client, userdata, message):
    print(f"{message.topic}")
    print("Message received: " + message.payload.decode("utf-8"))


broker = '136.243.210.26'
port = 1883
topic = "test"
# topic = meter_topics

client_id = f'python-mqtt-{random.randint(0, 1000)}'
# user = "test"
# password = "sayal@mqtt"

user = "mark"
password = "1234"

client = mqttClient.Client("Python")
client.username_pw_set(user, password=password)
client.on_connect = on_connect
client.on_message = on_message

client.connect(broker, port=port)

client.loop_start()

while Connected != True:
    time.sleep(0.1)

client.subscribe(topic)

try:
    while True:
        time.sleep(1)

except KeyboardInterrupt:
    print("exiting")
    client.disconnect()
    client.loop_stop()