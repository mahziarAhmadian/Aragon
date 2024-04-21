import json
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
from Devices.models import Devices
from Authorization.models import Users


# ------------------------------------------------add to data base -----------------------------------------------------
def add_data_to_databse(data):
    serial = data.get('serial', None)
    type_name = data.get('type_name', None)
    state = data.get('state', None)
    restart = data.get('Restart', None)
    time_over = data.get('time_over', None)

    if serial is not None and type_name is not None and state is not None:
        # get device object
        device_object = Devices.objects.filter(serial=serial, type__name=type_name)
        if len(device_object) == 1:
            if restart is not None and restart is True:
                update_device = device_object.update(state=False, start_time=None)
                print("update_device", update_device)
            elif time_over is not None and time_over is True:
                device_object.update(state=False, start_time=None)
                # set user time to 0time_duration
                for device_obj in device_object:
                    user_id = device_obj.user.id
                    user_obj = Users.objects.get(id=user_id)
                    user_obj.time_duration = 0
                    user_obj.save()
            else:
                device_object.update(state=state)


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
    print(f'message is : {message.payload.decode("utf-8")}')
    json_data = json.loads(message.payload.decode("utf-8"))
    print(f"Message received: {json_data}")
    add_data_to_databse(data=json_data)
    # print("json_data: " + json_data)


broker = '136.243.210.26'
port = 1883
topic = "/status/response"
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
