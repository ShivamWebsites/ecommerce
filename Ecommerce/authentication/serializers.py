from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import CustomUser,UserProfile
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from rest_framework.fields import SerializerMethodField
from . import google
from .register import register_social_user
from rest_framework.exceptions import AuthenticationFailed
from ecommerce.settings import BACKEND_SITE_URL
from django.conf import settings


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    confirm_password = serializers.CharField(required=True)
    username = serializers.CharField(max_length=20, required=True, allow_blank=False)

    class Meta:
        model = CustomUser
        fields = ('password', 'confirm_password','country','first_name','last_name',
                  'email','phone','username')


    # Object Level Validation
    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match")
        if CustomUser.objects.filter(email__iexact=data['email']).exists():
            raise serializers.ValidationError("Email must be unique")
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = CustomUser.objects.create_user(**validated_data)
        return user


class UserSerializer(serializers.ModelSerializer):
    email = serializers.CharField(required=True)

    class Meta:
        model = CustomUser
        fields = ["email", "password"]
        extra_kwargs = {
            'password': {'write_only': True}
        }


class SendForgotEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)


class ResetPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=200, required=True)
    confirm_password = serializers.CharField(max_length=200, required=True)




class ChangePasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=200, required=True)
    current_password = serializers.CharField(max_length=200, required=True)
    password = serializers.CharField(max_length=200, required=True)
    confirm_password = serializers.CharField(max_length=200, required=True)


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('image',)


    



class UserUpdateSerializer(serializers.ModelSerializer):
    user_profile = UserProfileSerializer(required=False)

    class Meta:
        model = CustomUser
        fields = ('email','first_name','last_name', 'phone', 'country', 'user_profile')


    def update(self, instance, validated_data):
        profile_data = validated_data.pop('user_profile', {})
        user_profile = getattr(instance, 'user_profile', None)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.country = validated_data.get('country', instance.country)
        instance.save()

        if not user_profile and profile_data:
            user_profile = UserProfile.objects.create(user=instance)
            
        if user_profile:
            for attr, value in profile_data.items():
                setattr(user_profile, attr, value)
            user_profile.save()

        return instance



class UserInfoSerializer(serializers.ModelSerializer):
    # user_profile = SerializerMethodField('get_profile_pic')
    user_image =  SerializerMethodField('get_user_image')
    class Meta:
        model = CustomUser
        fields = ('first_name','id','user_image','role','email', 'country','phone', 'username','last_name')

    def get_user_image(self, obj):
        if obj:
            # try:
            #     request = self.context.get('request')
            #     return request.build_absolute_uri(obj.user_profile.image.url)
            # except:
            #     return None

            try:
                request = self.context.get('request')
                image_url = obj.user_profile.image.url
                backend_site_url = getattr(settings, 'BACKEND_SITE_URL', 'http://localhost/')
                return f"{backend_site_url}{image_url}"
            except:
                return None

        return None


    def update(self, instance, validated_data):
        instance.role = validated_data.get('role', instance.role)
        instance.email = validated_data.get('email', instance.email)

        # Exclude email field from validation during updates
        self.fields['email'].required = False

        instance.save()
        return instance
    # def get_profile_pic(self,obj):
    #     if obj.




class GoogleSocialAuthSerializer(serializers.Serializer):
    auth_token = serializers.CharField()

    def validate_auth_token(self, auth_token):
        user_data = google.Google.validate(auth_token)

        print("================   ", user_data)

        try:
            user_data['sub']
        except:
            raise serializers.ValidationError(
                'The token is invalid or expired. Please login again.'
            )

        # if user_data['aud'] != os.environ.get('GOOGLE_CLIENT_ID'):
        # if user_data['aud'] !=  "426800741975-qsr1m31mbb0420q1k5lt6faict37hi3e.apps.googleusercontent.com":
        if user_data['aud'] !=  "209738357004-32inb3h5j9lnitjoadlnk0u53bum7ue7.apps.googleusercontent.com":
        # if user_data['aud'] != "91412928555-tdddig6gni7g0l45iaa344ch3n3o3cje.apps.googleusercontent.com": 
            raise AuthenticationFailed('oops, who are you?')

        user_id = user_data['sub']
        email = user_data['email']
        name = user_data['name']
        provider = 'google'

        return register_social_user(
            provider=provider, user_id=user_id, email=email, name=name)
