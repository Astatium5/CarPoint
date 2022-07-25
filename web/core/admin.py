from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import *

@admin.register(BotUser)
class BotUser(admin.ModelAdmin):
    fields = ["user_id", "first_name", "phone", "city", "username", "name"]
    list_display = ["user_id", "first_name", "phone", "get_city"]
    readonly_fields = ("user_id", "first_name", "username")
    search_fields = ["user_id"]

    def get_city(self, obj):
        return obj.city.title

    get_city.short_description = 'Город'


@admin.register(Mark)
class Mark(admin.ModelAdmin):
    fields = ["title", "is_visible"]
    list_display = ["title", "is_visible"]
    search_fields = ["title"]
    list_per_page = 15


@admin.register(Model)
class Model(admin.ModelAdmin):
    fields = ["mark", "title", "price", "body", "is_visible"]
    list_display = ["mark", "title"]
    search_fields = ["title"]
    list_per_page = 15


@admin.register(Set)
class Set(admin.ModelAdmin):
    fields = ["model", "title", "image", "special"]
    list_display = ["model", "title"]
    search_fields = ["title"]
    list_per_page = 15


@admin.register(Engine)
class Engine(admin.ModelAdmin):
    fields = ["volume", "power", "type_fuel"]
    list_display = ["volume", "power", "type_fuel"]
    search_fields = ["volume"]
    list_per_page = 15


@admin.register(Transmission)
class Transmission(admin.ModelAdmin):
    fields = ["title"]
    list_display = ["title"]
    search_fields = ["title"]
    list_per_page = 15


@admin.register(Wd)
class Wd(admin.ModelAdmin):
    fields = ["title"]
    list_display = ["title"]
    search_fields = ["title"]
    list_per_page = 15


@admin.register(City)
class City(admin.ModelAdmin):
    fields = ["title", "message"]
    list_display = ["title"]
    search_fields = ["title"]
    list_per_page = 10


@admin.register(Car)
class Car(admin.ModelAdmin):
    fields = ["title", "set", "image", "price", "engine", "transmission", "wd", "expenditure", "city", "mark"]
    list_display = ["title", "price", "get_image"]
    search_fields = ["title"]
    list_per_page = 20

    def get_image(self, obj):
        if obj.image:
            return mark_safe(f"<img src='{obj.image}' wdith=70 height=70>")

    get_image.short_description = "Изображение"