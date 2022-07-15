from tabnanny import verbose
from django.db import models


class BotUser(models.Model):
    user_id = models.BigIntegerField(unique=True, verbose_name="Индент. пользователя")
    first_name = models.CharField(max_length=255, verbose_name="Имя аккаунта")
    phone = models.BigIntegerField(null=True, verbose_name="Телефон")
    city = models.ForeignKey('City', on_delete=models.PROTECT, null=True, verbose_name="Город")
    username = models.CharField(max_length=255, null=True, verbose_name="Имя пользователя")
    name = models.CharField(max_length=255, null=True, verbose_name="Имя пользователя (заполненное)")

    def __str__(self):
        return F"Пользователь #{self.id}"

    class Meta:
        verbose_name = "Пользователь бота"
        verbose_name_plural = "Пользователи бота"


class Mark(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название")
    is_visible = models.BooleanField(verbose_name="Отображается")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Марка"
        verbose_name_plural = "Марки"


class Model(models.Model):
    mark = models.ForeignKey(Mark, on_delete=models.PROTECT, verbose_name="Идент. марки")
    title = models.CharField(max_length=255, verbose_name="Название")
    price = models.BigIntegerField(verbose_name="Цена")
    body = models.CharField(max_length=255, verbose_name="Тело")
    is_visible = models.BooleanField(verbose_name="Отображается")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Модель"
        verbose_name_plural = "Модели"


class Set(models.Model):
    model = models.ForeignKey(Model, on_delete=models.PROTECT, verbose_name="Модель")
    title = models.CharField(max_length=255, verbose_name="Название", unique=False)
    image = models.URLField(verbose_name="Ссылка на картинку")
    special = models.TextField()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Характеристика"
        verbose_name_plural = "Характеристики"


class Engine(models.Model):
    volume = models.FloatField(verbose_name="Значение", null=True)
    power = models.IntegerField(verbose_name="Мощность", null=True)
    type_fuel = models.CharField(max_length=255, verbose_name="Тип топлива", null=True)

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


class Car(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название")
    set_id = models.IntegerField()
    image = models.URLField(verbose_name="Картинка")
    price = models.FloatField(verbose_name="Цена")
    engine_id = models.ForeignKey(Engine, on_delete=models.PROTECT, verbose_name="Двигатель")
    transmission_id = models.ForeignKey(Transmission, on_delete=models.PROTECT, verbose_name="Трансмиссия")
    wd_id = models.ForeignKey(Wd, on_delete=models.PROTECT, verbose_name="Привод")
    expenditure = models.CharField(max_length=255, verbose_name="Расход")
    city_id = models.ForeignKey(City, on_delete=models.PROTECT, verbose_name="Город")
    mark_id = models.ForeignKey(Mark, on_delete=models.PROTECT, verbose_name="Марка")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Автомобиль"
        verbose_name_plural = "Автомобили"


class SetEngine(models.Model):
    set = models.ForeignKey(Set, on_delete=models.PROTECT)
    engine = models.ForeignKey(Engine, on_delete=models.PROTECT)


class SetTransmission(models.Model):
    set = models.ForeignKey(Set, on_delete=models.PROTECT)
    transmission = models.ForeignKey(Transmission, on_delete=models.PROTECT)
