from django.conf.urls import url
from .views import (
    RegisterAPIView,
    LoginAPIView,
)

urlpatterns = [
    url(r'^register/', RegisterAPIView.as_view(), name='register_api'),
    url(r'^login/$', LoginAPIView.as_view(), name='login_api'),
]
