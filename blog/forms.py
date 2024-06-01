# forms.py

from django import forms
from .models import Post, Comment

class BlogForm(forms.ModelForm):

    content = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'rows': 4,  # Number of rows for the textarea
                'cols': 75,  # Number of columns for the textarea
                #'placeholder': 'Write your comment here...'  # Optional placeholder text
            }
        )
    )

    class Meta:
        model = Post
        fields = ['title', 'content']


class CommentForm(forms.ModelForm):

    content = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'rows': 1,  # Number of rows for the textarea
                'cols': 50,  # Number of columns for the textarea
                'placeholder': 'Write your comment here...'  # Optional placeholder text
            }
        )
    )

    class Meta:
        model = Comment
        fields = ['content']