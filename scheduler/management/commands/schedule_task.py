import os
import time
import schedule
from datetime import datetime

LOGS_DIR = 'logs'
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
    # Your task code here
    write_to_log("Task is run")

create_log_file()
schedule.every(1).seconds.do(my_task)
while True:
    schedule.run_pending()
    time.sleep(1)