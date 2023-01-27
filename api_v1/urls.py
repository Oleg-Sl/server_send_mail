from django.urls import include, path
from rest_framework import routers

from api_v1.views import (
    SendEmailViewSet,
    SendEmailAsyncViewSet,
    GetSizeQueueEmailsViewSet,
)


app_name = 'api_v1'


router = routers.DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),

    # Синхронная отправка писем
    path(r'send-email', SendEmailViewSet.as_view()),
    # Асинхронная отправка писем
    path(r'send-email-async', SendEmailAsyncViewSet.as_view()),
    # Получение размера очереди для асинхронной отправки писем
    path(r'get-size-queue-emails', GetSizeQueueEmailsViewSet.as_view()),

]

urlpatterns += router.urls




