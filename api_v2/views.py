from rest_framework import views, viewsets, filters, status, mixins, generics
from rest_framework.response import Response
from django.shortcuts import render
import os
from django.views.decorators.clickjacking import xframe_options_exempt

from datecommunication import settings


import logging
import json
import time


from . import service



logging.basicConfig(filename="installapp.log", level=logging.INFO,
                    format='[%(asctime)s] %(levelname).1s %(message)s', datefmt='%Y.%m.%d %H:%M:%S')




class InstallApiView(views.APIView):
    @xframe_options_exempt
    def post(self, request):
        data = {
            "domain": request.query_params.get("DOMAIN", "bits24.bitrix24.ru"),
            "auth_token": request.data.get("AUTH_ID", ""),
            "expires_in": request.data.get("AUTH_EXPIRES", 3600),
            "refresh_token": request.data.get("REFRESH_ID", ""),
            "application_token": request.query_params.get("APP_SID", ""),   # используется для проверки достоверности событий Битрикс24
            'client_endpoint': f'https://{request.query_params.get("DOMAIN", "bits24.bitrix24.ru")}/rest/',
        }
        return render(request, 'install.html')


# Обработчик установленного приложения
class IndexApiView(views.APIView):
    @xframe_options_exempt
    def post(self, request):

        return render(request, 'index.html')


class AppUnistallApiView(views.APIView):
    @xframe_options_exempt
    def post(self, request):
        return Response(status.HTTP_200_OK)


class ActivityApiView(views.APIView):
    def post(self, request):
        logging.info({
            "params": request.query_params,
            "data": request.data,
        })
        event = request.data.get("event", "")
        id_activity = request.data.get("data[FIELDS][ID]", None)

        if not id_activity:
            return Response("Not transferred ID activity", status=status.HTTP_400_BAD_REQUEST)
        return Response(status.HTTP_200_OK)


class CallsApiView(views.APIView):
    def post(self, request):
        return Response(status.HTTP_200_OK)


class UsersApiView(views.APIView):

    def post(self, request):
        logging.info({
            "params": request.query_params,
            "data": request.data,
        })
        return Response(status=status.HTTP_200_OK)




