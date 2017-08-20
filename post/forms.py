from django import forms

from .models import Post 

from draceditor.fields import DraceditorFormField

class CreatePost(forms.ModelForm):
    content = DraceditorFormField()
    status = forms.CharField(widget=forms.HiddenInput())
    tags = forms.CharField(widget=forms.TextInput(), max_length=250, help_text = "Use ',' to seperate tags. For example 'tag1,tag2,tag3'")
    class Meta: 
        model = Post
        fields = ['status', 'title', 'content','tags']