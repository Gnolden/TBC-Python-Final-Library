from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, authenticate
from .models import User



class LoginForm(forms.Form):
    email = forms.EmailField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)
# class LoginForm(forms.Form):
#     email = forms.EmailField(max_length=150)
#     password = forms.CharField(widget=forms.PasswordInput)
#
#     def clean(self):
#         email = self.cleaned_data.get('email')
#         password = self.cleaned_data.get('password')
#         user = authenticate(email=email, password=password)
#         if not user:
#             raise forms.ValidationError("Invalid login credentials")
#         return self.cleaned_data

# class LoginForm(forms.Form):
#     email = forms.CharField(max_length=150)
#     password = forms.CharField(widget=forms.PasswordInput)
#     # class Meta:
#     #     model = User
#     #     fields = ['email', 'password']


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'full_name', 'personal_number', 'birth_date', 'password1', 'password2']
