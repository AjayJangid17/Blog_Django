from django import forms
from django.forms import TextInput
from .models import Post, Comment

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('author','title', 'text','created_date','image')
        widgets = {'title' : TextInput(attrs={'class': 'input', 'placeholder': 'City Name'})}
        
class LoginForm(forms.Form):

    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name','email','body')
