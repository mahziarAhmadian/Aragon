from Devices.models.device_types import DeviceTypes
from Authorization.models import Admins, Users
from Authorization.TokenManager import user_id_to_token, token_to_user_id
from Devices.Serializers import status_success_result, wrong_token_result, wrong_data_result
from Authorization.Serializers.AdminSerilizer import AdminSerializers


class DeviceTypeSerializers:

    @staticmethod
    def admin_create_serializer(token, name, other_information):
        token_result = token_to_user_id(token)
        if token_result["status"] == "OK":
            admin_id = token_result["data"]["user_id"]
            if AdminSerializers.admin_check_permission(admin_id, 'Admin'):
                admin_object = Admins.objects.get(id=admin_id)
                if admin_object.is_super_admin is not True:
                    wrong_data_result["message"] = "You do not have the required access"
                    return False, wrong_data_result
                try:
                    device_type = DeviceTypes()
                    device_type.admin = admin_object
                    device_type.name = name
                    device_type.other_information = other_information
                    device_type.save()
                    return True, status_success_result
                except:
                    wrong_data_result["message"] = "Invalid data"
                    return False, wrong_data_result
            wrong_data_result["message"] = "You do not have the required access"
            return False, wrong_data_result
        else:
            return False, wrong_token_result

    @staticmethod
    def admin_edit_serializer(token, id, name, other_information):
        token_result = token_to_user_id(token)
        if token_result["status"] == "OK":
            admin_id = token_result["data"]["user_id"]
            if AdminSerializers.admin_check_permission(admin_id, 'Admin'):
                admin_object = Admins.objects.get(id=admin_id)
                if admin_object.is_super_admin is not True:
                    wrong_data_result["message"] = "You do not have the required access"
                    return False, wrong_data_result
                try:
                    prepared_data = {
                        "name": name,
                        "other_information": other_information
                    }
                    DeviceTypes.objects.filter(id=id).update(**prepared_data)
                    return True, status_success_result
                except:
                    wrong_data_result["message"] = "Invalid data"
                    return False, wrong_data_result
            wrong_data_result["message"] = "You do not have the required access"
            return False, wrong_data_result
        else:
            return False, wrong_token_result

    @staticmethod
    def admin_delete_serializer(token, id):
        token_result = token_to_user_id(token)
        if token_result["status"] == "OK":
            admin_id = token_result["data"]["user_id"]
            if AdminSerializers.admin_check_permission(admin_id, 'Admin'):
                admin_object = Admins.objects.get(id=admin_id)
                if admin_object.is_super_admin is not True:
                    wrong_data_result["message"] = "You do not have the required access"
                    return False, wrong_data_result
                try:
                    DeviceTypes.objects.get(id=id).delete()
                    return True, status_success_result
                except:
                    wrong_data_result["message"] = "Invalid id"
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
                offset = int((page - 1) * count)
                limit = int(count)
                filters = {
                    "name": name
                }
                filters = {k: v for k, v in filters.items() if v is not None}
                queryset = DeviceTypes.objects.filter(**filters).order_by('-create_date')[offset:offset + limit]
                response = DeviceTypes.objects.serialize(queryset=queryset)
                return True, response
            else:
                return False, wrong_token_result
        else:
            return False, wrong_token_result

    @staticmethod
    def admin_get_one_serializer(token, id):
        token_result = token_to_user_id(token)
        if token_result["status"] == "OK":
            admin_id = token_result["data"]["user_id"]
            if AdminSerializers.admin_check_permission(admin_id, 'Admin'):
                try:
                    queryset = DeviceTypes.objects.filter(id=id)
                    response = DeviceTypes.objects.serialize(queryset=queryset)
                    return True, response
                except:
                    wrong_data_result["message"] = "Invalid id"
                    return False, wrong_data_result
            else:
                return False, wrong_token_result
        else:
            return False, wrong_token_result
