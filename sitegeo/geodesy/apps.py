from django.apps import AppConfig


class GeodesyConfig(AppConfig):
    verbose_name = "Основная информация"        # отображения заголовка в админке
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'geodesy'
