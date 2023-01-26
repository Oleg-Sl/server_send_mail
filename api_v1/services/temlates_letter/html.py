from urllib.parse import unquote, unquote_plus


def url_decode(raw):
    return unquote_plus(raw).replace('\n', '<br>')


def get_template_1(data):
    # letter = unquote_plus(data.get("letter", "")).replace('\n', '<br>')
    return f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta http-equiv="X-UA-Compatible" content="IE=edge">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Document</title>
            <style>
                #container {{
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    align-content: center;
                    font-size: 18px;
                    font-family: sans-serif;
                }}
                #container > div {{
                    margin: 2px;
                }}
                #container > div > img {{
                    width: 250px;
                }}
            </style>
        </head>
        <body>
            <div id="container" style="
    display: flex;
    flex-direction: column;
    align-items: center;
    align-content: center;
    font-size: 18px;
    font-family: sans-serif;
">
                <br>
                <div style="margin:2px;text-align:center">
                    Здравствуйте, <strong>{data.get("name", "")}!</strong>
                </div>
                <br>
                <div style="margin:2px;text-align:center">
                    Ваше обращение зарегистрировано, ему присвоен номер <strong>{data.get("appeal", "")}</strong>
                </div>
                <div style="margin:2px;text-align:center">
                    <strong>Дата регистрации: </strong>{data.get("reg_date", "")}
                </div>
                <div style="margin:2px;text-align:center">
                    <strong>Тема сообщения: </strong>{data.get("head", "")}
                </div>
                <div style="margin:2px;text-align:center">
                    <strong>Суть обращения: </strong>{url_decode(data.get("letter", ""))}
                </div>
                <div style="margin:2px;text-align:center">
                    <strong>Плановое время разрешения: </strong>{data.get("plan_date", "")}
                </div>
                <br>
                <div style="margin:2px;text-align:center">
                    С уважением,
                </div>
                <div style="margin:2px;text-align:center">
                    <strong>Контакт-центр ОЦО HR QYZMET</strong>
                </div>
                <div style="margin:2px;text-align:center">
                    Частное учреждение "Samruk Business Academy"
                </div>
                <br>
                <div style="margin:2px;text-align:center">
                    <img src="https://bitrix24public.com/sba.bitrix24.kz/docs/pub/89195c5197daa45482f5c536a00cc40b/showFile/?&token=ppyxqrbal0w0" alt="">
                </div>
            </div>
        </body>
        </html>
    """


def get_template_2(data):
    return f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta http-equiv="X-UA-Compatible" content="IE=edge">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Document</title>
            <style>
                .container {{
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    align-content: center;
                    font-size: 18px;
                    font-family: sans-serif;
                }}
                .container > div {{
                    margin: 2px;
                }}
                .container > div > img {{
                    width: 250px;
                }}
            </style>
        </head>
        <body>
            <div class="container" style="
    display: flex;
    flex-direction: column;
    align-items: center;
    align-content: center;
    font-size: 18px;
    font-family: sans-serif;
">
                <br>
                <div style="margin:2px;text-align:center">
                    Здравствуйте, <strong>{data.get("name", "")}!</strong>
                </div>
                <br>
                <div style="margin:2px;text-align:center">
                    Вы назначены ответственным по обращению <strong>{data.get("appeal", "")}</strong>
                </div>
                <br>
                <div style="margin:2px;text-align:center">
                    <strong>Тема обращения: </strong>{data.get("head", "")}
                </div>
                <div style="margin:2px;text-align:center">
                    <strong>Суть обращения: </strong>{url_decode(data.get("cl_let", ""))}
                </div>
                <div style="margin:2px;text-align:center">
                    <strong>Дата регистрации: </strong>{data.get("reg_date", "")}
                </div>
                <div style="margin:2px;text-align:center">
                    <strong>Плановое время разрешения: </strong>{data.get("plan_date", "")}
                </div>
                <br>
                <div style="margin:2px;text-align:center">
                    <strong>Контрагент: </strong>{data.get("company", "")}
                </div>
                <div style="margin:2px;text-align:center">
                    <strong>Контакт: </strong>{data.get("contact", "")}
                </div>
                <div style="margin:2px;text-align:center">
                    <strong>Рабочий телефон: </strong>{data.get("work_phone", "")}
                </div>
                <div style="margin:2px;text-align:center">
                    <strong>Мобильный телефон: </strong>{data.get("mob_phone", "")}
                </div>
                <div style="margin:2px;text-align:center">
                    <strong>Email: </strong>{data.get("cl_email", "")}
                </div>
                <br>
                <div style="margin:2px;text-align:center">
                    Просим по факту отработки запроса, ответить через форму по <a href="{data.get("link", "")}" target="_blank">ссылке</a>
                <br>
                <div style="margin:2px;text-align:center">
                    С уважением, {data.get("op_name", "")}
                </div>
                <div style="margin:2px;text-align:center">
                    <strong>Контакт-центр ОЦО HR QYZMET</strong>
                </div>
                <div style="margin:2px;text-align:center">
                    Частное учреждение "Samruk Business Academy"
                </div>
                <br>
                <div style="margin:2px;text-align:center">
                    <img src="https://bitrix24public.com/sba.bitrix24.kz/docs/pub/89195c5197daa45482f5c536a00cc40b/showFile/?&token=ppyxqrbal0w0" alt="">
                </div>
            </div>
        </body>
        </html>
    """


