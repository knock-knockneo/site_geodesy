from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class PublishedManager(models.Manager):
    """ Manager возвращает только опубликованные записи """
    def get_queryset(self):
        return super().get_queryset().filter(is_published=1)


class ClientManager(models.Manager):
    """ Manager возвращает записи которые доступны для отображения клиентам"""
    def get_queryset(self):
        return super().get_queryset().filter(display_client=1)


class Info(models.Model):
    """ Таблица с постами """

    title = models.CharField(max_length=255, verbose_name='Заголовок')
    slug = models.SlugField(max_length=255, unique=True, db_index=True)
    images = models.ImageField(upload_to='images/', default=None, blank=True, null=True, verbose_name='Изображение')
    content = models.TextField(blank=True)
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Время изменения')
    is_published = models.BooleanField(default=True, verbose_name='Статус')

    objects = models.Manager()            # стандартный manager записей
    published = PublishedManager()      # только опубликованные записи manager

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Публикации"         # отображение в админке
        verbose_name_plural = "Публикации"

    def get_absolute_url(self):
        """Форимрование ссылки для отображения постов, по уникальному слагу из таблицы"""
        return reverse('post', kwargs={'post_slug': self.slug})


class MainServices(models.Model):
    """ Таблица с категориями услуг """

    name = models.CharField(max_length=255, db_index=True, verbose_name='Категория')
    slug = models.SlugField(max_length=255, unique=True, db_index=True)
    content = models.TextField(blank=True)
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Время изменения')
    is_published = models.BooleanField(default=True, verbose_name='Статус')

    objects = models.Manager()  # стандартный manager записей
    published = PublishedManager()  # только опубликованные записи manager

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория услуги"         # отображение в админке
        verbose_name_plural = "Категории услуг"

    def get_absolute_url(self):
        """Форимрование ссылки для отображения категорий, по уникальному слагу из таблицы"""
        return reverse('service', kwargs={'service_slug': self.slug})


class Services(models.Model):
    """ Все существующие услуги """

    main = models.ForeignKey(MainServices, on_delete=models.PROTECT, verbose_name='Категория услуги')
    name = models.CharField(max_length=255, db_index=True, verbose_name='Наименование')
    price = models.CharField(max_length=100, verbose_name='Стоимость')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Услуга"         # отображение в админке
        verbose_name_plural = "Услуги"


class Orders(models.Model):
    """ Таблица с заказами """

    user = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name='Клиент')
    service = models.ForeignKey(MainServices, on_delete=models.PROTECT, verbose_name='Услуга')
    address = models.CharField(max_length=255, verbose_name='Адрес')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Время изменения')
    comment = models.TextField(blank=True, verbose_name='Комментарий к заказу')
    status = models.BooleanField(default=False, verbose_name='Статус')
    display_client = models.BooleanField(default=False, verbose_name='Отображение у клиента')

    def __str__(self):
        return f"Заказ для {self.user} по адресу: {self.address}"

    class Meta:
        verbose_name = "Заказ"         # отображение в админке
        verbose_name_plural = "Заказы"
        ordering = ['-time_create']

        # def get_absolute_url(self):
    #     """Форимрование ссылки для отображения заказа"""
    #     return reverse('order', kwargs={'order_id': self.pk})

    objects = models.Manager()  # стандартный manager записей
    forclient = ClientManager()  # только разрешенные для отображения записи manager


class OrderFile(models.Model):
    """ Таблица с файлами привязаных к заказам """

    order = models.ForeignKey(Orders, on_delete=models.CASCADE, verbose_name='Заказ', related_name='files')
    file = models.FileField(upload_to='users/files/', default=None, blank=True, null=True, verbose_name='Файл')

    def __str__(self):
        return f'{self.file}'

    def get_filename(self):
        return self.file.name.split('/')[-1]


class CallBack(models.Model):
    """ Таблица с обратными звонками """

    phone = models.CharField(max_length=20, verbose_name='Номер телефона')
    name = models.CharField(max_length=50, verbose_name='Имя')
    comment = models.TextField(blank=True, verbose_name='Комментарий')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время заявки')
    status = models.BooleanField(default=False, verbose_name='Отработан ли звонок?')

    def __str__(self):
        return f'{self.phone} {self.name}'

    class Meta:
        verbose_name = "Обратный звонок"  # отображение в админке
        verbose_name_plural = "Обратные звонки"
        ordering = ['status', '-time_create']
