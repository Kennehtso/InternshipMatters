from django.db.models import fields
from django.forms import ModelForm, ValidationError, TextInput
from .models import Comment
from django import forms

class CommentForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields['organization'].widget.attrs['disabled'] = 'true'
        self.fields['intern'].widget.attrs['disabled'] = 'true'
        self.fields['organization'].label = "機構"
        self.fields['internshipType'].label = "實習類型"
        self.fields['hashTags'].label = "標籤 (按'Ctrl'可以多選)"
        self.fields['comments'].label = "心得分享"
        self.fields['score'].label = "評分"

    class Meta:
        # Specify 2 fields for basic model
        # need to know which model we are going to build the form for
        model = Comment
        # which fields are allow, use '__all__' to allow all
        fields = '__all__'