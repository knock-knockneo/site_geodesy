from django.contrib import admin, messages
from django.utils.safestring import mark_safe
from .models import Info, MainServices, Services, Orders, OrderFile, CallBack


@admin.register(MainServices)
class MainServicesAdmin(admin.ModelAdmin):
    """ настройка отображения таблицы с категориями услуг """

    prepopulated_fields = {'slug': ('name',)}  # auto определение слага, поле должено быть редактируемым
    list_display = ('id', 'name', 'time_update', 'is_published')       # список отображаемых полей в админке
    list_display_links = ('id', 'name')     # кликабельные поля
    ordering = ['-time_update', 'name']     # сортировка отображения постов в админке
    list_editable = ('is_published',)       # редакрируемые поля в админке
    actions = ['set_published', 'set_draft']  # действия над выбраными записями

    @admin.action(description="Опубликовать выбранные записи")
    def set_published(self, request, queryset):
        """ Действие: опубликовать выбраные записи """

        count = queryset.update(is_published=1)
        self.message_user(request, f"Измененно {count} записи")

    @admin.action(description="Снять с публикации выбранные записи")
    def set_draft(self, request, queryset):
        """ Действие: Снять с публикации выбранные записи """

        count = queryset.update(is_published=0)
        self.message_user(request, f"{count} записи снято с публикации!", messages.WARNING)


@admin.register(Services)
class ServicesAdmin(admin.ModelAdmin):
    """ настройка отображения таблицы со всеми услугами """

    list_display = ('id', 'name', 'price', 'main')       # список отображаемых полей в админке
    list_display_links = ('id', 'name')     # кликабельные поля
    ordering = ['main_id', 'id']    # сортировка отображения постов в админке
    list_filter = ['main__name']    # филтр по выбраным полям


@admin.register(Info)
class InfoAdmin(admin.ModelAdmin):
    """настройка отображения таблицы с постами в админке"""

    # форма редактирования
    fields = ['title', 'slug', 'images', 'post_image', 'content', 'is_published']    # отображаемые поля в форме
    #exclude = []    # не отображаемые поля
    readonly_fields = ['post_image']    # поля для чтения
    # /форма редактирования

    prepopulated_fields = {'slug': ('title', )}     # auto определение слага, поле должено быть редактируемым
    list_display = ('id', 'title', 'post_image', 'time_update', 'is_published')       # список отображаемых полей в админке
    list_display_links = ('id', 'title')        # кликабельные поля
    ordering = ['-time_update', 'title']        # сортировка отображения постов в админке
    list_editable = ('is_published',)      # редакрируемые поля в админке
    list_per_page = 10       # пагинация списка постов
    actions = ['set_published', 'set_draft']     # действия над выбраными записями
    search_fields = ['title', 'content']

    @admin.display(description='Изображение')
    def post_image(self, post: Info):
        """ Вспомогательное поле с изображением"""
        if post.images:
            return mark_safe(f"<img src='{post.images.url}' width=100>")
        return f"Нет изображения"

    @admin.action(description="Опубликовать выбранные записи")
    def set_published(self, request, queryset):
        """ Действие: опубликовать выбраные записи """

        count = queryset.update(is_published=1)
        self.message_user(request, f"Измененно {count} записи")

    @admin.action(description="Снять с публикации выбранные записи")
    def set_draft(self, request, queryset):
        """ Действие: Снять с публикации выбранные записи """

        count = queryset.update(is_published=0)
        self.message_user(request, f"{count} записи снято с публикации!", messages.WARNING)


# @admin.register(OrderFile)
class OrderFileInline(admin.StackedInline):
    """ Таблица файлов """

    extra = 1
    model = OrderFile
    list_display = ('id', 'order', 'file')  # список отображаемых полей в админке
    # list_display_links = ('id', 'order')  # кликабельные поля
    # list_filter = ['order']  # филтр по выбраным полям


@admin.register(Orders)
class OrdersAdmin(admin.ModelAdmin):
    """ Таблица заказов """

    inlines = (OrderFileInline,)
    list_display = ('id', 'user', 'service', 'address', 'time_update', 'comment', 'status', 'display_client')
    list_display_links = ('id', 'service')  # кликабельные поля
    list_filter = ['user__username', 'service__name']  # филтр по выбраным полям


@admin.register(CallBack)
class CallBackAdmin(admin.ModelAdmin):
    """ Таблица с обратными звонками """

    list_display = ('id', 'phone', 'name', 'comment', 'time_create', 'status')  # список отображаемых полей в админке
    list_display_links = ('id', 'name')  # кликабельные поля


# регистрация таблицы Info в админке
# admin.site.register(Info, InfoAdmin)
