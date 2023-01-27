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


# Создание логгера
logger_access = logging.getLogger('access')
logger_access.setLevel(logging.INFO)
fh_access = logging.handlers.TimedRotatingFileHandler('./logs/access/access.log', when='D', interval=1, encoding="cp1251", backupCount=7)
formatter_access = logging.Formatter('[%(asctime)s] %(levelname).1s %(message)s')
fh_access.setFormatter(formatter_access)
logger_access.addHandler(fh_access)


# Количкство параллельно выполняемых работников при асинхронной отправке писем
COUNT_WORKERS = 1

# Создание очереди писем для отправки при асинхронной отправке писем
queue_emails = EmailsQueue(COUNT_WORKERS)

# Создание работников для отправки писем при асинхронной отправке писем
worker_emails = ThreadsSendEmail(queue_emails, COUNT_WORKERS)
worker_emails.create()
worker_emails.start()


# Представление для получения кол-ва писем ожидающих отпрвки
class GetSizeQueueEmailsViewSet(views.APIView):
    def get(self, request):
        global queue_emails
        return Response(queue_emails.qsize(), status=status.HTTP_200_OK)


# Представление для асинхронной отпрвки писем
class SendEmailAsyncViewSet(views.APIView):
    def post(self, request):
        global worker_emails
        # Логгирование входящих запросов
        logger_access.info({
            "request": request.data,
            "params": request.query_params,
        })
        # Добавление данных для отправки письма
        queue_emails.send_queue(request.query_params)
        # Перезапуск работника
        if not worker_emails:
            worker_emails = ThreadsSendEmail(queue_emails, COUNT_WORKERS)
            worker_emails.create()
            worker_emails.start()
        return Response(True, status=status.HTTP_200_OK)


# Представление для синхронной отпрвки писем
class SendEmailViewSet(views.APIView):
    def send_mail(self, to_email, head, body, files_data, cc_email):
        # Чтение секретных данных из файла
        with open("api_v1/mail_secrets.json") as secrets_file:
            secret_data = json.load(secrets_file)

        # Если в файле отсутсвуют секретные данные
        if not secret_data or "server" not in secret_data or "username" not in secret_data or "password" not in secret_data:
            return None

        # Формирование содержимого письма
        msg = MIMEMultipart()
        password = secret_data["password"]
        msg['From'] = "support@hrqyzmet.kz"
        msg['To'] = to_email
        msg['Subject'] = head
        if cc_email:
            msg['CC'] = cc_email
        if body:
            msg.attach(MIMEText(body, 'html', 'utf-8'))

        # Добавление вложений в письмо
        for f_data in files_data:
            part = MIMEApplication(f_data[1], filename=('utf-8', '', f_data[0]))
            part.add_header('Content-Disposition', 'attachment', filename=f_data[0])
            msg.attach(part)

        # Формирование списка emails - получателей сообщения
        to_emails_list = [to_email, ]
        if cc_email:
            to_emails_list.extend(cc_email.split(','))

        # Отправка сообщения
        server = smtplib.SMTP(f'{secret_data["server"]}: 25')
        server.starttls()
        server.login(secret_data["username"], password)
        server.sendmail(msg['From'], to_emails_list, msg.as_string())
        server.quit()
        return "OK"

    # Скачиваие файла из Битрикс по его ID в хранилище
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

    # Получение данных файлов из Битрикс
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
        # Формирование тела письма
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
        # Получение данных файлов вложения в письмо
        data = self.get_data_files(file_ids)
        # Отправка письма
        res = self.send_mail(email, head, body, data, cc_email)
        return Response({
            "email": email,
            "head": head,
            "body": body,
            "res": res
        }, status=status.HTTP_201_CREATED)















