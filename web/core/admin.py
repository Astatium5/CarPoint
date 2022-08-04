from typing import Literal, Any

from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import *


@admin.register(BotUser)
class BotUser(admin.ModelAdmin):
    fields: list[str] = ["user_id", "first_name", "phone", "city", "username", "name"]
    list_display: list[str] = ["user_id", "first_name", "phone", "get_city"]
    readonly_fields: tuple[Literal["user_id"], Literal["first_name"], Literal["username"]] = ("user_id", "first_name", "username",)
    search_fields: list[str] = ["user_id"]

    def get_city(self, obj) -> Any:
        return obj.city.title

    get_city.short_description = 'Город'


@admin.register(Mark)
class Mark(admin.ModelAdmin):
    fields: list[str] = ["title", "is_visible"]
    list_display: list[str] = ["title", "is_visible"]
    search_fields: list[str] = ["title"]
    list_per_page: int = 15


@admin.register(Model)
class Model(admin.ModelAdmin):
    fields: list[str] = ["mark", "title", "price", "body", "is_visible"]
    list_display: list[str] = ["mark", "title"]
    search_fields: list[str] = ["title"]
    list_per_page: int = 15


@admin.register(Set)
class Set(admin.ModelAdmin):
    fields: list[str] = ["model", "title", "image", "special"]
    list_display: list[str] = ["model", "title"]
    search_fields: list[str] = ["title"]
    list_per_page: int = 15


@admin.register(Engine)
class Engine(admin.ModelAdmin):
    fields: list[str] = ["volume", "power", "type_fuel"]
    list_display: list[str] = ["volume", "power", "type_fuel"]
    search_fields: list[str] = ["volume"]
    list_per_page: int = 15


@admin.register(Transmission)
class Transmission(admin.ModelAdmin):
    fields: list[str] = ["title"]
    list_display: list[str] = ["title"]
    search_fields: list[str] = ["title"]
    list_per_page: int = 15


@admin.register(Wd)
class Wd(admin.ModelAdmin):
    fields: list[str] = ["title"]
    list_display: list[str] = ["title"]
    search_fields: list[str] = ["title"]
    list_per_page: int = 15


@admin.register(City)
class City(admin.ModelAdmin):
    fields: list[str] = ["title", "message"]
    list_display: list[str] = ["title"]
    search_fields: list[str] = ["title"]
    list_per_page: int = 10


@admin.register(Car)
class Car(admin.ModelAdmin):
    fields: list[str] = ["title", "set", "image", "price", "engine", "transmission", "wd", "expenditure", "city", "mark"]
    list_display = ["title", "price", "get_image"]
    list_filter: tuple[Literal['mark']] = ("mark",)
    search_fields = ["title"]
    list_per_page: int = 20

    def get_image(self, obj) -> Any:
        if obj.image:
            return mark_safe(f"<img src='{obj.image}' wdith=70 height=70>")
        else:
            return obj.image

    get_image.short_description = "Изображение"
