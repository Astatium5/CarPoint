from os.path import splitext
from uuid import uuid4
from enum import Enum

from django.utils import timezone
from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage


class UUIDFileStorage(FileSystemStorage):
    def get_available_name(self, name, max_length=None) -> str:
        _, ext = splitext(name)
        return F"{settings.MEDIA_ROOT}/profile_pictures/{uuid4().hex + ext}"


class CSVFileStorage(FileSystemStorage):
    def get_available_name(self, name, max_length=None) -> str:
        _, ext = splitext(name)
        return F"{settings.MEDIA_ROOT}/csv/{uuid4().hex + ext}"


class DistributorFileStorage(FileSystemStorage):
    def get_available_name(self, name, max_length=None) -> str:
        _, ext = splitext(name)
        return F"{settings.MEDIA_ROOT}/files/distributor/{uuid4().hex + ext}"


class AdminFileStorage(FileSystemStorage):
    def get_available_name(self, name, max_length=None) -> str:
        _, ext = splitext(name)
        return F"{settings.MEDIA_ROOT}/files/admin/{uuid4().hex + ext}"


class DealerFileStorage(FileSystemStorage):
    def get_available_name(self, name: str, max_length=None) -> str:
        _, ext = splitext(name)
        return F"{settings.MEDIA_ROOT}/files/agreements/{uuid4().hex + ext}"


class BotUser(models.Model):
    user_id = models.BigIntegerField(
        unique=True, verbose_name="Индент. пользователя")
    first_name = models.CharField(max_length=255, verbose_name="Имя аккаунта")
    phone = models.BigIntegerField(null=True, verbose_name="Телефон")
    city = models.ForeignKey(
        'City', on_delete=models.PROTECT, null=True, verbose_name="Город")
    username = models.CharField(
        max_length=255, null=True, verbose_name="Имя пользователя")
    name = models.CharField(max_length=255, null=True,
                            verbose_name="Имя пользователя (заполненное)")

    def __str__(self):
        return F"Пользователь #{self.id}"

    class Meta:
        verbose_name = "Пользователь бота"
        verbose_name_plural = "Пользователи бота"


class WebUser(models.Model):
    ip_address = models.GenericIPAddressField(verbose_name="IP адрес")
    is_blocked = models.BooleanField(default=False, verbose_name="Блокировка")

    class Meta:
        verbose_name = "Пользователь сайта"
        verbose_name_plural = "Пользователи сайта"


class Distributor(models.Model):
    distributor = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name="Дистрибьютор")
    title = models.CharField(max_length=255, verbose_name="Название")
    image = models.ImageField(
        upload_to="distributor/profile_images/", storage=UUIDFileStorage(), null=True, verbose_name="Логотип")

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = "Дистрибьютор"
        verbose_name_plural = "Дистрибьюторы"


