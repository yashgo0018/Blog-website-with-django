from django import forms

from .models import Post


class ContactForm(forms.Form):
    Name = forms.CharField(max_length=200)
    Email = forms.EmailField()
    Subject = forms.CharField(max_length=400)
    Message = forms.TextInput()

class PostForm(forms.ModelForm):
    
    class Meta:
        model = Post
        exclude = []

class SortForm(forms.Form):
    sortBy = forms.CharField(label='', widget=forms.Select(choices=[
        ('Sort By Price High To Low', 'Sort By Price High To Low'),
        ('Sort By Price Low To High', 'Sort By Price Low To High')
    ], attrs={
        'class': 'form-control'
    }))

"""
class PriceRange(forms.Form):
    pricerange = forms.ChoiceField(
        label='Price', 
        choices=[
            ('Under $5', 'Under $5'), 
            ('Under $10', 'Under $10'), 
            ('Under $20', 'Under $20'), 
            ('Under $40', 'Under $40')], 
        widget=forms.RadioSelect(attrs={
            'class': 'radio'
        })
    )
"""

class SearchForm(forms.Form):
    search = forms.CharField(label='', widget=forms.TextInput(attrs={
        'class'      : 'form-control mr-sm-2',
        'placeholder': 'I want to search for...',
        'aria-label' : 'Search',
    }))
