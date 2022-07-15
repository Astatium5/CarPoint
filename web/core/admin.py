from django.contrib import admin

from .models import *

@admin.register(BotUser)
class BotUser(admin.ModelAdmin):
    fields = ["user_id", "first_name", "phone", "city", "username", "name"]
    list_display = ["user_id", "first_name", "phone", "get_city"]
    readonly_fields = ("user_id", "first_name", "username")

    def get_city(self, obj):
        return obj.city.title

    get_city.short_description = 'Город'


@admin.register(Mark)
class Mark(admin.ModelAdmin):
    fields = ["title", "is_visible"]
    list_display = ["title", "is_visible"]
    list_per_page = 15
    search_fields = ["title"]


@admin.register(Model)
class Model(admin.ModelAdmin):
    fields = ["mark", "title", "price", "body", "is_visible"]
    list_display = ["mark", "title"]


@admin.register(Set)
class Set(admin.ModelAdmin):
    fields = ["model", "title", "image", "special"]
    list_display = ["model", "title"]


@admin.register(Engine)
class Engine(admin.ModelAdmin):
    fields = ["volume", "power", "type_fuel"]
    list_display = ["volume", "power"]


@admin.register(Transmission)
class Transmission(admin.ModelAdmin):
    fields = ["title"]
    list_display = ["title"]


@admin.register(Wd)
class Wd(admin.ModelAdmin):
    fields = ["title"]
    list_display = ["title"]


@admin.register(City)
class City(admin.ModelAdmin):
    fields = ["title", "message"]
    list_display = ["title"]
    list_per_page = 10
    search_fields = ["title"]


@admin.register(Car)
class Car(admin.ModelAdmin):
    fields = ["title", "set_id", "image", "price", "engine_id", "transmission_id", "wd_id", "expenditure", "city_id", "mark_id"]
    list_display = ["title", "price"]