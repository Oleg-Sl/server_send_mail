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
        service.writ_app_data_to_file(data)
        return render(request, 'install.html')


class IndexApiView(views.APIView):
    @xframe_options_exempt
    def post(self, request):
        # logging.info({
        #     request_params["DOMAIN"]: type(request_params["DOMAIN"]),
        #     request_data["AUTH_ID"]: type(request_data["AUTH_ID"]),
        #     request_data["AUTH_EXPIRES"]: type(request_data["AUTH_EXPIRES"]),
        #     request_data["REFRESH_ID"]: type(request_data["REFRESH_ID"]),
        #     request_data["PLACEMENT"]: type(request_data["PLACEMENT"]),
        # })
        data = {
            "request": request.query_params,
            "ddd": request.data,
        }
        return render(request, 'index.html', context=data)

        # return Response(request.data, status=status.HTTP_200_OK)



        