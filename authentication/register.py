from django.contrib.auth import authenticate
from authentication.models import CustomUser
from dotenv import load_dotenv
import os
import random
from rest_framework.exceptions import AuthenticationFailed

load_dotenv()


def generate_username(name):
    username = "".join(name.split(' ')).lower()
    if not CustomUser.objects.filter(username=username).exists():
        return username
    else:
        random_username = username + str(random.randint(0, 1000))
        return generate_username(random_username)


def register_social_user(provider, user_id, email, name):
    filtered_user_by_email = CustomUser.objects.filter(email=email)
    print("email  ", email)
    if filtered_user_by_email.exists():
        # print("if if if if if =====")
        # print("email " ,filtered_user_by_email[0].email)
        # print("provider ", filtered_user_by_email[0].auth_provider)

        # if filtered_user_by_email[0].email == email and filtered_user_by_email[0].auth_provider == '' or filtered_user_by_email[0].auth_provider == None:
        #     print("yoou are in firstb if")
        #     raise AuthenticationFailed('Email already exists')
        # print("out side outside")

        if provider == filtered_user_by_email[0].auth_provider:

            print("6666666666666666 ", filtered_user_by_email[0].auth_provider)

            user = CustomUser.objects.filter(email=email).first()
            if user:
                user.check_password("jhwue824jkhw83it")
                registered_user = user
                # registered_user = authenticate(
                #     # email=email, password=os.environ.get('SOCIAL_SECRET'))
                #     email=email, password="jhwue824jkhw83it")

                return {
                    'id': registered_user.id,
                    'user_name': registered_user.username,
                    'email': registered_user.email,
                }


        else:
            raise AuthenticationFailed(
                detail='Please continue your login using ' + filtered_user_by_email[0].auth_provider)

    else:
        print("else else register ---")
        user_data = {
            'username': generate_username(name), 'email': email,
            # 'password': os.environ.get('SOCIAL_SECRET')}
        'password': "jhwue824jkhw83it"}
        user = CustomUser(
        username=user_data['username'],
        email=user_data['email']
        )
        user.set_password(user_data['password'])
        user.is_verified = True
        user.email_verified = True
        user.auth_provider = provider
        user.save()
        print("------ else else else else ------")
        # new_user = authenticate(
        #     # email=email, password=os.environ.get('SOCIAL_SECRET'))
        # email=email, password="jhwue824jkhw83it")
        return {
            'email': user.email,
            'username': user.username,
            # 'tokens': new_user.tokens()
        }