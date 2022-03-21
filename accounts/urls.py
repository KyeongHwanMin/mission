from django.urls import path, include
from accounts.views import LoginView, MyinfoView, ChangePasswordView, SignupView, AuthView, LogoutView

urlpatterns = [
    path('auth/', AuthView.as_view(), name='auth'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='login'),
    path('myinfo/<int:pk>/', MyinfoView.as_view(), name='myinfo'),
    path('change-password/<int:pk>/', ChangePasswordView.as_view(), name='change-password'),
    path('api-auth/', include('rest_framework.urls')),

]
