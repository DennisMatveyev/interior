# coding: utf-8
from django import forms
from .models import Subscriber, Sort
from django.db.utils import OperationalError

choices=[]
try:
    #code requiring database access here
    choices = [ (c, c) for c in Sort.objects.all()]
    choices.append(('', ''))
except OperationalError:
    #close the database connection
    # connection.close()
    print 'hello, world!'

class SelectForm(forms.Form):
    name = forms.CharField(widget=forms.Select(choices=choices), label="Выбор по типу объекта:")

class ContactForm(forms.Form):
    name = forms.CharField(max_length=20, label="Ваше имя")
    email = forms.EmailField(label="Ваш Email")
    subject = forms.CharField(max_length=100, label="Тема сообщения")
    message = forms.CharField(widget=forms.Textarea, label="Текст сообщения")


class SubscriberForm(forms.ModelForm):
    class Meta:
        model = Subscriber
        fields = ['email']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control',
                                       'id': 'mc-email',
                                       'placeholder': 'Ваш Email...'}
                                     )
        }

