# coding: utf-8
from django import forms
from django.contrib.auth.forms import UserCreationForm as CreationForm, UserChangeForm as ChangeForm
from django.utils.translation import ugettext_lazy as _
from users.models import User

class UserCreationForm(CreationForm):
    error_messages = {
        'duplicate_email': u'Пользователь с таким адресом уже существует.',
        'password_mismatch': _("The two password fields didn't match."),
    }

    class Meta:
        model = User
        fields = ('email',)

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            User._default_manager.get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError(
            self.error_messages['duplicate_email'],
            code='duplicate_email',
        )


class UserChangeForm(ChangeForm):
    class Meta:
        model = User
        fields = '__all__'


class SignupForm(forms.Form):
    first_name = forms.CharField(max_length=150, label=u'Имя')
    last_name = forms.CharField(max_length=150, label=u'Фамилия')
    startup_name = forms.CharField(max_length=250, label=u'Название стартапа')

    def signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.startup_name = self.cleaned_data['startup_name']
        user.save()