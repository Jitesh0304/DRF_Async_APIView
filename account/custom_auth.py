from rest_framework.permissions import BasePermission
from .models import User
from django.contrib.auth.backends import BaseBackend
from asgiref.sync import async_to_sync
from channels.db import database_sync_to_async



# class AsyncAuthentication(BaseAuthentication):
#     async def authenticate(self, request) -> tuple[User, None]:
#         return user, None


class CustomUserAuthentication(BaseBackend):
    async def authenticate(self, email=None, password=None):
        if email is None or password is None:
            return None
        try:
            # Query for user using emplID and companyCode
            user_data = database_sync_to_async(User.objects.get)(email=email)
            user = await user_data
        except User.DoesNotExist:
            return None

        # If user is found, verify password
        condition = await database_sync_to_async(user.check_password)(password)
        # if user.check_password(password):
        #     return user
        # else:
        #     return None
        if condition:
            return user
        else:
            return None



class AsyncPermission(BasePermission):
    async def has_permission(self, request, view) -> bool:
        if request.user.is_anonymous:
            return False
        return True

    async def has_object_permission(self, request, view, obj):
        if obj.user == request.user or request.user.is_admin:
            return True

        return False

