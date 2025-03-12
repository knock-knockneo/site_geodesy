# основное меню всего сайта
menu = [
    {'title': 'Услуги', 'url_name': 'services'},
    {'title': 'Полезная информация', 'url_name': 'info'},
    {'title': 'Контакты', 'url_name': 'contact'},
    {'title': 'Обратный звонок', 'url_name': 'call'},
]


def get_geodesy_context(request):
    """ контескт для передачи основного меню во все шаблоны"""

    return {'mainmenu': menu}
