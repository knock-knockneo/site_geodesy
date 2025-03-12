from django import forms
from .models import CallBack
import re


# Форма для обратного звонка
class CallBackForm(forms.ModelForm):
    # comment = forms.CharField(widget=forms.Textarea(attrs={'cols': 50, 'rows': 5}))

    class Meta:
        model = CallBack    # модель с которой будем работать
        fields = ['phone', 'name', 'comment']   # Указываем поля модели для отображения

        # стили для оформления полей формы
        widgets = {
            'phone': forms.TextInput(attrs={'class': 'form-input'}),
            'name': forms.TextInput(attrs={'class': 'form-input'}),
            'comment': forms.Textarea(attrs={'class': 'form-input', 'rows': 5}),
        }

    # проверка телефона
    def clean_phone(self):
        phone = self.cleaned_data['phone']
        # Проверяем, что номер телефона состоит только из цифр и имеет длину 11 символов
        if not re.match(r'^\d{11}$', phone):
            raise forms.ValidationError("Номер телефона должен содержать 11 цифр.")
        return phone
