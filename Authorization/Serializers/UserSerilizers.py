from Authorization.models import Admins, Users
from Devices.models.devices import Devices
from Authorization.TokenManager import user_id_to_token, token_to_user_id
from Authorization.Serializers import status_success_result, wrong_token_result, wrong_data_result
from Authorization.Serializers.AdminSerilizer import AdminSerializers


class UserSerializers:

    @staticmethod
    def user_login_serializer(email, password):
        try:
            user = Users.objects.get(email=email, password=password)
            user_id = str(user.id)
            token = user_id_to_token(user_id, True, token_level="User")

            result = {
                "token": token
            }
            return True, result
        except:
            return False, None

    @staticmethod
    def staff_admin_create_user_serializer(token, name, last_name, email, password, other_information):
        token_result = token_to_user_id(token)
        if token_result["status"] == "OK":
            admin_id = token_result["data"]["user_id"]
            if AdminSerializers.admin_check_permission(admin_id, ['Staff', 'User']):
                admin_object = Admins.objects.get(id=admin_id)
                if admin_object.is_staff is not True:
                    wrong_data_result["message"] = "You do not have the required access"
                    return False, wrong_data_result
                try:
                    user = Users()
                    user.admin = admin_object
                    user.name = name
                    user.last_name = last_name
                    user.email = email
                    user.password = password
                    user.other_information = other_information
                    user.save()
                    return True, status_success_result
                except:
                    wrong_data_result["message"] = "Duplicate email"
                    return False, wrong_data_result
            wrong_data_result["message"] = "You do not have the required access"
            return False, wrong_data_result
        else:
            return False, wrong_token_result

    @staticmethod
    def user_get_profile_serializer(token):
        token_result = token_to_user_id(token)
        if token_result["status"] == "OK":
            user_id = token_result["data"]["user_id"]
            queryset = Users.objects.filter(id=user_id)
            response = Users.objects.serialize(queryset=queryset)
            return True, response
        else:
            return False, wrong_token_result

    @staticmethod
    def admin_edit_serializer(
            token, name, last_name, email, password, other_information):
        token_result = token_to_user_id(token)
        if token_result["status"] == "OK":
            user_id = token_result["data"]["user_id"]
            try:
                user = Users.objects.get(id=user_id)
                prepared_data = {
                    "name": name,
                    "last_name": last_name,
                    "email": email,
                    "password": password,
                    "other_information": other_information
                }
                old_email = user.email
                if old_email == email:
                    prepared_data.pop('email')
                Users.objects.filter(id=user_id).update(**prepared_data)
                return True, status_success_result
            except:
                wrong_data_result['message'] = 'invalid data'
                return False, wrong_data_result
        else:
            return False, wrong_token_result

    @staticmethod
    def admin_delete_serializer(token, id):
        token_result = token_to_user_id(token)
        if token_result["status"] == "OK":
            admin_id = token_result["data"]["user_id"]
            if AdminSerializers.admin_check_permission(admin_id, 'Admin'):
                try:
                    Users.objects.get(id=id).delete()
                except:
                    wrong_data_result["message"] = "invalid id"
                    return False, wrong_data_result

                return True, status_success_result
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
                    queryset = Users.objects.filter(id=id)
                    response = Users.objects.serialize(queryset=queryset)
                    return True, response
                except:
                    wrong_data_result["english_message"] = "invalid id"
                    return False, wrong_data_result
            else:
                return False, wrong_token_result
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
                queryset = Users.objects.filter(**filters).order_by('-create_date')[offset:offset + limit]
                response = Users.objects.serialize(queryset=queryset)
                for object in response:
                    user_id = object.get('Id')
                    queryset = Devices.objects.filter(user__id=user_id).order_by('-create_date')
                    user_devices_response = Devices.objects.serialize(queryset=queryset)
                    user_devices  = {
                        "AllUSerDevicesCount" : queryset.count() ,
                        "UserDevices" : user_devices_response
                    }
                    object['UserDevices'] = user_devices
                return True, response
            else:
                return False, wrong_token_result
        else:
            return False, wrong_token_result
