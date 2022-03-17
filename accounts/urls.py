from django.urls import path
from accounts.views import Auth, Signupview

urlpatterns = [
    path('auth/', Auth.as_view(), name='auth'),
    path('signup/', Signupview.as_view(), name='signup'),
]
