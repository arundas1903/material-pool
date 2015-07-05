from django.conf.urls import url

from rest_framework.urlpatterns import format_suffix_patterns

from . import views

urlpatterns = [
    url(r'^users/$', views.CreateUser.as_view()),  # Url for registration
    url(r'^login_token/$', views.UserLogin.as_view()),  # Url for login
]