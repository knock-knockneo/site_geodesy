from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from geodesy.models import Orders, OrderFile, Services, MainServices


# Форма авторизации
class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label="Логин",
                               widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label="Пароль",
                               widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        model = get_user_model()
        fields = ['username', 'password']


# Форма регистрации
class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label="Логин", widget=forms.TextInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label="Пароль", widget=forms.PasswordInput())
    password2 = forms.CharField(label="Повтор пароля", widget=forms.PasswordInput())

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'first_name', 'password1', 'password2']
        labels = {
            'email': 'E-mail',
            'first_name': 'Имя',
        }

        widget = {
            'email': forms.TextInput(attrs={'class': 'form-input'}),
        }

    def clean_email(self):
        email = self.cleaned_data['email']
        if get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError('Такой E-mail уже зарегистрирован!')
        return email


# class RegisterUserForm(forms.ModelForm):
#     username = forms.CharField(label="Логин")
#     password = forms.CharField(label="Пароль", widget=forms.PasswordInput())
#     password2 = forms.CharField(label="Повтор пароля", widget=forms.PasswordInput())
#
#     class Meta:
#         model = get_user_model()
#         fields = ['username', 'email', 'first_name', 'password', 'password2']
#         labels = {
#             'email': 'E-mail',
#             'first_name': 'Имя',
#         }
#
#     def clean_password2(self):
#         cd = self.cleaned_data
#         if cd['password'] != cd['password2']:
#             raise forms.ValidationError('Пароли не совпадают!')
#         return cd['password']
#
#     def clean_email(self):
#         email = self.cleaned_data['email']
#         if get_user_model().objects.filter(email=email).exists():
#             raise forms.ValidationError('Такой E-mail уже зарегистрирован!')
#         return email


# Форма для создания заказа
class OrderForm(forms.ModelForm):
    user = forms.ModelChoiceField(queryset=User.objects.all(),
                                  empty_label='Заказчик не выбран',
                                  label='Заказчик',)     # определяем поле вручную, и значение по умолчанию

    service = forms.ModelChoiceField(queryset=MainServices.objects.all(),
                                  empty_label='Услуга не выбрана',
                                  label='Услуга', )  # определяем поле вручную, и значение по умолчанию

    class Meta:
        model = Orders  # модель, с которой связана форма
        fields = ['user', 'service', 'address', 'comment', ]  # Поля, которые будут отображаться в форме


# Форма для загрузки файлов
class OrderFileForm(forms.ModelForm):

    class Meta:
        model = OrderFile  # модель, с которой связана форма
        fields = ['file']  # Поле для загрузки файла

    label = 'Для загрузки фалов'
