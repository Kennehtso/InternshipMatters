from django.db.models import fields
from django.forms import ModelForm, ValidationError, TextInput
from .models import Comment
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class LoginUserForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(LoginUserForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = '你/妳的稱呼'
        self.fields['password1'].widget.attrs['placeholder'] = '密碼'

    class Meta():
        model = User
        fields = '__all__'

class CreateUserForm(UserCreationForm):
    email = forms.EmailField(required=True)
    def __init__(self, *args, **kwargs):
        super(CreateUserForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = '你/妳的稱呼'
        self.fields['email'].widget.attrs['placeholder'] = '電郵地址（找回密碼用）'
        self.fields['password1'].widget.attrs['placeholder'] = '密碼'
        self.fields['password2'].widget.attrs['placeholder'] = '密碼確認'

    class Meta():
        model = User
        fields = ['username','email','password1','password2']

class CommentForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields['organization'].widget.attrs['disabled'] = 'true'
        self.fields['intern'].widget.attrs['disabled'] = 'true'
        self.fields['organization'].label = "機構"
        self.fields['internshipType'].label = "實習類型"
        self.fields['hashTags'].label = "標籤 (按'Ctrl'可以多選)"
        self.fields['comments'].label = "心得分享"
        #self.fields['score'].label = "評分"

    class Meta:
        # Specify 2 fields for basic model
        # need to know which model we are going to build the form for
        model = Comment
        # which fields are allow, use '__all__' to allow all
        fields = '__all__'