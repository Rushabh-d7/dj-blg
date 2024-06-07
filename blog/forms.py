# forms.py

from django import forms
from .models import Post, Comment

class BlogForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'media']
        widgets = {
            'content': forms.Textarea(attrs={
                'rows': 4,
                'cols': 75,
                'placeholder': 'Write your post content here...'
            })
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content', 'media','parent']
        widgets = {
            'content': forms.Textarea(attrs={
                'rows': 4,
                'cols': 75,
                'placeholder': 'Write your comment here...'
            }),
            'parent': forms.HiddenInput()
        }