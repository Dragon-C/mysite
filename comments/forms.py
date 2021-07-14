from django import forms
from .models import Comment
from mdeditor.fields import MDTextFormField

# class CommentForm(forms.Form):
#     name = forms.CharField()
#     email = forms.CharField()
#     url = forms.CharField()
#     text = MDTextFormField()

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name','email','url','text']