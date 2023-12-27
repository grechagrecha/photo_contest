from django import forms
from .models import Post


class AddPostForm(forms.ModelForm):
    title = forms.CharField(
        max_length=64,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        )
    )
    description = forms.CharField(
        max_length=1000,
        widget=forms.Textarea(
            attrs={
                'class': 'form-control'
            }
        )
    )
    image = forms.ImageField(
        widget=forms.FileInput(
            attrs={
                'class': 'btn'
            }
        )
    )

    class Meta:
        model = Post
        exclude = (
            'author',
            'slug',
            'created_at',
            'modified_at'
        )


class FilterForm(forms.Form):
    search_query = forms.CharField(max_length=1000, label='Search for posts')