def get_template_3(data):
    return f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta http-equiv="X-UA-Compatible" content="IE=edge">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Document</title>
            <style>
                .container {{
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    align-content: center;
                    font-size: 18px;
                    font-family: sans-serif;
                }}
                .container > div {{
                    margin: 2px;
                }}
                .container > div > img {{
                    width: 250px;
                }}
            </style>
        </head>
        <body>
            <div class="container" style="
    display: flex;
    flex-direction: column;
    align-items: center;
    align-content: center;
    font-size: 18px;
    font-family: sans-serif;
">
                <br>
                <div style="margin:2px;text-align:center">
                    Здравствуйте, <strong>коллеги!</strong>
                </div>
                <br>
                <div style="margin:2px;text-align:center">
                    Уведомляем Вас о том, что по обращению {data.get("appeal", "")}
                </div>
                <div style="margin:2px;text-align:center">
                    <strong>осталось 2 рабочих часа до окончания планового времени разрешения.</strong>
                </div>
                <br>
                <div style="margin:2px;text-align:center">
                    <strong>Тема обращения: </strong>{data.get("head", "")}
                </div>
                <div style="margin:2px;text-align:center">
                    <strong>Суть обращения: </strong>{url_decode(data.get("cl_let", ""))}
                </div>
                <div style="margin:2px;text-align:center">
                    <strong>Дата регистрации: </strong>{data.get("reg_date", "")}
                </div>
                <div style="margin:2px;text-align:center">
                    <strong>Плановое время разрешения: </strong>{data.get("plan_date", "")}
                </div>
                <div style="margin:2px;text-align:center">
                    <strong>Ответственный менеджер 2-й линии: </strong>{data.get("assign", "")}
                </div>
                <br>
                <div style="margin:2px;text-align:center">
                    <strong>Контрагент: </strong>{data.get("company", "")}
                </div>
                <div style="margin:2px;text-align:center">
                    <strong>Контакт: </strong>{data.get("contact", "")}
                </div>
                <div style="margin:2px;text-align:center">
                    <strong>Рабочий телефон: </strong>{data.get("work_phone", "")}
                </div>
                <div style="margin:2px;text-align:center">
                    <strong>Мобильный телефон: </strong>{data.get("mob_phone", "")}
                </div>
                <div style="margin:2px;text-align:center">
                    <strong>Email: </strong>{data.get("cl_email", "")}
                </div>
                <br>
                <div style="margin:2px;text-align:center">
                    Просим по факту отработки запроса, ответить через форму по <a href="{data.get("link", "")}" target="_blank">ссылке</a>
                </div>
                <br>
                <div style="margin:2px;text-align:center">
                    С уважением, {data.get("op_name", "")}
                </div>
                <div style="margin:2px;text-align:center">
                    <strong>Контакт-центр ОЦО HR QYZMET</strong>
                </div>
                <div style="margin:2px;text-align:center">
                    Частное учреждение "Samruk Business Academy"
                </div>
                <br>
                <div style="margin:2px;text-align:center">
                    <img src="https://bitrix24public.com/sba.bitrix24.kz/docs/pub/89195c5197daa45482f5c536a00cc40b/showFile/?&token=ppyxqrbal0w0" alt="">
                </div>
            </div>
        </body>
        </html>
    """


def get_template_4(data):
    return f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta http-equiv="X-UA-Compatible" content="IE=edge">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Document</title>
            <style>
                .container {{
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    align-content: center;
                    font-size: 18px;
                    font-family: sans-serif;
                }}
                .container > div {{
                    margin: 2px;
                }}
                .container > div > img {{
                    width: 250px;
                }}
            </style>
        </head>
        <body>
            <div class="container" style="
    display: flex;
    flex-direction: column;
    align-items: center;
    align-content: center;
    font-size: 18px;
    font-family: sans-serif;
">
                <br>
                <div style="margin:2px;text-align: center;">
                    Здравствуйте, <strong>{data.get("name", "")}!</strong>
                </div>
                <br>
                <div style="margin:2px;text-align: center;">
                    По вашему обращению <strong>{data.get("appea", "")}</strong> "{data.get("head", "")}" <strong>подготовлено решение:</strong>
                </div>
                <div style="margin:2px;text-align: center;">
                    {url_decode(data.get("res", ""))}
                </div>
                <br>
                <div style="margin:2px;text-align: center;">
                    <strong>Фактическое время разрешения: </strong>{data.get("fact_date", "")}
                </div>
                <br>
                <div style="margin:2px;text-align: center;">
                    Если предоставленное решение не принесло ожидаемого результата, пожалуйста, ответьте на данное письмо.
                </div>
                <br>
                <div style="margin:2px;text-align: center;">
                    Пожалуйста,оцените <strong>качество предоставленного решения по </strong><a href="{data.get("link", "")}&utm_medium=feedback" target="_blank">ссылке</a>
                </div>
                <br>
                <div style="margin:2px;text-align: center;">
                    С уважением,
                </div>
                <div style="margin:2px;text-align: center;">
                    <strong>Контакт-центр ОЦО HR QYZMET</strong>
                </div>
                <div style="margin:2px;text-align: center;">
                    Частное учреждение "Samruk Business Academy"
                </div>
                <br>
                <div style="margin:2px;text-align: center;">
                    <img src="https://bitrix24public.com/sba.bitrix24.kz/docs/pub/89195c5197daa45482f5c536a00cc40b/showFile/?&token=ppyxqrbal0w0" alt="">
                </div>
            </div>
        </body>
        </html>
    """




