from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView
from auth_app.forms import MyAuthForm


urlpatterns = [
    path('signup/', views.SignupView, name='signup'),
    path('login/', LoginView.as_view(authentication_form=MyAuthForm), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('generate/', views.gen_user, name='gen_user'),

]
