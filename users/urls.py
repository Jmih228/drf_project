from django.urls import path
from users.views import PaymentListAPIView, UserCreateAPIView, UserRetriveAPIView, UserUpdateAPIView, UserDestroyAPIView
from users.apps import UsersConfig
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView,)


app_name = UsersConfig.name

urlpatterns = [
    path('user/create/', UserCreateAPIView.as_view(), name='user_create'),
    path('profile/<int:pk>/', UserRetriveAPIView.as_view(), name='profile'),
    path('update/<int:pk>/', UserUpdateAPIView.as_view(), name='profile_update'),
    path('delete/<int:pk>/', UserDestroyAPIView.as_view(), name='user_delete'),
    path('payment/', PaymentListAPIView.as_view(), name='payment_list'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh')
]
