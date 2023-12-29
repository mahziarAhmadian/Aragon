from Devices.models.devices import Devices, DeviceTypes
from Devices.models.tarnsactions import Transactions
from Authorization.models import Admins, Users
from Authorization.TokenManager import user_id_to_token, token_to_user_id
from Devices.Serializers import status_success_result, wrong_token_result, wrong_data_result
from Authorization.Serializers.AdminSerilizer import AdminSerializers
from MQQTService.Publisher import publish_message_to_client


class TransactionSerializers:

    @staticmethod
    def create_serializer(token, stripe_code, status, duration, other_information):
        token_result = token_to_user_id(token)
        if token_result["status"] == "OK":
            user_id = token_result["data"]["user_id"]
            try:
                user_obj = Users.objects.get(id=user_id)
                transaction = Transactions()
                transaction.user = user_obj
                transaction.stripe_code = stripe_code
                transaction.status = status
                transaction.duration = duration
                transaction.other_information = other_information
                transaction.save()
                return True, status_success_result
            except:
                wrong_data_result["message"] = "Invalid data"
                return False, wrong_data_result
        else:
            return False, wrong_token_result

    @staticmethod
    def admin_get_all_serializer(token, status, page, count):
        token_result = token_to_user_id(token)
        if token_result["status"] == "OK":
            admin_id = token_result["data"]["user_id"]
            if AdminSerializers.admin_check_permission(admin_id, 'Admin'):
                admin = Admins.objects.get(id=admin_id)
                print(admin.permissions)
                offset = int((page - 1) * count)
                limit = int(count)
                filters = {
                    "status": status
                }
                filters = {k: v for k, v in filters.items() if v is not None}
                queryset = Transactions.objects.filter(**filters).order_by('-create_time')[offset:offset + limit]
                response = Transactions.objects.serialize(queryset=queryset)
                return True, response
            else:
                return False, wrong_token_result
        else:
            return False, wrong_token_result
