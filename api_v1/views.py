from rest_framework import views, viewsets, filters, status, mixins, generics
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.shortcuts import render

from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.generic import TemplateView
from rest_framework.permissions import IsAuthenticated



from django_filters import rest_framework as filters_externel
from django_filters.rest_framework import DjangoFilterBackend

from datetime import datetime, timedelta
from django.db import models
from django.db.models.functions import Coalesce
from rest_framework.pagination import PageNumberPagination



from urllib.parse import unquote
from email import encoders
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
import smtplib
import os
import json
import requests
import base64


from api_v1 import secrets
from api_v1 import bitrix
from api_v1 import html_templates


class SendEmailViewSet(views.APIView):
    def send_mail(self, to_email, head, body, files_data, cc_email):
        with open("api_v1/mail_secrets.json") as secrets_file:
            secret_data = json.load(secrets_file)

        if not secret_data or "server" not in secret_data or "username" not in secret_data or "password" not in secret_data:
            return None

        msg = MIMEMultipart()
        password = secret_data["password"]
        msg['From'] = "support@hrqyzmet.kz"
        msg['To'] = to_email
        msg['Subject'] = head
        if cc_email:
            msg['CC'] = cc_email
        if body:
            msg.attach(MIMEText(body, 'html', 'utf-8'))
        for f_data in files_data:
            part = MIMEApplication(f_data[1], filename=('utf-8', '', f_data[0]))
            part.add_header('Content-Disposition', 'attachment', filename=f_data[0])
            msg.attach(part)

        to_emails_list = [to_email,]
        if cc_email:
            to_emails_list.extend(cc_email.split(','))

        # Отправка сообщения
        server = smtplib.SMTP(f'{secret_data["server"]}: 25')
        server.starttls()
        server.login(secret_data["username"], password)
        server.sendmail(msg['From'], to_emails_list, msg.as_string())
        # server.sendmail(msg['From'], msg['To'], msg.as_string())
        server.quit()
        return "OK"

    def download_file(self, file_id):
        f_info = bitrix.get_file_data(file_id)
        f_url = None
        f_name = None
        if f_info:
            f_url = f_info.get("DOWNLOAD_URL")
            f_name = f_info.get("NAME")

        if f_url:
            f = requests.get(f_url)
            return {
                "f_name": f_name,
                "f_data": f.content
            }

    def get_data_files(self, file_ids):
        res = []
        for file_id in file_ids.split(','):
            data = self.download_file(file_id)
            if data and "f_name" in data and "f_data" in data:
                res.append((data["f_name"], data["f_data"]))
        return res

    def post(self, request):
        email = request.GET.get('email')
        head = request.GET.get('title')
        file_ids = request.GET.get('f_data', '')
        post_type = request.GET.get('post_type')
        cc_email = request.GET.get('email_copy', '')
        if post_type == "1":
             body = html_templates.get_template_1(request.GET)
        if post_type == "2":
             body = html_templates.get_template_2(request.GET)
        if post_type == "3":
             body = html_templates.get_template_3(request.GET)
        if post_type == "4":
             body = html_templates.get_template_4(request.GET)
        if post_type == "5":
             body = html_templates.get_template_5(request.GET)
        #if 'letter' in request.GET:
        #    request.GET['letter'] = unquote(request.GET['letter'])

        # data = self.download_file(file_id)
        # f_data = None
        # f_name = None
        # if data:
        #     f_data = data.get("f_data")
        # if data and data["f_name"]:
        #     f_name = data["f_name"]
        #     # f_name = data["f_name"].encode()
        data = self.get_data_files(file_ids)
        res = self.send_mail(email, head, body, data, cc_email)
        return Response({
            "email": email,
            "head": head,
            "body": body,
            # "f_name": f_name,
            "res": res
        }, status=status.HTTP_201_CREATED)















