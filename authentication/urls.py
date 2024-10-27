from django.urls import path
from .views import CustomUserCreateView
from .views import CustomPasswordResetConfirmView, CustomPasswordResetView
from .views import VerifyEmailView
from rest_framework_simplejwt.views import(
    TokenObtainPairView,
    TokenRefreshView,
)

app_name = 'authentication'


urlpatterns = [
    path('auth/register/', CustomUserCreateView.as_view(), name='user-register'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_view'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('password-reset/', CustomPasswordResetView.as_view(), name='password-reset'),
    path('password-reset-confirm/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_view'),
    # path('verify-email/<uidb64>/<token>/', VerifyEmailView.as_view(), name='verify_email'),
    path('verify-email/<str:uidb64>/<str:token>/', VerifyEmailView.as_view(), name='verify_email'),
]
