from rest_framework import serializers
from django.db import models
from django.db.models.functions import Coalesce
from datetime import datetime, timedelta, timezone

from statisticsapp.models import (Department,
                                  User,
                                  Direction,
                                  Stage,
                                  Company,
                                  Deal)

from cashflowapp.models import (TemplateParsing, TypeActivity, Items, Companies, Payment, )


class RecursiveSerializer(serializers.Serializer):
    def to_representation(self, instance):
        serializer = self.parent.parent.__class__(instance, context=self.context)
        return serializer.data


# class FilterDepartmentSerializer(serializers.ListSerializer):
#     def to_representation(self, data):
#         data = data.first()
#         return super().to_representation(data)


class DepartmentSerializer(serializers.ModelSerializer):
    parent_dep = RecursiveSerializer(many=True)

    class Meta:
        # list_serializer_class = FilterDepartmentSerializer
        model = Department
        fields = ('id_bx', 'name', 'head', 'parent_dep')
        # fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    url = serializers.URLField(read_only=True)

    class Meta:
        model = User
        fields = '__all__'


class DirectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Direction
        fields = '__all__'


class StageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Stage
        fields = '__all__'


class CompanySerializer(serializers.ModelSerializer):
    url = serializers.URLField(read_only=True)
    # active = serializers.BooleanField(read_only=True)

    class Meta:
        model = Company
        fields = '__all__'


class DealSerializer(serializers.ModelSerializer):
    url = serializers.URLField(read_only=True)
    # stage = serializers.IntegerField(read_only=True)
    # stage = StageSerializer(read_only=True)
    # active = serializers.BooleanField(read_only=True)
    date_last_communication = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Deal
        fields = '__all__'




class DealStatisticSerializer(serializers.ModelSerializer):
    url = serializers.URLField(read_only=True)
    opportunity = serializers.DecimalField(max_digits=999999999, decimal_places=2, read_only=True)

    class Meta:
        model = Deal
        fields = ["id_bx", "title", "url", "closed", "date_last_communication", "date_modify", "opportunity"]


