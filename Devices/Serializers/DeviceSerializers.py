import threading
from datetime import datetime, timedelta
from Devices.models.devices import Devices, DeviceTypes
from Authorization.models import Admins, Users
from Authorization.TokenManager import user_id_to_token, token_to_user_id
from Devices.Serializers import status_success_result, wrong_token_result, wrong_data_result
from Authorization.Serializers.AdminSerilizer import AdminSerializers
from MQQTService.Publisher import publish_message_to_client


class ThreadHandler:
    def __init__(self):
        self.__alive_device = []
        self.__devices_start_time = {}

    def __real_thread(self, device_serial, time_to_shout_down):
        device_object = Devices.objects.get(serial=device_serial)
        user_id = device_object.user.id
        while True:
            if device_serial in self.__alive_device:
                current_time = datetime.now()
                # print(
                #     f"device_serial : {device_serial} -- current_time : {current_time.strftime('%Y-%m-%d %H:%M:%S')} "
                #     f"-- time_to_shout_down : {time_to_shout_down.strftime('%Y-%m-%d %H:%M:%S')}")
                if current_time.strftime('%Y-%m-%d %H:%M:%S') == time_to_shout_down.strftime('%Y-%m-%d %H:%M:%S'):
                    # publish turn off to mqtt broker
                    prepared_data = {
                        "serial": device_object.serial,
                        "type_name": device_object.type.name,
                        "state": False,
                    }
                    publish_message_to_client(data=prepared_data)
                    Users.objects.filter(id=user_id).update(time_duration=0)
                    self.__alive_device.remove(device_serial)
                    if device_serial in list(self.__devices_start_time.keys()):
                        self.__devices_start_time.pop(device_serial)
                    break
            else:
                break

    def start_thread(self, device_serial):
        device_object = Devices.objects.get(serial=device_serial)
        self.__alive_device.append(device_serial)
        current_time = datetime.now()
        self.__devices_start_time[f'{device_serial}'] = current_time
        user_time_duration = device_object.user.time_duration
        time_to_shout_down = current_time + timedelta(minutes=user_time_duration)
        prepared_data = {
            "serial": device_object.serial,
            "type_name": device_object.type.name,
            "state": True,
        }
        publish_message_to_client(data=prepared_data)
        t = threading.Thread(target=self.__real_thread, args=(device_serial, time_to_shout_down))
        t.start()

    def stop_thread(self, device_serial):
        current_time = datetime.now()
        device_object = Devices.objects.get(serial=device_serial)
        user_id = device_object.user.id
        if device_serial in self.__alive_device:
            self.__alive_device.remove(device_serial)
        if device_serial in list(self.__devices_start_time.keys()):
            user_start_time = self.__devices_start_time[device_serial]
            time_difference = (current_time - user_start_time).total_seconds() / 60
            print(f"current_time : {current_time} -- user_start_time : {user_start_time}")
            print(f"time_difference : {time_difference}")
            if time_difference > 0:
                user_object = Users.objects.filter(id=user_id)
                user_time_duration = list(user_object.values('time_duration'))[0]['time_duration']
                time_delta = user_time_duration - time_difference
                if time_delta > 0:
                    user_object.update(time_duration=time_delta)
                    # publish turn off to mqtt broker
                    prepared_data = {
                        "serial": device_object.serial,
                        "type_name": device_object.type.name,
                        "state": False,
                    }
                    publish_message_to_client(data=prepared_data)
                elif time_delta <= 0:
                    user_object.update(time_duration=0)

        if device_serial not in self.__alive_device and device_serial not in list(self.__devices_start_time.keys()):
            # This state occurs when server is restart
            print("server restarted")
            prepared_data = {
                "serial": device_object.serial,
                "type_name": device_object.type.name,
                "state": False,
            }
            publish_message_to_client(data=prepared_data)


