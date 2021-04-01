from django.db.models import fields
from django.forms import ModelForm
from .models import Comment

class CommentForm(ModelForm):
    class Meta:
        # Specify 2 fields for basic model
        # need to know which model we are going to build the form for
        model = Comment
        # which fields are allow, use '__all__' to allow all
        fields = '__all__' # if  ['organization', 'comments']
