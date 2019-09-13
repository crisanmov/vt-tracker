import os
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.forms.widgets import PasswordInput, TextInput
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.utils import timezone
from accounts.models import User

class CustomAuthForm(AuthenticationForm):
	username = forms.CharField(widget=TextInput(attrs={'class':'validate form-control col-sm-4 mx-auto',
	 'placeholder': 'Introduce tu Correo'}))
	password = forms.CharField(widget=PasswordInput(attrs={'class':'validate form-control col-sm-4 mx-auto',
	 'placeholder':'Introduce tu Contraseña'}))

class RegistrationForm(UserCreationForm):
	password1 = forms.CharField(widget=PasswordInput(attrs={'class': 'validate form-control form-accounts'}))
	password2 = forms.CharField(widget=PasswordInput(attrs={'class': 'validate form-control form-accounts'}))

	class Meta:
		model = User
		fields = (
			'username',
			'name',
			'lastP',
			'lastM',
			'address',
			'email',
			'phone',
			'date_born',
			'password1',
			)

		labels = {
			'username': 'Nombre de Usuario',
            'name': 'Nombre',
            'lastP': 'Apellido Paterno',
            'lastM': 'Apellido Materno',
            'address': 'Dirección',
			'date_born': 'Fecha de Nacimiento',
            'phone': 'Telefono',
            'email': 'Email',
			'password1': 'Contraseña',

			#'is_superuser': 'Administrador',
        }

		widgets={

			'username': forms.TextInput(attrs={'class': 'validate form-control form-accounts'}),
			'name': forms.TextInput(attrs={'class': 'validate form-control form-accounts'}),
			'lastP': forms.TextInput(attrs={'class': 'validate form-control form-accounts'}),
			'lastM': forms.TextInput(attrs={'class': 'validate form-control form-accounts'}),
			'email': forms.EmailInput(attrs={'class': 'validate form-control form-accounts'}),
			'phone': forms.TextInput(attrs={'class': 'validate form-control form-accounts'}),
			'date_born': forms.TextInput(attrs={'class': 'validate form-control form-accounts'}),
			'address': forms.TextInput(attrs={'class': 'validate form-control form-accounts'})
		}

	def save(self, commit=True):
		user = super(RegistrationForm, self).save(commit=False)

		user.username = self.cleaned_data['username']
		user.name = self.cleaned_data['name']
		user.lastP = self.cleaned_data['lastP']
		user.lastM = self.cleaned_data['lastM']
		user.address = self.cleaned_data['address']
		user.email = self.cleaned_data['email']
		user.phone = self.cleaned_data['phone']
		#user.is_superuser = self.cleaned_data['is_superuser']
		user.is_active = True
		user.date_joined = timezone.now()
		user.date_born = self.cleaned_data['date_born']

		if commit:
			user.save()

		return user
