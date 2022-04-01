
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import *
User = get_user_model()
from django.contrib.auth import authenticate #for authentication and phone otp




# User serializer for registration
class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','name','is_admin','is_customer', 'email','password','is_verified']

        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        # print("here")
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        print(instance)
        # print("here")
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


##for Login Serializer
class LoginUserSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'}, trim_whitespace=False)
    
    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        if email and password:
            
            if User.objects.filter(email=email).exists():
                user = authenticate(request=self.context.get('request'),
                                    email=email, password=password)
                # print(password)
                # getUser = User.objects.all().filter(email=email).values('is_deliveryboy','is_verified')
                # print(getUser)
            else:
                msg = {'detail': 'Email ID is not registered.',
                       'register': False,"status":False}
                raise serializers.ValidationError(msg)
            getUser = User.objects.all().filter(email=email).values('is_verified')
            
            if not user:
                msg = {
                    'detail': 'Unable to log in with provided credentials.', 'register': True,"status":False}
                raise serializers.ValidationError(msg, code='authorization')

        else:
            msg = {'detail':'Must include "Email ID" and "password".',"status":False}
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        
        return attrs


#for product get,post and update with varient(quantity) and category
class UserDetailsSerializer(serializers.ModelSerializer):
    User = User()
    class Meta:
        model = userDetails
        fields = ('__all__') 