class DirectionStatisticSerializer(serializers.ModelSerializer):
    # deals = serializers.SerializerMethodField(source='get_deals', read_only=True)
    summa_by_direction_success = serializers.SerializerMethodField(source='get_summa_by_direction_success', read_only=True)
    summa_by_direction_work = serializers.SerializerMethodField(source='get_summa_by_direction_work', read_only=True)
    # summa_by_direction_success = serializers.IntegerField(read_only=True)
    # summa_by_direction_work = serializers.IntegerField(read_only=True)
    date_last_communication = serializers.SerializerMethodField(source='get_date_last_communication', read_only=True)
    # date_last_modify = serializers.SerializerMethodField(source='get_date_last_modify', read_only=True)
    status_summa_by_direction_work = serializers.SerializerMethodField(
        source='get_status_summa_by_direction_work', read_only=True
    )

    class Meta:
        model = Direction
        fields = ["id_bx", "name", "summa_by_direction_success", "summa_by_direction_work",
                  "status_summa_by_direction_work", "date_last_communication"]

    def get_deals(self, obj):
        return DealStatisticSerializer(obj.dea, many=True, read_only=True).data

    def get_summa_by_direction_success(self, obj):
        summa = [deal.opportunity or 0 for deal in obj.dea
                 if deal.closed is True and     # сделка закрыта
                    deal.active is True and     # сделка не удалена из BX24
                    deal.won is True            # сделка успешно заверешена
        ]
        return int(sum(summa))

    def get_summa_by_direction_work(self, obj):
        # arr_stage = ['C43:7', 'C43:1', 'C43:2', 'C43:9', 'C43:11']
        summa = [deal.opportunity or 0 for deal in obj.dea
                 if deal.closed is False and        # сделка не закрыта
                    deal.active is True and         # сделка не удалена из BX24
                    deal.status == "1"              # сделка имеет статус "в работе"
                    # deal.abbrev in ['C43:7', 'C43:1', 'C43:2', 'C43:9', 'C43:11'] # сделка находиттся на данных стадиях
        ]
        return int(sum(summa))

    def get_date_last_communication(self, obj):
        date = [deal.date_last_communication for deal in obj.dea
                if deal.date_last_communication is not None and     # дата ДПК заполнена
                   deal.active is True                              # сделка не удалена из BX24
                ]
        if date:
            return max(date)

    def get_date_last_modify(self, obj):
        date_modify_limit = datetime.now(timezone.utc) - timedelta(days=183)    # предельная допустимая дата изменения сделки - за пол года до текущей даты
        # print("date_modify_limit = ", date_modify_limit)
        # dir = self.context.get("request", {}).query_params.get("direction", None)
        date = [deal.date_modify for deal in obj.dea
                if deal.date_modify is not None and     # дата последнего изменения сделки заполнена
                deal.closed is False and                # сделка не закрыта
                deal.active is True and                 # сделка не удалена из BX24
                deal.status == "0" and                    # сделка имеет статус "подготовка к работе"
                # deal.abbrev in ["C43:NEW", "C43:PREPARATION", "C43:PREPAYMENT_INVOICE", "C43:EXECUTING", "C43:8", "C43:10"] and
                # находится на стадиях подготовки (ещё не в работе)
                # deal.abbrev in ['C43:7', 'C43:1', 'C43:2', 'C43:9', 'C43:11'] and

                deal.date_modify > date_modify_limit    # с даты последней модификации сделки прошло не более полугода
        ]
        # print("date_modify_limit = ", date_modify_limit)
        # print("date = ", date)
        if date:
            return max(date)
        else:
            return False

    def get_status_summa_by_direction_work(self, obj):
        date_modify_limit = datetime.now(timezone.utc) - timedelta(
            days=183)  # предельная допустимая дата изменения сделки - за пол года до текущей даты
        # сделки в работе
        deal_work = [deal for deal in obj.dea
                     if deal.closed is False and        # сделка не закрыта
                     deal.active is True and            # сделка не удалена из BX24
                     deal.status == "1"                 # сделка имеет статус "подготовка к работе"
                     ]
        # сделки на стадии "подготовка к работе" и с даты изменения сделки прошло не более полугода
        deal_preparation = [deal for deal in obj.dea
                if deal.date_modify is not None and     # дата последнего изменения сделки заполнена
                deal.closed is False and                # сделка не закрыта
                deal.active is True and                 # сделка не удалена из BX24
                deal.status == "0" and                  # сделка имеет статус "подготовка к работе"

                deal.date_modify > date_modify_limit    # с даты последней модификации сделки прошло не более полугода
                ]

        if deal_work:
            return 2        # есть сделки в работе
        if deal_preparation:
            return 1        # есть не просроченные сделки на подготовке к работе

        return 0            # нет сделок


