import pprint

from .temlates_letter import html as html_template
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
import smtplib
import json
import requests
import time

from . import bitrix
import logging


logger_success = logging.getLogger('success')
logger_success.setLevel(logging.INFO)
fh_success = logging.handlers.TimedRotatingFileHandler('./logs/success/success.log', when='D', interval=1, encoding="cp1251", backupCount=7)
formatter_success = logging.Formatter('[%(asctime)s] %(levelname).1s %(message)s')
fh_success.setFormatter(formatter_success)
logger_success.addHandler(fh_success)

logger_errors = logging.getLogger('errors')
logger_errors.setLevel(logging.INFO)
fh_errors = logging.handlers.TimedRotatingFileHandler('./logs/errors/errors.log', when='D', interval=1, encoding="cp1251", backupCount=7)
formatter_errors = logging.Formatter('[%(asctime)s] %(levelname).1s %(message)s')
fh_errors.setFormatter(formatter_errors)
logger_errors.addHandler(fh_errors)


def send(data):
    email = data.get('email')
    head = data.get('title')
    file_ids = data.get('f_data', '')
    post_type = data.get('post_type')
    cc_email = data.get('email_copy', '')
    body = ""
    f_data = []
    try:
        if post_type == "1":
            body = html_template.get_template_1(data)
        if post_type == "2":
            body = html_template.get_template_2(data)
        if post_type == "3":
            body = html_template.get_template_3(data)
        if post_type == "4":
            body = html_template.get_template_4(data)
        if post_type == "5":
            body = html_template.get_template_5(data)
        f_data = get_data_files_by_ids_in_bx24_(file_ids)
        res = send_mail_(email, head, body, f_data, cc_email)
        # time.sleep(5)
    except Exception as err:
        logger_errors.info({
            "to_email": email,
            "err": err,
            "copy_email": cc_email,
            "head": head,
            "post_type": post_type,
            "f_data": [f_name for f_name, _ in f_data],
            "body": body
        })

    logger_success.info({
        "to_email": email,
        "copy_email": cc_email,
        "head": head,
        "post_type": post_type,
        "f_data": [f_name for f_name, _ in f_data],
        "body": body
    })


# отправка письма
def send_mail_(to_email, head, body, files_data, cc_email):

    with open("api_v1/mail_secrets.json") as secrets_file:
        secret_data = json.load(secrets_file)

    if not secret_data or "server" not in secret_data or "username" not in secret_data or "password" not in secret_data:
        return None

    msg = MIMEMultipart()
    password = secret_data["password"]
    msg['From'] = "support@hrqyzmet.kz"
    msg['To'] = to_email
    msg['Subject'] = head
    # print(msg)
    if cc_email:
        msg['CC'] = cc_email
    if body:
        msg.attach(MIMEText(body, 'html', 'utf-8'))

    # добавление вложений-файлов к письму
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
    return True


# Формирование списка данных файлов
def get_data_files_by_ids_in_bx24_(file_ids):
    res = []
    for file_id in file_ids.split(','):
        if not file_id:
            continue
        data = download_file_from_bx24_(file_id)
        if data and "f_name" in data and "f_data" in data:
            res.append((data["f_name"], data["f_data"]))
    return res


# Скачивание файла из Битрикс
def download_file_from_bx24_(file_id):
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
