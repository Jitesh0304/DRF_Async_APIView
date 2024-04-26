from .models import User
from adrf.serializers import ModelSerializer
from rest_framework import serializers
from channels.db import database_sync_to_async
from asgiref.sync import sync_to_async, async_to_sync


        ## user registration 
class UserRegistrationSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    name = serializers.CharField(max_length=30)
    password = serializers.CharField(required=True, style = {'input_type':'password'}, write_only =True)
    password2 = serializers.CharField(required=True, style = {'input_type':'password'}, write_only =True)
    class Meta:
        fields = ['email','name','password','password2']


    def validate(self, data):
        password = data.get('password')
        password2 = data.get('password2')
        if password != password2:
            raise serializers.ValidationError('Password and Confirm password does not match.....')
        if len(password) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long....")
        return data


                ## if the validation is successfull then create that 
    def create(self, validate_data):
        # user = await sync_to_async(User.objects.create_user, thread_sensitive=False)(**validate_data)
        # user = User.objects.create_user(**validate_data)
        user = database_sync_to_async(User.objects.create_user)(**validate_data)
        return user




                ## This is for login page
class UserLoginSerializer(ModelSerializer):
    email = serializers.EmailField(max_length=200)
    class Meta:
        model = User
        fields = ['email','password']




            ## this is for perticular user profile 
class UserProfileSerializer(ModelSerializer):
    class Meta:
        model = User
        exclude = ['password']