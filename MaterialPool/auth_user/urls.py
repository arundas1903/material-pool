from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^users/$', views.CreateUser.as_view()),  # Url for registration
    url(r'^login_token/$', views.UserLogin.as_view()),  # Url for login
    url(r'^password/$', views.ChangePassword.as_view()),  # Url for login
]
