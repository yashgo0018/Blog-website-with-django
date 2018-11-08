from django import forms

class ContactForm(forms.Form):
    Name = forms.CharField(max_length=200, label='', widget=forms.TextInput(attrs={
        'class'      : 'form-control mr-sm-2 mt-2',
        'placeholder': 'Name',
        'aria-label' : 'Search',
    }))
    Email = forms.EmailField(label='', widget=forms.EmailInput(attrs={
        'class'      : 'form-control mr-sm-2 mt-2',
        'placeholder': 'Email',
        'aria-label' : 'Search',
    }))
    Subject = forms.CharField(max_length=400, label='', widget=forms.TextInput(attrs={
        'class'      : 'form-control mr-sm-2 mt-2',
        'placeholder': 'Subject',
        'aria-label' : 'Search',
    }))
    Message = forms.CharField(label='', widget=forms.Textarea(attrs={
        'class'      : 'form-control mr-sm-2  mt-2',
        'placeholder': 'Message',
        'aria-label' : 'Search',
    }))