class DeviceSerializers:
    thread_object = ThreadHandler()

    @staticmethod
    def admin_create_serializer(token, name, serial, type_id, other_information):
        token_result = token_to_user_id(token)
        if token_result["status"] == "OK":
            admin_id = token_result["data"]["user_id"]
            if AdminSerializers.admin_check_permission(admin_id, 'Admin'):
                admin_object = Admins.objects.get(id=admin_id)
                if admin_object.is_super_admin is not True:
                    wrong_data_result["message"] = "You do not have the required access"
                    return False, wrong_data_result
                try:
                    type_object = DeviceTypes.objects.get(id=type_id)
                    device = Devices()
                    device.serial = serial
                    device.type = type_object
                    device.name = name
                    device.other_information = other_information
                    device.save()
                    return True, status_success_result
                except:
                    wrong_data_result["message"] = "Invalid data"
                    return False, wrong_data_result
            wrong_data_result["message"] = "You do not have the required access"
            return False, wrong_data_result
        else:
            return False, wrong_token_result

    @staticmethod
    def admin_get_all_serializer(token, name, page, count):
        token_result = token_to_user_id(token)
        if token_result["status"] == "OK":
            admin_id = token_result["data"]["user_id"]
            if AdminSerializers.admin_check_permission(admin_id, 'Admin'):
                admin = Admins.objects.get(id=admin_id)
                print(admin.permissions)
                offset = int((page - 1) * count)
                limit = int(count)
                filters = {
                    "name": name
                }
                filters = {k: v for k, v in filters.items() if v is not None}
                queryset = Devices.objects.filter(**filters).order_by('-create_date')[offset:offset + limit]
                response = Devices.objects.serialize(queryset=queryset)
                return True, response
            else:
                return False, wrong_token_result
        else:
            return False, wrong_token_result

    @staticmethod
    def admin_get_one_serializer(token, serial):
        token_result = token_to_user_id(token)
        if token_result["status"] == "OK":
            admin_id = token_result["data"]["user_id"]
            if AdminSerializers.admin_check_permission(admin_id, 'Admin'):
                admin = Admins.objects.get(id=admin_id)
                try:
                    filters = {
                        "serial": serial
                    }
                    if serial is None:
                        filters['serial'] = ""
                    if 'Staff' in admin.permissions:
                        filters['admin__id'] = admin_id
                    filters = {k: v for k, v in filters.items() if v is not None}
                    queryset = Devices.objects.filter(**filters)
                    response = Devices.objects.serialize(queryset=queryset)
                    return True, response
                except:
                    wrong_data_result["english_message"] = "invalid serial"
                    return False, wrong_data_result
            else:
                return False, wrong_token_result
        else:
            return False, wrong_token_result

    @staticmethod
    def user_get_all_serializer(token, serial, page, count):
        token_result = token_to_user_id(token)
        if token_result["status"] == "OK":
            user_id = token_result["data"]["user_id"]

            offset = int((page - 1) * count)
            limit = int(count)
            filters = {
                "serial": serial,
                "user__id": user_id
            }
            filters = {k: v for k, v in filters.items() if v is not None}
            queryset = Devices.objects.filter(**filters).order_by('-create_date')[offset:offset + limit]
            response = Devices.objects.serialize(queryset=queryset)
            return True, response
        else:
            return False, wrong_token_result

    @staticmethod
    def staff_admin_assign_user_serializer(token, user_id, serial):
        token_result = token_to_user_id(token)
        if token_result["status"] == "OK":
            admin_id = token_result["data"]["user_id"]
            if AdminSerializers.admin_check_permission(admin_id, 'Staff'):
                admin = Admins.objects.get(id=admin_id)
                if admin.is_staff is not True:
                    wrong_data_result["message"] = "You do not have the required access"
                    return False, wrong_data_result
                try:
                    user_object = Users.objects.get(id=user_id)
                except:
                    wrong_data_result["message"] = "invalid user_id"
                    return False, wrong_data_result
                try:
                    device_object = Devices.objects.filter(serial=serial)
                    if len(device_object) == 1:
                        device_object.update(user=user_object, admin=admin)
                    else:
                        wrong_data_result["message"] = "invalid serial"
                        return False, wrong_data_result
                except:
                    wrong_data_result["message"] = "invalid user_id"
                    return False, wrong_data_result
                return True, status_success_result
            else:
                return False, wrong_token_result
        else:
            return False, wrong_token_result

    @staticmethod
    def user_get_one_serializer(token, serial):
        token_result = token_to_user_id(token)
        if token_result["status"] == "OK":
            user_id = token_result["data"]["user_id"]
            try:
                queryset = Devices.objects.filter(user__id=user_id, serial=serial)
                response = Devices.objects.serialize(queryset=queryset)
                return True, response
            except:
                wrong_data_result["english_message"] = "invalid serial"
                return False, wrong_data_result
        else:
            return False, wrong_token_result

    @staticmethod
    def thread_for_use_time_duration(device_serial, user_time_duration):
        current_time = datetime.now()
        time_to_shout_down = current_time + timedelta(minutes=user_time_duration)
        while True:
            current_time = datetime.now()
            if current_time == time_to_shout_down:
                # send trun off to device
                pass
        pass

    @staticmethod
    def user_send_order_serializer(token, serial, state):
        token_result = token_to_user_id(token)
        if token_result["status"] == "OK":
            user_id = token_result["data"]["user_id"]
            try:
                device_object = Devices.objects.get(serial=serial)
            except:
                wrong_data_result["message"] = "Invalid serial"
                return False, wrong_data_result
            if device_object.user is None:
                wrong_data_result["message"] = "Invalid data"
                return False, wrong_data_result
            if str(device_object.user.id) != str(user_id):
                wrong_data_result["message"] = "Invalid data"
                return False, wrong_data_result
            user_time_duration = device_object.user.time_duration
            # start_thread
            if user_time_duration <= 0:
                wrong_data_result["message"] = "Please buy time."
                return False, wrong_data_result
            elif user_time_duration > 0:
                if state is True:
                    DeviceSerializers.thread_object.start_thread(device_serial=serial)
                elif state is False:
                    print("Stop")
                    DeviceSerializers.thread_object.stop_thread(device_serial=serial)
            return True, status_success_result
        else:
            return False, wrong_token_result

    @staticmethod
    def user_devices_serializer(token, user_id_list):
        token_result = token_to_user_id(token)
        if token_result["status"] == "OK":
            admin_id = token_result["data"]["user_id"]
            if AdminSerializers.admin_check_permission(admin_id, 'Admin'):
                response = []
                for id in user_id_list:
                    user_devices = Devices.objects.filter(user__id=id)
                    queryset = user_devices.order_by('-create_date')
                    user_response = Devices.objects.serialize(queryset=queryset)
                    prepared_data = {
                        "UserID": id,
                        "AllUserDeviceCount": user_devices.count(),
                        "AllUserDevices": user_response
                    }
                    response.append(prepared_data)
                return True, response
            else:
                return False, wrong_token_result
        else:
            return False, wrong_token_result
