from Devices.models.devices import Devices, DeviceTypes
from Authorization.models import Admins, Users
from Authorization.TokenManager import user_id_to_token, token_to_user_id
from Devices.Serializers import status_success_result, wrong_token_result, wrong_data_result
from Authorization.Serializers.AdminSerilizer import AdminSerializers
from MQQTService.Publisher import publish_message_to_client


class DeviceSerializers:

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
                if 'Staff' in admin.permissions:
                    filters['admin__id'] = admin_id
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
    def user_send_order_serializer(token, serial):
        token_result = token_to_user_id(token)
        if token_result["status"] == "OK":
            user_id = token_result["data"]["user_id"]
            try:
                device_object = Devices.objects.get(serial=serial)
            except:
                wrong_data_result["message"] = "Invalid serial"
                return False, wrong_data_result
            if device_object.user is None :
                wrong_data_result["message"] = "Invalid data"
                return False, wrong_data_result
            if str(device_object.user.id) != str(user_id) :
                wrong_data_result["message"] = "Invalid data"
                return False, wrong_data_result
            prepared_data = {
                "serial": device_object.serial,
                "type_name": device_object.type.name,
                "state": device_object.state,
            }
            publish_message_to_client(data=prepared_data)
            return True , status_success_result
        else:
            return False, wrong_token_result