class StatisticSerializer(serializers.ModelSerializer):
    responsible_name = serializers.StringRelatedField(source='responsible.name', read_only=True)
    responsible_lastname = serializers.StringRelatedField(source='responsible.lastname', read_only=True)
    responsible_url = serializers.StringRelatedField(source='responsible.url', read_only=True)
    # responsible_profession = serializers.StringRelatedField(source='responsible.work_position', read_only=True)
    # responsible_photo = serializers.StringRelatedField(source='responsible.photo', read_only=True)
    # responsible_id = serializers.StringRelatedField(source='responsible.id_bx', read_only=True)

    direction = serializers.SerializerMethodField(source='get_direction', read_only=True)

    summa_by_company_success = serializers.IntegerField(read_only=True)
    summa_by_company_work = serializers.IntegerField(read_only=True)
    date_last_communication = serializers.DateTimeField()

    class Meta:
        model = Company
        fields = ["id_bx", "name", "url", "inn", "responsible_name", "responsible_lastname",
                  "responsible_url", "date_last_communication",
                  "summa_by_company_success", "summa_by_company_work", "direction"]

    def get_direction(self, obj):
        dir = self.context.get("request", {}).query_params.get("direction", None)
        deals = Deal.objects.filter(
            company=obj,  # сделки компании obj
            active=True,  # сделка не удалена из BX24
        ).annotate(
            won=models.F("stage__won"),         # добавляем поле сделка завершена успешно
            abbrev=models.F("stage__abbrev"),   # добавляем поле аббревиатура стадии в сделке
            status=models.F("stage__status"),   # добавляем поле статус стадии в сделке
        )
        if dir:
            deals = deals.filter(direction__in=dir.split(","))

        directions = Direction.objects.prefetch_related(
            models.Prefetch('deal', queryset=deals, to_attr="dea")
        ).filter(new=True).order_by("id_bx")
        if dir:
            directions = directions.filter(id_bx__in=dir.split(","))

        # if dir:
        #     deals = Deal.objects.filter(
        #         company=obj,                        # сделки компании obj
        #         active=True,                        # сделка не удалена из BX24
        #         direction__in=dir.split(",")        # сделка имеет направление переданное в параметрах
        #     ).annotate(
        #         won=models.F("stage__won"),         # добавляем поле сделка завершена успешно
        #         abbrev=models.F("stage__abbrev"),   # добавляем поле аббревиатура стадии к сделке
        #     )
        #     directions = Direction.objects.prefetch_related(
        #         models.Prefetch('deal', queryset=deals, to_attr="dea")
        #     ).filter(new=True, id_bx__in=dir.split(",")).order_by("id_bx")
        # else:
        #     deals = Deal.objects.filter(
        #         company=obj,                        # сделки компании obj
        #         active=True,                        # сделка не удалена из BX24
        #     ).annotate(
        #         won=models.F("stage__won"),
        #         abbrev=models.F("stage__abbrev"),
        #     )
        #     directions = Direction.objects.prefetch_related(
        #         models.Prefetch('deal', queryset=deals, to_attr="dea")
        #     ).filter(new=True).order_by("id_bx")

        return DirectionStatisticSerializer(directions, many=True, read_only=True).data




    # def get_direction_all(self, obj):
    #     # print("obj.direct =>>> ", obj.direct)
    #     # print("len(obj.direct) =>>> ", len(obj.direct))
    #     # if obj.direct:
    #     #     print("obj.direct.dea = ", obj.direct[12].dea)
    #     # return 111
    #     return CompanyDirectionStatisticSerializer(obj.direct, many=True, read_only=True).data








































class TemplateParsingSerializer(serializers.ModelSerializer):

    class Meta:
        model = TemplateParsing
        fields = '__all__'


class TypeActivitySerializer(serializers.ModelSerializer):
    items = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = TypeActivity
        fields = '__all__'


class ItemsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Items
        fields = '__all__'


class CompanieSerializer(serializers.ModelSerializer):
    balance = serializers.DecimalField(max_digits=14, decimal_places=2, read_only=True)
    # balance = serializers.FloatField(max_digits=14, decimal_places=2, read_only=True)

    class Meta:
        model = Companies
        fields = '__all__'


class PaymentSerializer(serializers.ModelSerializer):
    d_c = serializers.CharField(source='item.type', read_only=True)

    class Meta:
        model = Payment
        exclude = ["plat_inn", "pol_inn"]








# Вложенный серриализатор сводной таблицы
class SummaryItemsSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    type = serializers.CharField()
    amount_by_items = serializers.FloatField()
    name = serializers.CharField()

    class Meta:
        model = Items
        fields = ["id", "type", "amount_by_items", "name"]


# Серриализатор сводной таблицы
class SummarySerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    items = SummaryItemsSerializer(many=True, read_only=True)
    amount = serializers.FloatField()

    class Meta:
        model = TypeActivity
        fields = '__all__'


#
class SummaryBalanceSerializer(serializers.ModelSerializer):
    balance_start_month = serializers.DecimalField(max_digits=14, decimal_places=2)
    balance_end_month = serializers.DecimalField(max_digits=14, decimal_places=2)
    amount_start_pol = serializers.DecimalField(max_digits=14, decimal_places=2)
    # amount_start_plat = serializers.DecimalField(max_digits=14, decimal_places=2)
    amount_end_pol = serializers.DecimalField(max_digits=14, decimal_places=2)
    # amount_end_plat = serializers.DecimalField(max_digits=14, decimal_places=2)

    class Meta:
        model = Companies
        fields = ['id', 'name', 'date_balance', 'money', 'balance_start_month', 'balance_end_month', 'amount_start_pol', 'amount_end_pol', ]
