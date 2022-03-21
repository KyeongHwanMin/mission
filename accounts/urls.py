from django.urls import path
from accounts.views import LoginView, MyinfoView, ChangePasswordView, AuthView, SignupView

urlpatterns = [
    path('auth/', AuthView.as_view(), name='auth'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('myinfo/', MyinfoView.as_view(), name='myinfo'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
]
