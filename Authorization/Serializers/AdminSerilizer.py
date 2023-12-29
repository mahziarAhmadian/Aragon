from Authorization.models import Admins
from Authorization.TokenManager import user_id_to_token, token_to_user_id
from Authorization.Serializers import status_success_result, wrong_token_result, wrong_data_result


class AdminSerializers:

    @staticmethod
    def admin_check_permission(admin_id, permission):
        admin = Admins.objects.get(id=admin_id)
        if type(permission) == str:
            if permission in admin.permissions:
                return True
            else:
                return False
        else:
            counter = len(permission)
            counter_checker = 0
            for per in permission:
                if per in admin.permissions:
                    counter_checker += 1
                else:
                    pass
            if counter_checker == counter:
                return True
            else:
                return False

    @staticmethod
    def admin_login_serializer(email, password):
        try:
            admin = Admins.objects.get(email=email, password=password)
            is_staff = admin.is_staff
            is_super_user = admin.is_super_admin
            admin_id = str(admin.id)
            permissions = admin.permissions
            token = user_id_to_token(admin_id, True, token_level="Admin")

            result = {
                "permissions": permissions,
                "IsStaff": is_staff,
                "IsSuperUser": is_super_user,
                "token": token
            }
            return True, result
        except:
            return False, None

    @staticmethod
    def admin_add_serializer(token, name, last_name, email, is_staff, password, other_information):
        token_result = token_to_user_id(token)
        if token_result["status"] == "OK":
            admin_id = token_result["data"]["user_id"]
            if AdminSerializers.admin_check_permission(admin_id, 'Admin'):
                admin_object = Admins.objects.get(id=admin_id)
                if admin_object.is_super_admin is not True:
                    wrong_data_result["english_message"] = "You do not have the required access"
                    return False, wrong_data_result
                try:
                    admin = Admins()
                    admin.name = name
                    admin.last_name = last_name
                    admin.email = email
                    admin.password = password
                    admin.is_staff = is_staff
                    admin.is_super_admin = False
                    admin.permissions = ['Self', 'Admin', 'Staff', 'User', 'Device']
                    admin.other_information = other_information
                    admin.save()
                    return True, status_success_result
                except:
                    wrong_data_result["message"] = "Duplicate email"
                    return False, wrong_data_result

            wrong_data_result["english_message"] = "You do not have the required access"
            return False, wrong_data_result
        else:
            return False, wrong_token_result

    @staticmethod
    def admin_edit_serializer(
            token, id, name, last_name, email, is_staff, password, other_information):
        token_result = token_to_user_id(token)
        if token_result["status"] == "OK":
            admin_id = token_result["data"]["user_id"]
            if AdminSerializers.admin_check_permission(admin_id, 'Admin'):
                try:
                    admin = Admins.objects.get(id=id)
                    prepared_data = {
                        "name": name,
                        "last_name": last_name,
                        "email": email,
                        "is_staff": is_staff,
                        "password": password,
                        "other_information": other_information
                    }
                    old_email = admin.email
                    if old_email == email:
                        prepared_data.pop('email')
                    Admins.objects.filter(id=admin_id).update(**prepared_data)
                    return True, status_success_result
                except:
                    wrong_data_result['message'] = 'invalid data'
                    return False, wrong_data_result
            else:
                return False, wrong_token_result
        else:
            return False, wrong_token_result

    @staticmethod
    def admin_delete_serializer(token, id):
        token_result = token_to_user_id(token)
        if token_result["status"] == "OK":
            admin_id = token_result["data"]["user_id"]
            if AdminSerializers.admin_check_permission(admin_id, 'Admin'):
                try:
                    Admins.objects.get(id=id).delete()
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
                    queryset = Admins.objects.filter(id=id)
                    response = Admins.objects.serialize(queryset=queryset)
                    return True, response
                except:
                    wrong_data_result["english_message"] = "invalid id"
                    return False, wrong_data_result
            else:
                return False, wrong_token_result
        else:
            return False, wrong_token_result

    @staticmethod
    def admin_get_all_serializer(token, name, page, count, is_super_admin, is_staff):
        token_result = token_to_user_id(token)
        if token_result["status"] == "OK":
            admin_id = token_result["data"]["user_id"]
            if AdminSerializers.admin_check_permission(admin_id, 'Admin'):
                offset = int((page - 1) * count)
                limit = int(count)
                filters = {
                    "name": name,
                    "is_super_admin": is_super_admin,
                    "is_staff": is_staff,
                }
                filters = {k: v for k, v in filters.items() if v is not None}
                queryset = Admins.objects.filter(**filters).order_by('-create_date')[offset:offset + limit]
                response = Admins.objects.serialize(queryset=queryset)
                return True, response
            else:
                return False, wrong_token_result
        else:
            return False, wrong_token_result
