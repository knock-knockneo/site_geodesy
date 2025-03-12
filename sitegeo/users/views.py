from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView
from geodesy.models import Orders, OrderFile, CallBack
from .forms import LoginUserForm, RegisterUserForm, OrderForm, OrderFileForm


class LoginUser(LoginView):
    """ представление авторизации """

    form_class = LoginUserForm
    template_name = 'users/login.html'
    extra_context = {'title': 'Авторизация'}

    # def get_success_url(self):
    #     return reverse_lazy('users:account')


# def login_user(request):
#     if request.method == 'POST':    # проверка на тип запроса
#         form = LoginUserForm(request.POST)
#         if form.is_valid():         # проверка заполнения полей формы
#             cd = form.cleaned_data
#             user = authenticate(request,                # аутентификация user по БД
#                                 username=cd['username'],
#                                 password=cd['password'])
#             if user and user.is_active:
#                 login(request, user)        # авторизация пользователя
#                 return HttpResponseRedirect(reverse('clients'))
#     else:
#         form = LoginUserForm()
#     return render(request, 'users/login.html', {'form': form})


# def logout_user(request):
#     logout(request)
#     return HttpResponseRedirect(reverse('users:login'))


class RegisterUser(CreateView):
    """ представление регистрации """

    form_class = RegisterUserForm
    template_name = 'users/register.html'
    extra_context = {'title': 'Регистрация'}
    success_url = reverse_lazy('users:login')       # перенаправление после регистрации


# def register(request):
#     if request.method == 'POST':
#         form = RegisterUserForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.set_password(form.cleaned_data['password1'])
#             user.save()
#             return render(request, 'users/register_done.html')
#     else:
#         form = RegisterUserForm()
#     return render(request, 'users/register.html', {'form': form})


@staff_member_required
def addorder(request):
    """ добавление нового заказа в лтчном кабинете """

    if request.method == 'POST':
        order_form = OrderForm(request.POST)
        file_form = OrderFileForm(request.POST, request.FILES)
        if order_form.is_valid() and file_form.is_valid():
            order = order_form.save()
            if request.FILES:
                file_order = file_form.save(commit=False)
                file_order.order = order
                file_order.save()
            return redirect('users:account')
    else:
        order_form = OrderForm()
        file_form = OrderFileForm()

    data = {
        'order_form': order_form,
        'file_form': file_form,
        'title': 'Новый заказ'
    }

    return render(request, 'users/addorder.html', context=data)


@staff_member_required
def list_callback(request):
    """ представление списка с обратными звонками """

    callbacks = CallBack.objects.all()

    data = {
        'title': 'Список обратных звонков',
        'callbacks': callbacks
    }
    return render(request, 'users/call_back_list.html', context=data)


@login_required
def account_user(request):
    """ представление личного кабинета """

    client = request.user
    if client.is_staff:
        orders = Orders.objects.all()
    else:
        orders = Orders.forclient.filter(user_id=client.pk)
    data = {
        'title': 'Личный кабинет',
        'user': client,
        'client_orders': orders,

    }
    return render(request, 'users/account.html', context=data)


@login_required
def order_user(request, order_id):
    """ представление конкретного заказа """

    client = request.user
    if client.is_staff:
        order = get_object_or_404(Orders, id=order_id)
    else:
        order = get_object_or_404(Orders, id=order_id, user=client)  # Заказ только для текущего пользователя
    data = {
        'title': 'Страница заказа',
        'order': order,
        'files': order.files.all(),
    }

    return render(request, 'users/order.html', context=data)
