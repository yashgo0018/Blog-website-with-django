from django import forms
from django.contrib.auth.models import User
from blog.models import Post
from ckeditor_uploader.fields import RichTextUploadingField
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from pages.models import Page
from django.contrib.auth.forms import UserChangeForm, ReadOnlyPasswordHashField

class LoginForm(forms.Form):
    UserName = forms.CharField(label = 'Username', widget = forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Username',
            'style': 'margin: 3px 0 10px 0'
        }
    ))

    PassWord = forms.CharField(label = 'Password', widget = forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Password',
            'style': 'margin: 3px 0 10px 0'
        }
    ))

class SubscriberLoginForm(forms.Form):
    UserName = forms.CharField(label = '', widget = forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Username',
            'style': 'margin: 3px 0 10px 0'
        }
    ))

    PassWord = forms.CharField(label = '', widget = forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Password',
            'style': 'margin: 3px 0 10px 0'
        }
    ))

common_text_field = forms.TextInput(attrs={
    'class': 'form-control',
})

common_password_field = forms.PasswordInput(attrs={
    'class': 'form-control',
})

common_email_field = forms.EmailInput(attrs={
    'class': 'form-control',
})

class UserForm(forms.ModelForm):
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password']
        widgets = {
            'first_name': common_text_field,
            'last_name' : common_text_field,
            'email'     : common_email_field,
            'username'  : common_text_field,
            'password'  : common_password_field,
        }

class RegisterForm(forms.Form):
    FirstName = forms.CharField(label = '', widget = forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'First Name',
            'style': 'margin: 3px 0 5px 0'
        }
    ))

    LastName = forms.CharField(label = '', widget = forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Last Name',
            'style': 'margin: 3px 0 5px 0'
        }
    ))

    Email = forms.EmailField(label = '', widget = forms.EmailInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Email',
            'style': 'margin: 3px 0 5px 0'
        }
    ))

    UserName = forms.CharField(label = '', widget = forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Username',
            'style': 'margin: 3px 0 5px 0'
        }
    ))

    PassWord = forms.CharField(label = '', widget = forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Password',
            'style': 'margin: 3px 0 5px 0'
        }
    ))

    PassWord2 = forms.CharField(label = '', widget = forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Confirm Password',
            'style': 'margin: 3px 0 10px 0'
        }
    ))

    def clean(self):
        data = self.cleaned_data
        password = data.get("PassWord")
        password2 = data.get("PassWord2")
        if password != password2:
            raise forms.ValidationError("Password doesn't match")
        else:
            return data

    def clean_UserName(self):
        username = self.cleaned_data.get("UserName")
        qs = User.objects.filter(username=username)
        if qs.exists():
            raise forms.ValidationError("Username Already Taken")
        return username

    def clean_Email(self):
        email = self.cleaned_data.get("Email")
        qs = User.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError("Email Already Taken")
        return email

class UserUpdateForm(UserChangeForm):
    password = ReadOnlyPasswordHashField(
        label="Password",
        help_text=(
            "user's password can be change by "
            "<a href=\"/accounts/password/\">this form</a>."
        ),
    )
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'password', 'email']
        widgets = {
            'first_name': common_text_field,
            'last_name' : common_text_field,
            'email'     : common_email_field,
            'password'  : common_password_field,
        }

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'thumbnail', 'description', 'publish']
        widgets = {
            'title': forms.TextInput(attrs={
                'class'         : 'form-control',
                'placeholder'   : 'Post Title'
            }),
            'description': CKEditorUploadingWidget()
        }

class PageForm(forms.ModelForm):
    class Meta:
        model = Page
        fields = ['title', 'Content', 'publish']
        widgets = {
            'title': forms.TextInput(attrs={
                'class'         : 'form-control',
                'placeholder'   : 'Page Title'
            }),
            'Content': CKEditorUploadingWidget()
        }