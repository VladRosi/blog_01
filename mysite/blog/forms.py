from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):
  class Meta:
    model = Comment
    fields = ['name', 'email', 'body']


class EmailPostForm(forms.Form):
  name = forms.CharField(max_length=32)
  email = forms.EmailField()
  to = forms.EmailField()
  comment = forms.CharField(required=False, widget=forms.Textarea)


class SearchForm(forms.Form):
  query = forms.CharField()