import copy
from typing import Literal, Any

from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import *


@admin.action(description='Клонировать выбранные Автомобили')
def clone_object(modeladmin, request, queryset):
    obj = queryset.get()
    car = copy.copy(obj)
    car.pk = None
    car.save()
    return car


@admin.register(BotUser)
class BotUser(admin.ModelAdmin):
    fields = ["user_id", "first_name", "username", "name", "city"]
    list_display = ["user_id", "first_name", "get_city"]
    readonly_fields = ("user_id", "first_name", "username",)
    search_fields = ["user_id"]
    search_help_text = "Для поиска введите идентификатор пользователя"

    def get_city(self, obj) -> Any:
        if obj.city:
            return obj.city.title

    get_city.short_description = 'Город'


@admin.register(WebUser)
class WebUser(admin.ModelAdmin):
    fields = ["ip_address", "is_blocked"]
    list_display = ["ip_address", "is_blocked"]
    readonly_fields = ("ip_address",)
    search_fields = ["ip_address"]
    search_help_text = "Для поиска введите ip адрес"


@admin.register(Mark)
class Mark(admin.ModelAdmin):
    fields = ["id", "title", "is_visible"]
    list_display = ["title", "id", "is_visible"]
    readonly_fields = ("id",)
    search_fields = ["title"]
    search_help_text = "Для поиска название марки"
    list_per_page: int = 15


@admin.register(Model)
class Model(admin.ModelAdmin):
    fields = ["mark", "title", "price", "body", "is_visible"]
    list_display = ["mark", "title"]
    search_fields = ["title"]
    search_help_text = "Для поиска название модели"
    list_per_page: int = 15


@admin.register(Set)
class Set(admin.ModelAdmin):
    fields = ["model", "title", "image", "special"]
    list_display = ["model", "title"]
    search_fields = ["title"]
    search_help_text = "Для поиска название характеристики"
    list_per_page: int = 15


@admin.register(Engine)
class Engine(admin.ModelAdmin):
    fields = ["volume", "power", "type_fuel"]
    list_display = ["volume", "power", "type_fuel"]
    search_fields = ["volume"]
    search_help_text = "Для поиска значение объема"
    list_per_page: int = 15


@admin.register(Transmission)
class Transmission(admin.ModelAdmin):
    fields = ["title"]
    list_display = ["title"]
    search_fields = ["title"]
    search_help_text = "Для поиска название коробки передач"
    list_per_page: int = 15


@admin.register(Wd)
class Wd(admin.ModelAdmin):
    fields = ["title"]
    list_display = ["title"]
    search_fields = ["title"]
    search_help_text = "Для поиска название привода"
    list_per_page: int = 15


@admin.register(City)
class City(admin.ModelAdmin):
    fields = ["title", "message"]
    list_display = ["title"]
    search_fields = ["title"]
    search_help_text = "Для поиска название города"
    list_per_page: int = 10


@admin.register(Car)
class Car(admin.ModelAdmin):
    fields = ["title", "set", "image", "price", "engine",
              "transmission", "wd", "expenditure", "city", "mark"]
    list_display = ["title", "price", "get_image"]
    list_filter = ("mark",)
    search_fields = ["title"]
    actions = [clone_object]
    search_help_text = "Для поиска введите название автомобиля"
    list_per_page: int = 20

    def get_image(self, obj) -> Any:
        if obj.image:
            return mark_safe(f"<img src='{obj.image}' wdith=70 height=70>")
        else:
            return obj.image

    get_image.short_description = "Изображение"


@admin.register(Entry)
class Entry(admin.ModelAdmin):
    fields = ["user", "username", "car", "email", "name", "address", "phone"]
    list_display = ["id", "user", "email", "name", "address", "phone"]
    search_fields = ["phone"]
    search_help_text = "Для поиска введите номер телефона"
    list_per_page: int = 15


@admin.register(UserQuestion)
class UserQuestion(admin.ModelAdmin):
    fields = ["user", "username", "ip_address", "name", "phone", "question"]
    list_display = ["ip_address", "name", "phone", "question"]
    search_fields = ["name"]
    search_help_text = "Для поиска введите имя пользователя"
    list_per_page: int = 15


@admin.register(Question)
class Question(admin.ModelAdmin):
    fields = ["question", "answer"]
    list_display = ["id", "question", "answer"]
    search_fields = ["question"]
    search_help_text = "Для поиска введите вопрос"
    list_per_page: int = 15


@admin.register(NewCar)
class NewCar(admin.ModelAdmin):
    fields = ["title", "image", "price"]
    list_display = ["title", "get_image", "price"]
    search_fields = ["title"]
    search_help_text = "Для поиска введите название автомобиля"
    list_per_page: int = 15

    def get_image(self, obj) -> Any:
        if obj.image:
            return mark_safe(f"<img src='{obj.image.url}' wdith=70 height=70>")
        else:
            return obj.image

    get_image.short_description = "Изображение"

@admin.register(Color)
class Color(admin.ModelAdmin):
    fields = ["title"]
    list_display = ["title"]
    search_fields = ["title"]
    search_help_text = "Для поиска введите название цвета"
    list_per_page: int = 20

@admin.register(SetColor)
class SetColor(admin.ModelAdmin):
    fields = ["car", "color"]
    list_display = ["car", "color"]

@admin.register(Distributor)
class Distributor(admin.ModelAdmin):
    fields = ["distributor", "title", "image"]
    readonly_fields = ("distributor",)
    list_display = ["distributor", "title", "get_image"]
    search_fields = ["title"]
    search_help_text = "Для поиска введите название дистрибьютора"
    list_per_page: int = 20

    def get_image(self, obj) -> Any:
        if obj.image:
            return mark_safe(f"<img src='{obj.image.url}' wdith=70 height=70>")
        else:
            return obj.image

    get_image.short_description = "Изображение"


@admin.register(AdminEntryFiles)
class AdminEntryFiles(admin.ModelAdmin):
    fields = ["entry", "act", "agreement", "bill"]
    readonly_fields = ("entry",)
    list_display = ["__str__", "entry", "act", "agreement", "bill"]

@admin.register(DistributorEntryFiles)
class DistributorEntryFiles(admin.ModelAdmin):
    fields = ["entry", "act", "agreement", "bill"]
    readonly_fields = ("entry",)
    list_display = ["__str__", "entry", "act", "agreement", "bill"]

@admin.register(SetEntry)
class SetEntry(admin.ModelAdmin):
    fields = ["distributor", "entry", "distributor_file", "admin_file", "status"]
    readonly_fields = ("distributor",)
    list_display = ["__str__", "distributor", "entry", "distributor_file", "admin_file", "status"]

@admin.register(Agreements)
class Agreements(admin.ModelAdmin):
    fields = ["user", "distributor", "agreement"]
    list_display = ["__str__", "get_dealer", "distributor", "agreement"]

    def get_dealer(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return request.user.username

    get_dealer.short_description = "Дилер"

    def get_form(self, request, obj=None, **kwargs):

        form = super().get_form(request, obj, **kwargs)
        user = form.base_fields["user"]
        distributor = form.base_fields['distributor']

        user.widget.can_add_related = False
        user.widget.can_delete_related = False
        user.widget.can_change_related = False

        distributor.widget.can_add_related = False
        distributor.widget.can_delete_related = False
        distributor.widget.can_change_related = False

        return form
