from django.urls import include, path
from rest_framework import routers


from .views import (InstallApiView, 
                    IndexApiView,
                    AppUnistallApiView,
                    ActivityApiView,
                    CallsApiView,
                    UsersApiView,
                    )


app_name = 'api_v2'


router = routers.DefaultRouter()


urlpatterns = [
    path('', include(router.urls)),
    path('install/', InstallApiView.as_view()),
    path('index/', IndexApiView.as_view()),
    path('app-uninstall/', AppUnistallApiView.as_view()),
    path('create-update-activity/', ActivityApiView.as_view()),
    path('create-update-calls/', CallsApiView.as_view()),
    path('create-user/', UsersApiView.as_view()),
    
]


urlpatterns += router.urls

