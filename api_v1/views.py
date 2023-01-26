from rest_framework import views, viewsets, filters, status, mixins, generics
from rest_framework.response import Response
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
import smtplib
import json
import requests
import logging

from threading import Thread

from .services.queue import EmailsQueue
from .services.workers import ThreadsSendEmail
from api_v1 import secrets
from api_v1 import bitrix
from api_v1 import html_templates


logger_access = logging.getLogger('access')
logger_access.setLevel(logging.INFO)
fh_access = logging.handlers.TimedRotatingFileHandler('./logs/access/access.log', when='D', interval=1, encoding="cp1251", backupCount=7)
formatter_access = logging.Formatter('[%(asctime)s] %(levelname).1s %(message)s')
fh_access.setFormatter(formatter_access)
logger_access.addHandler(fh_access)


COUNT_WORKERS = 1
queue_emails = EmailsQueue(COUNT_WORKERS)
worker_emails = ThreadsSendEmail(queue_emails, COUNT_WORKERS)
worker_emails.create()
worker_emails.start()


class GetSizeQueueEmailsViewSet(views.APIView):
    def get(self, request):
        global queue_emails
        # print(queue_emails.qsize())
        return Response(queue_emails.qsize(), status=status.HTTP_200_OK)


class SendEmailAsyncViewSet(views.APIView):
    def post(self, request):
        global worker_emails
        logger_access.info({
            "request": request.data,
            "params": request.query_params,
        })
        queue_emails.send_queue(request.query_params)
        if not worker_emails:
            worker_emails = ThreadsSendEmail(queue_emails, COUNT_WORKERS)
            worker_emails.create()
            worker_emails.start()
        return Response(True, status=status.HTTP_200_OK)


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
        body = ""
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

        data = self.get_data_files(file_ids)
        res = self.send_mail(email, head, body, data, cc_email)
        return Response({
            "email": email,
            "head": head,
            "body": body,
            "res": res
        }, status=status.HTTP_201_CREATED)















