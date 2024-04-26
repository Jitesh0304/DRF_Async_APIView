from rest_framework import status
from rest_framework.views import APIView
from adrf.views import APIView as AsyncAPIView
from rest_framework.response import Response
from .serializers import UserRegistrationSerializer, UserLoginSerializer, UserProfileSerializer
from .models import User
# from django.contrib.auth import authenticate
from .custom_auth import CustomUserAuthentication, AsyncPermission
from rest_framework_simplejwt.tokens import RefreshToken
# from rest_framework.permissions import IsAuthenticated
from channels.db import database_sync_to_async
from asgiref.sync import async_to_sync, sync_to_async
from rest_framework_simplejwt.tokens import RefreshToken






def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'access': str(refresh.access_token),
        'refresh': str(refresh),
    }




class UserRegisterView(AsyncAPIView):

    async def post(self, request, format=None):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            await serializer.save()
            return Response({'msg':'ok'}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





class UserLoginView(AsyncAPIView):
    async def post(self, request, format= None):
        try:
            serializer = UserLoginSerializer(data= request.data)
            if serializer.is_valid():

                email = serializer.data.get('email')
                password = serializer.data.get('password')

                auth_class = CustomUserAuthentication()
                user_auth = await auth_class.authenticate(email= email, password = password)
                if user_auth is not None:
                    user = await database_sync_to_async(User.objects.get)(email=email)
                    token = get_tokens_for_user(user)
                        ## generate the refresh token
                    return Response({'token': token}, status=status.HTTP_200_OK)
                else:
                    return Response({'msg':'wrong credential'},status=status.HTTP_404_NOT_FOUND)
            else:
                return Response({'msg':serializer.errors}, status= status.HTTP_400_BAD_REQUEST)    
        except Exception as e:
            return Response({'msg': str(e)}, status=status.HTTP_400_BAD_REQUEST)



class UserProfileView(AsyncAPIView):
    # permission_classes = [IsAuthenticated]
    permission_classes = [AsyncPermission]

    async def get(self, request, format= None):
        try:
            user = request.user
            serializer = UserProfileSerializer(user, context={"user":user})
            new_serializer = await serializer.adata
            return Response(new_serializer, status= status.HTTP_200_OK)
        except Exception as e:
            return Response({'msg': str(e)}, status=status.HTTP_400_BAD_REQUEST)

