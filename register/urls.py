from django.urls import path
from .views import (AuthView, UserUpdate, PasswordChange, PasswordForget, PasswordChangeDone,
                    PasswordResetConfirm, PasswordResetComplete, PasswordResetDone)

app_name = "register"

urlpatterns = [
    path('', AuthView.as_view(), name='auth'),
    path('user_update/<int:pk>/', UserUpdate.as_view(), name='user_update'),
    path('password_change/', PasswordChange.as_view(), name='password_change'),
    path('password_change/done/', PasswordChangeDone.as_view(), name='password_change_done'),
    path('password_forget/', PasswordForget.as_view(), name='password_forget'),
    path('password_forget/done/', PasswordResetDone.as_view(), name='password_forget_done'),
    path('password_reset/confirm/<uidb64>/<token>/', PasswordResetConfirm.as_view(),
         name='password_reset_confirm'),
    path('password_reset/complete/', PasswordResetComplete.as_view(), name='password_reset_complete'),
]