class Mark(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название")
    is_visible = models.BooleanField(verbose_name="Отображается")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Марка"
        verbose_name_plural = "Марки"
        ordering = ['title']


class Model(models.Model):
    mark = models.ForeignKey(
        Mark, on_delete=models.PROTECT, verbose_name="Идент. марки")
    title = models.CharField(max_length=255, verbose_name="Название")
    price = models.BigIntegerField(verbose_name="Цена")
    body = models.CharField(max_length=255, verbose_name="Тело")
    is_visible = models.BooleanField(verbose_name="Отображается")

    def __str__(self):
        return self.body

    class Meta:
        verbose_name = "Модель"
        verbose_name_plural = "Модели"


class Set(models.Model):
    model = models.ForeignKey(
        Model, on_delete=models.PROTECT, verbose_name="Модель")
    title = models.CharField(
        max_length=255, verbose_name="Название", unique=False)
    image = models.URLField(verbose_name="Ссылка на картинку")
    special = models.TextField(verbose_name="Конфигурации")

    def __str__(self):
        return self.model.body

    class Meta:
        verbose_name = "Характеристика"
        verbose_name_plural = "Характеристики"


class Engine(models.Model):
    volume = models.FloatField(verbose_name="Значение", null=True)
    power = models.IntegerField(verbose_name="Мощность", null=True)
    type_fuel = models.CharField(
        max_length=255, verbose_name="Тип топлива", null=True)

    def to_dict(self):
        return dict(volume=self.volume, power=self.power, type_fuel=self.type_fuel)

    def __str__(self):
        return F"{self.volume} - {self.power}"

    class Meta:
        verbose_name = "Двигатель"
        verbose_name_plural = "Двигатели"


class Transmission(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Трансмиссия"
        verbose_name_plural = "Трансмиссии"


class Wd(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Привод"
        verbose_name_plural = "Приводы"


class City(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название")
    message = models.TextField(verbose_name="Сообщение")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Город"
        verbose_name_plural = "Города"
        ordering = ['title']


class Car(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название")
    set = models.ForeignKey(Set, on_delete=models.PROTECT, verbose_name="Тип кузова")
    image = models.URLField(verbose_name="Картинка")
    price = models.FloatField(verbose_name="Цена")
    engine = models.ForeignKey(
        Engine, on_delete=models.PROTECT, verbose_name="Двигатель")
    transmission = models.ForeignKey(
        Transmission, on_delete=models.PROTECT, verbose_name="Трансмиссия")
    wd = models.ForeignKey(Wd, on_delete=models.PROTECT, verbose_name="Привод")
    expenditure = models.CharField(max_length=255, null=True, verbose_name="Расход")
    city = models.ForeignKey(
        City, on_delete=models.PROTECT, null=True, verbose_name="Город")
    mark = models.ForeignKey(
        Mark, on_delete=models.PROTECT, verbose_name="Марка")

    def to_dict(self):
        return dict(
            id=self.id, title=self.title, price=self.price, image=self.image, mark_id=self.mark_id, engine = self.engine.to_dict(),
            wd=self.wd.title, expenditure=self.expenditure, transmission=self.transmission.title, special=self.set.special,
            body=self.set.model.body, set_title=self.set.title, model_title=self.set.model.title)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Автомобиль"
        verbose_name_plural = "Автомобили"


class Color(models.Model):
    title = models.CharField(max_length=128, verbose_name="Цвет")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Цвет"
        verbose_name_plural = "Цвета"


class Entry(models.Model):
    user = models.ForeignKey(
        BotUser, null=True, on_delete=models.PROTECT, verbose_name="Пользователь")
    username = models.CharField(
        max_length=255, null=True, verbose_name="Имя пользователя")
    car = models.ForeignKey(Car, on_delete=models.PROTECT,
                            verbose_name="Автомобиль")
    email = models.CharField(max_length=255, verbose_name="Почта")
    name = models.CharField(max_length=255, verbose_name="Имя")
    address = models.CharField(max_length=255, verbose_name="Адрес")
    phone = models.BigIntegerField(verbose_name="Телефон")
    created = models.DateTimeField(default=timezone.now, verbose_name="Дата и время создания")

    def __str__(self):
        return f"Заявка #{self.id}"

    class Meta:
        verbose_name = "Заявка"
        verbose_name_plural = "Заявки"


class SetEntry(models.Model):
    class STATUS(Enum):
        new = ("new", "Ожидает")
        shipped = ("shipped", "Отгружен")
        road = ("road", "В пути")
        client = ("client", "Передан клиенту")
        payment = ("payment", "Ожидает оплаты")
        complete = ("complete", "Закрыто")

        @classmethod
        def get_value(cls, member):
            return cls[member].value[0]

    distributor = models.ForeignKey(Distributor, on_delete=models.PROTECT, verbose_name="Дистрибьютор")
    entry = models.ForeignKey(Entry, on_delete=models.PROTECT, verbose_name="Заявка")
    distributor_file = models.ForeignKey('DistributorEntryFiles', on_delete=models.SET_NULL, null=True, verbose_name="Файлы дистрибьютора")
    admin_file = models.ForeignKey('AdminEntryFiles', on_delete=models.SET_NULL, null=True, verbose_name="Файлы админа")
    status = models.CharField(max_length=32, choices=[x.value for x in STATUS], default=STATUS.get_value("new"), verbose_name="Статус заявки")

    def to_dict(self, is_distributor=False):
        if is_distributor:
            return dict(car=self.entry.car.to_dict())

    def __str__(self):
        return f"Заявка дистрибьютора #{self.id}"

    class Meta:
        verbose_name = "Заявка дистрибьютора"
        verbose_name_plural = "Заявки дистрибьюторов"


class UserQuestion(models.Model):
    user = models.ForeignKey(
        BotUser, null=True, on_delete=models.PROTECT, verbose_name="Пользователь сайта"
    )
    username = models.CharField(
        max_length=255, null=True, verbose_name="Имя пользователя")
    ip_address = models.GenericIPAddressField(null=True, verbose_name="IP адрес")
    name = models.CharField(max_length=255, verbose_name="Имя")
    phone = models.BigIntegerField(verbose_name="Телефон")
    question = models.TextField(verbose_name="Вопрос")

    class Meta:
        verbose_name = "Вопрос пользователя"
        verbose_name_plural = "Вопросы пользователей"


class Question(models.Model):
    question = models.TextField(verbose_name="Вопрос")
    answer = models.TextField(verbose_name="Ответ")

    class Meta:
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы"


class NewCar(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название")
    image = models.ImageField(verbose_name="Картинка")
    price = models.FloatField(verbose_name="Цена")

    class Meta:
        verbose_name = "Новинка"
        verbose_name_plural = "Новинки"


class SetEngine(models.Model):
    set = models.ForeignKey(Set, on_delete=models.PROTECT)
    engine = models.ForeignKey(Engine, on_delete=models.PROTECT)


class SetTransmission(models.Model):
    set = models.ForeignKey(Set, on_delete=models.PROTECT)
    transmission = models.ForeignKey(Transmission, on_delete=models.PROTECT)


class SetColor(models.Model):
    color = models.ForeignKey(Color, on_delete=models.PROTECT)
    car = models.ForeignKey(Car, on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = "Цветовое соотношение"
        verbose_name_plural = "Цветовые соотношения"


class SetTypeCar(models.Model):
    class TYPES(Enum):
        parser = ('parser', 'With the help to parser')
        distributor = ('distributor', 'With the help to distributor')

        @classmethod
        def get_value(cls, member):
            return cls[member].value[0]

    type = models.CharField(max_length=128, choices=[x.value for x in TYPES], null=True, verbose_name="Тип загрузки")
    car = models.ForeignKey(Car, on_delete=models.SET_NULL, null=True, verbose_name="Автомобиль")
    user = models.ForeignKey(User, on_delete=models.PROTECT, null=True, verbose_name="Пользователь")

    class Meta:
        verbose_name = "Тип загрузки автомобиля"
        verbose_name_plural = "Тип загрузки автомобилей"


class File(models.Model):
    file = models.FileField(upload_to="distributor/csv/", storage=CSVFileStorage(), verbose_name="CSV файл")
    user = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name="Пользователь")
    created = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-created"]
        verbose_name = "CSV файл"
        verbose_name_plural = "CSV файлы"


class DistributorEntryFiles(models.Model):
    entry = models.ForeignKey(Entry, on_delete=models.PROTECT, null=True, verbose_name="Заявка")
    act = models.FileField(upload_to="files/distributor", storage=DistributorFileStorage(), blank=True, default=None, verbose_name="Акт")
    agreement = models.FileField(upload_to="files/distributor", storage=DistributorFileStorage(), blank=True, default=None, verbose_name="Соглашение")
    bill = models.FileField(upload_to="files/distributor", storage=DistributorFileStorage(), blank=True, default=None, verbose_name="Счёт")

    def __str__(self):
        return f"#{self.id}"

    class Meta:
        verbose_name = "Файл дистрибьютора"
        verbose_name_plural = "Файлы дистрибьюторов"


class AdminEntryFiles(models.Model):
    entry = models.ForeignKey(Entry, on_delete=models.PROTECT, null=True, verbose_name="Заявка")
    act = models.FileField(upload_to="files/admin", storage=AdminFileStorage(), blank=True, default=None, verbose_name="Акт")
    agreement = models.FileField(upload_to="files/admin", storage=AdminFileStorage(), blank=True, default=None, verbose_name="Соглашение")
    bill = models.FileField(upload_to="files/admin", storage=AdminFileStorage(), blank=True, default=None, verbose_name="Счёт")

    def __str__(self):
        return f"#{self.id}"

    class Meta:
        verbose_name = "Файл админа"
        verbose_name_plural = "Файлы админов"


class Agreements(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, null=True, verbose_name="Дилер")
    distributor = models.ForeignKey(Distributor, on_delete=models.PROTECT, null=True, verbose_name="Дистрибьютор")
    agreement = models.FileField(upload_to="files/agreements", storage=DealerFileStorage(), blank=True, default=None, verbose_name="Соглашение")

    def __str__(self):
        return f"#{self.id}"

    class Meta:
        verbose_name = "Соглашение"
        verbose_name_plural = "Соглашения"
