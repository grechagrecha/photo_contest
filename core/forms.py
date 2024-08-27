from django import forms
from .models import Post, Comment


class PostAddForm(forms.ModelForm):
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
        fields = [
            'title',
            'image',
            'description'
        ]


class PostUpdateForm(forms.ModelForm):
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
        fields = [
            'title',
            'image',
            'description'
        ]


class CommentUpdateForm(forms.ModelForm):
    text = forms.CharField(
        max_length=1000,
        widget=forms.Textarea(
            attrs={
                'class': 'form-control'
            }
        )
    )

    class Meta:
        model = Comment
        fields = [
            'text'
        ]


class AddCommentForm(forms.ModelForm):
    text = forms.CharField(
        max_length=300,
        widget=forms.Textarea(
            attrs={
                'class': 'form-control'
            }
        )
    )

    class Meta:
        model = Comment
        exclude = [
            'user',
            'post'
        ]


class FilterForm(forms.Form):
    search_query = forms.CharField(max_length=1000, label='Search for posts')
