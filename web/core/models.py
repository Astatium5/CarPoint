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
    special = models.TextField(verbose_name="Конфигурации")

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
        return F"{self.volume} - {self.power} - {self.type_fuel}"

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
    set = models.ForeignKey(Set, on_delete=models.PROTECT)
    image = models.URLField(verbose_name="Картинка")
    price = models.FloatField(verbose_name="Цена")
    engine = models.ForeignKey(Engine, on_delete=models.PROTECT, verbose_name="Двигатель")
    transmission = models.ForeignKey(Transmission, on_delete=models.PROTECT, verbose_name="Трансмиссия")
    wd = models.ForeignKey(Wd, on_delete=models.PROTECT, verbose_name="Привод")
    expenditure = models.CharField(max_length=255, verbose_name="Расход")
    city = models.ForeignKey(City, on_delete=models.PROTECT, verbose_name="Город")
    mark = models.ForeignKey(Mark, on_delete=models.PROTECT, verbose_name="Марка")

    def __str__(self):
        return self.title

    def to_dict(self):
        return dict(
            id=self.id, title=self.title, price=self.price, image=self.image,
            engine_volume=self.engine.volume, engine_power=self.engine.power, engine_type_fuel=self.engine.type_fuel,
            wd=self.wd.title, expenditure=self.expenditure)

    class Meta:
        verbose_name = "Автомобиль"
        verbose_name_plural = "Автомобили"


class Color(models.Model):
    title = models.CharField(max_length=128)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Цвет"
        verbose_name_plural = "Цвета"


class SetEngine(models.Model):
    set = models.ForeignKey(Set, on_delete=models.PROTECT)
    engine = models.ForeignKey(Engine, on_delete=models.PROTECT)


class SetTransmission(models.Model):
    set = models.ForeignKey(Set, on_delete=models.PROTECT)
    transmission = models.ForeignKey(Transmission, on_delete=models.PROTECT)


class SetColor(models.Model):
    color = models.ForeignKey(Color, on_delete=models.PROTECT)
    car = models.ForeignKey(Car, on_delete=models.PROTECT)
