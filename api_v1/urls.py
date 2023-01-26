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

    path(r'send-email', SendEmailViewSet.as_view()),
    path(r'send-email-async', SendEmailAsyncViewSet.as_view()),
    path(r'get-size-queue-emails', GetSizeQueueEmailsViewSet.as_view()),

]

urlpatterns += router.urls




