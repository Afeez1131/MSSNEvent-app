from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView
from auth_app.forms import MyAuthForm


urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('login/', LoginView.as_view(authentication_form=MyAuthForm), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('generate/', views.gen_user, name='gen_user'),
    path('reset-password/', views.reset_password, name='reset_password'),
    path('create-user/', views.generate_user, name='create_user'),

]
