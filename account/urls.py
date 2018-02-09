from django.conf.urls import url
from django.contrib.auth.views import LoginView, LogoutView

from .views import (
    RegisterView,
)


urlpatterns = [
    url(r'^register/$', RegisterView.as_view(), name='register'),
    url(r'^login/$', LoginView.as_view(template_name='account/login.html'), name="login"),
    url(r'^logout/$', LogoutView.as_view(template_name='account/login.html'), name="logout"),
]
