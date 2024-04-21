import os
import time
import schedule
from datetime import datetime, timedelta
from pytz import utc
from Devices.models import Devices
from Authorization.models.users import Users
from MQQTService.Publisher import publish_message_to_client

BASE_DIR = os.getcwd()
SCHEDULER_DIR = os.path.join(BASE_DIR, 'scheduler')
LOGS_DIR = os.path.join(SCHEDULER_DIR, 'Log')
LOG_FILE = 'task_log.txt'


def create_log_file():
    if not os.path.exists(LOGS_DIR):
        os.makedirs(LOGS_DIR)
    if not os.path.exists(os.path.join(LOGS_DIR, LOG_FILE)):
        with open(os.path.join(LOGS_DIR, LOG_FILE), 'w') as file:
            file.write("Task Log:\n")


def write_to_log(message):
    with open(os.path.join(LOGS_DIR, LOG_FILE), 'a') as file:
        file.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} : {message}\n")


def my_task():
    current_time = datetime.now().replace(tzinfo=utc)
    # Your task code here
    # get all devices
    all_devices = Devices.objects.filter(state=True).exclude(start_time=None)
    for device in all_devices:
        device_user_time = device.user.time_duration
        device_start_time = device.start_time.replace(tzinfo=utc)
        valid_time = device_start_time + timedelta(minutes=device_user_time)
        if current_time > valid_time:
            # set time to off user time to 0 and publish message to turnoff device
            device_obj = Devices.objects.get(serial = device.serial)
            device_obj.state = False
            device_obj.start_time = None
            device_obj.save()
            user_id = device.user.id
            user_obj = Users.objects.get(id=user_id)
            user_obj.time_duration = 0
            user_obj.save()
            prepared_data = {
                "serial": device.serial,
                "type_name": device.type.name,
                "state": False,
            }
            publish_message_to_client(data=prepared_data)
            time_delta = int((current_time - valid_time).total_seconds() / 60)
            message = (f"device : {device.serial} - valid_time is : {valid_time} , current_time is : {current_time} , "
                       f"device_usage_time : {time_delta}")
            write_to_log(message)


create_log_file()
schedule.every(1).seconds.do(my_task)
while True:
    schedule.run_pending()
    time.sleep(1)
