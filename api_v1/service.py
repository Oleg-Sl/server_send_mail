import requests
from django_filters import rest_framework as filters


from statisticsapp.models import (Department,
                                  User,
                                  Direction,
                                  Stage,
                                  Company,
                                  Deal)


# url для запроса к BX24
URL_BATCH = "https://atonlab.bitrix24.ru/rest/2479/w5633kgubg2zwanm/batch.json"


def execute_request(url, data):
    """Выполнение batch запроса к Bitrix
    url: str - url-адрес
    data: json - тело запроса в json формате
    return: JSON.object - ответ при уддачном запросе,
            none - при неудачном запросе
    """
    try:
        response = requests.post(url, json=data)
    except requests.exceptions.ReadTimeout:
        print('Oops. Read timeout occured')
    except requests.exceptions.ConnectTimeout:
        print('Oops. Connection timeout occured!')
    except requests.exceptions.ConnectionError:
        print('Seems like dns lookup failed..')
    except requests.exceptions.HTTPError as err:
        print('Oops. HTTP Error occured')
        print('Response is: {content}'.format(content=err.response.content))
    else:
        data_json = response.json()
        if response.status_code == 200:
            return data_json['result']


def get_data_company(id_company):
    """ Запрос к BX24 на получение данных компании по ее ID """
    inn = None
    response = execute_request(
        URL_BATCH,
        {
            "halt": 0,
            "cmd": {
                "DATA": f"crm.company.get?id={id_company}",
                "REQUISITES": f"crm.requisite.list?filter[ENTITY_ID]={id_company}&filter[ENTITY_TYPE_ID]=4&select[0]=RQ_INN"
            }
        }
    )

    if not response.get("result", None):
        # если ответ от BX24 не содержит результата
        return None

    company = response["result"].get("DATA", {})
    requisites_company = response["result"].get("REQUISITES", [])
    if requisites_company:
        # если у компании в BX24 заполнены реквизиты
        inn = requisites_company[0].get("RQ_INN", None)
    company["INN"] = inn or None
    return company


def get_data_deal(id_deal):
    response = execute_request(
        URL_BATCH,
        {
            "halt": 0,
            "cmd": {
                "DATA": f"crm.deal.get?id={id_deal}"},
        }
    )

    if not response["result"]:
        # если ответ от BX24 не содержит результата
        return None

    deal = response["result"].get("DATA", {})
    return deal


def get_data_activity(id_activity):
    response = execute_request(
        URL_BATCH,
        {
            "halt": 0,
            "cmd": {
                "DATA": f"crm.activity.get?id={id_activity}",
            }
        }
    )

    if not response["result"]:
        # если ответ от BX24 не содержит результата
        return None

    activity = response["result"].get("DATA", None)
    return activity







class CompanyIdFilter(filters.RangeFilter, filters.DateFilter):
    pass

class NumberInFilter(filters.BaseInFilter, filters.NumberFilter):
    pass


class StatisticDataFilter(filters.FilterSet):
    # date = DateRangeFilter(field_name="date", lookup_expr="range")
    date = filters.DateFromToRangeFilter()
    summa_by_company = filters.RangeFilter()
    company = NumberInFilter(field_name='pk', lookup_expr='in')
    responsible = NumberInFilter(field_name='responsible__pk', lookup_expr='in')

    class Meta:
        model = Company
        fields = ["date", "summa_by_company", "company", "responsible"]


class UserDataFilter(filters.FilterSet):
    work_position = filters.BaseInFilter(lookup_expr='in')
    department = filters.BaseInFilter(field_name='department__id_bx', lookup_expr='in')

    class Meta:
        model = User
        fields = ["work_position", "department", "active"]


class DirectionDataFilter(filters.FilterSet):
    # work_position = filters.BaseInFilter(lookup_expr='in')

    class Meta:
        model = Direction
        fields = ["id_bx", "new"]


class DealDataFilter(filters.FilterSet):
    # work_position = filters.BaseInFilter(lookup_expr='in')

    class Meta:
        model = Deal
        fields = ["company", "direction", "closed"]


class DepartmentDataFilter(filters.FilterSet):

    class Meta:
        model = Department
        fields = ["id_bx", ]


