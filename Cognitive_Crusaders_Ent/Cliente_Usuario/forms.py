from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email','first_name','last_name','email','password1', 'password2']

class CustomUserCreationFormExtendedTrabajador(UserCreationForm):
    sueldo = forms.FloatField()
    especialidad = forms.CharField(max_length=150)
    telefono = forms.CharField(max_length=50)

    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ('email', 'first_name', 'last_name', 'sueldo', 'especialidad', 'telefono')
