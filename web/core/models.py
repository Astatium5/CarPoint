from django.db import models


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
    expenditure = models.CharField(max_length=255, verbose_name="Расход")
    city = models.ForeignKey(
        City, on_delete=models.PROTECT, verbose_name="Город")
    mark = models.ForeignKey(
        Mark, on_delete=models.PROTECT, verbose_name="Марка")

    def __str__(self):
        return self.title

    def to_dict(self):
        return dict(
            id=self.id, title=self.title, price=self.price, image=self.image, mark_id=self.mark_id,
            engine_volume=self.engine.volume, engine_power=self.engine.power, engine_type_fuel=self.engine.type_fuel,
            wd=self.wd.title, expenditure=self.expenditure, transmission=self.transmission.title, special=self.set.special,
            body=self.set.model.body, set_title=self.set.title, model_title=self.set.model.title)

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
        BotUser, on_delete=models.PROTECT, verbose_name="Пользователь")
    username = models.CharField(
        max_length=255, null=True, verbose_name="Имя пользователя")
    car = models.ForeignKey(Car, on_delete=models.PROTECT,
                            verbose_name="Автомобиль")
    email = models.CharField(max_length=255, verbose_name="Почта")
    name = models.CharField(max_length=255, verbose_name="Имя")
    address = models.CharField(max_length=255, verbose_name="Адрес")
    phone = models.BigIntegerField(verbose_name="Телефон")

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = "Заявка"
        verbose_name_plural = "Заявки"


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
    image = models.URLField(verbose_name="Картинка")
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
    car = models.ForeignKey(Car, on_delete=models.PROTECT)