def get_template_5(data):
    return f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta http-equiv="X-UA-Compatible" content="IE=edge">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Document</title>
            <style>
                .container {{
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    align-content: center;
                    font-size: 18px;
                    font-family: sans-serif;
                }}
                .container > div {{
                    margin: 2px;
                }}
                .container > div > img {{
                    width: 250px;
                }}
            </style>
        </head>
        <body>
            <div class="container" style="
            display: flex;
            flex-direction: column;
            align-items: center;
            align-content: center;
            font-size: 18px;
            font-family: sans-serif;
            ">
                <br>
                <div style="margin:2px;text-align:center">
                    {data.get("res", "")}
                </div>
                <br>
                <div style="margin:2px;text-align: center;">
                    С уважением,
                </div>
                <div style="margin:2px;text-align: center;">
                    <strong>Контакт-центр ОЦО HR QYZMET</strong>
                </div>
                <div style="margin:2px;text-align: center;">
                    Частное учреждение "Samruk Business Academy"
                </div>
                <br>
                <div style="margin:2px;text-align: center;">
                    <img src="https://bitrix24public.com/sba.bitrix24.kz/docs/pub/89195c5197daa45482f5c536a00cc40b/showFile/?&token=ppyxqrbal0w0" alt="">
                </div>
            </div>
        </body>
        </html>
    """







