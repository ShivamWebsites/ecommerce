from django.urls import path
from rest_framework import routers
from . import views
router = routers.DefaultRouter()
router.register(r'user-info', views.UserInfoViewsets)

urlpatterns = [
    path('register/', views.RegistrationView.as_view(), name='register'),
    path('verify-email/<str:uid>/<str:token>/', views.VerifyEmail.as_view(), name='verify_email'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('forgot-password/', views.ForgetPassword.as_view(), name='forget-password'),
    path('reset-password/<str:token>/<str:uid>/', views.ResetPassword.as_view(), name='reset_password'),
    path('change-password/', views.ChangePassword.as_view(), name='change_password'),
    path('user-profile/', views.UserProfileUpdateAPIView.as_view(), name='user_profile'),
    path('user-detail/', views.GetUser.as_view(), name='user_detail'),

    path('google-authentication/', views.GoogleSocialAuthView.as_view()),
]
urlpatterns += router.urls
