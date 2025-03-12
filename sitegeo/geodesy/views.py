from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, get_object_or_404, redirect
from .forms import CallBackForm
from .models import Info, MainServices, Services


def index(request):
    """ представление главной страницы """

    data = {
        'title': 'Главная',
    }
    return render(request, 'geodesy/index.html', context=data)


def services(request):
    """ представление страницы с услугами """

    services = MainServices.published.all()     # выбираются все разрешенные записи из модели

    data = {
        'title': 'Услуги',
        'services': services
    }
    return render(request, 'geodesy/services.html', context=data)


def show_service(request, service_slug):
    """ представление станицы с отображением конкретной услуги """

    service_main = get_object_or_404(MainServices, slug=service_slug)   # берем категорию (запись) в БД по slug
    services = Services.objects.filter(main_id=service_main.pk)         # из всего отбираем то что связанно с категорией

    data = {
        'title': service_main.name,
        'service_main': service_main,
        'services': services
    }
    return render(request, 'geodesy/service.html', context=data)


def useful_info(request):
    """ представление страницы с полезной информацией """

    posts = Info.published.all()    # выбираются все разрешенные посты

    data = {
        'title': 'Полезная информация',
        'posts': posts
    }
    return render(request, 'geodesy/useful_info.html', context=data)


def show_post(request, post_slug):
    """ представление страницы с отображением конкретного поста """

    post = get_object_or_404(Info, slug=post_slug)  # берем пост (запись) в БД по slug

    data = {
        'title': post.title,
        'post': post
    }
    return render(request, 'geodesy/post.html', context=data)


def contact(request):
    """ представление страницы с контактами """

    data = {
        'title': 'Контакты',
    }
    return render(request, 'geodesy/contact.html', context=data)


def call_back(request):
    """ представление страницы с обратным звонком """

    if request.method == 'POST':
        call_form = CallBackForm(request.POST)      # заполняем форму данными из запроса
        if call_form.is_valid():                    # если все корректно, сохраняем запись в БД
            call_form.save()
            return redirect('home')
    else:                                           # если нет, отдаем форму для заполнения
        call_form = CallBackForm()

    data = {
        'title': 'Заказать обратный звонок',
        'call_form': call_form,
    }
    return render(request, 'geodesy/call.html', context=data)


# страница не найдена
def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>404 Ты обосрался<h1>')
