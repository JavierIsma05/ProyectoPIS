from django import forms
from django.contrib.auth.models import User,Group
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from accounts.models import Profile
from .models import *
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit

#LOGIN
class LoginForm(AuthenticationForm):
    pass

class RegisterForm(UserCreationForm):
    email = forms.EmailField(label='Correo electrónico')
    first_name = forms.CharField(label='Nombre')
    last_name = forms.CharField(label='Apellido')
    password1 = forms.CharField(label='Contraseña',widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirma Contraseña',widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username','email','first_name','last_name','password1','password2']
        help_texts = {k:"" for k in fields}
    
    def clean_email(self):
        email_field = self.cleaned_data['email']

        if User.objects.filter(email=email_field).exists():
            raise forms.ValidationError('Este correo ya está registrado')
        return email_field

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name','last_name']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image','address','location','telephone']



class TutoriaForm(forms.ModelForm):
    teacher = forms.ModelChoiceField(queryset=User.objects.filter(groups__name='profesores'),label = 'Profesor')

    #status = forms.ChoiceField(choices=Tutoria.STATUS_CHOICES,initial='I',label='Estado')
    description = forms.CharField(widget=forms.Textarea(attrs={'rows':3}),label='Descripción')
    
    class Meta:
        model = Tutoria
        fields = ['date','description','teacher','status','time_quantity','modalidad','firma']
   
    #helper = FormHelper()
    #helper.layout = Layout(
    #    Field('date'),
    #    Field('description'),
    #    Field('teacher'),
    #    Submit('submit','Submit')
    #)

