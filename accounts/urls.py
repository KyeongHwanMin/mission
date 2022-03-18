from django.urls import path, include
from accounts.views import Auth, Signupview, LoginView, MyinfoView, ChangePasswordView

urlpatterns = [
    path('auth/', Auth.as_view(), name='auth'),
    path('signup/', Signupview.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('myinfo/', MyinfoView.as_view(), name='myinfo'),
    path('change-password/<int:pk>/', ChangePasswordView.as_view(), name='change-password'),
    path('api-auth/', include('rest_framework.urls')),
    # path("auth/register/", RegistrationAPI.as_view()),
    # path("auth/login/", LoginAPI.as_view()),
]
