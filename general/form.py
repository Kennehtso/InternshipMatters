from django.db.models import fields
from django.forms import ModelForm, ValidationError, TextInput
from .models import Comment
from django import forms

class CommentForm(ModelForm):
    #internshipType = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    #comments = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    #score = forms.IntegerField(widget=forms.TextInput(attrs={'class':'form-control'}))
    class Meta:
        # Specify 2 fields for basic model
        # need to know which model we are going to build the form for
        model = Comment
        # which fields are allow, use '__all__' to allow all
        exclude = ['intern','createDate']
