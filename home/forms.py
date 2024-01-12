from django import forms
from django.db import transaction
from home.models import Student, Code
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.forms import TextInput, EmailInput, PasswordInput
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
User = get_user_model()

class StudentSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username','full_name','email','group')
        widgets = {
            'username': TextInput(attrs={'placeholder': 'Ravshan', 'class': 'common__login__input'}),
            'full_name': TextInput(attrs={'placeholder': 'Ravshan Ermatov', 'class': 'common__login__input'}),
            'email': EmailInput(attrs={'placeholder': 'example@gmail.com', 'class': 'common__login__input'}),
            'group': TextInput(attrs={'placeholder': 'A-1', 'class': 'common__login__input'}),
            'password1': PasswordInput(attrs={'placeholder': '*****', 'class': 'common__login__input'}),
            'password2': PasswordInput(attrs={'placeholder': '*****', 'class': 'common__login__input'}),
        }

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_student = True
        user.save()
        student = Student.objects.create(user=user)
        student.save()
        return user

    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(email=email).exists():
            raise ValidationError("An user with this email already exists!")
        return email

class CodeForm(forms.ModelForm):
    number = forms.CharField(label='Code', help_text='Enter SMS Verification code')
    class Meta:
        model = Code
        fields = ( 'number',)
class UserUpdateForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username','full_name','email','group')

    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(email=email).exists():
            raise ValidationError("An user with this email already exists!")
        return email

