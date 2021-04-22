from django.db.models import fields
from django.forms import ModelForm, ValidationError, TextInput
from .models import Comment, InternPerson, Organization
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
        self.fields['username'].widget.attrs['placeholder'] = '你/妳的稱呼(不分大小寫)'
        self.fields['email'].widget.attrs['placeholder'] = '電郵地址（找回密碼用）'
        self.fields['password1'].widget.attrs['placeholder'] = '密碼'
        self.fields['password2'].widget.attrs['placeholder'] = '密碼確認'

    class Meta():
        model = User
        fields = ['username','email','password1','password2']

class UpdateUserForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(UpdateUserForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['placeholder'] = '你/妳的稱呼'
        self.fields['email'].widget.attrs['placeholder'] = '電郵地址（找回密碼用）'
        self.fields['profilePic'].widget.attrs['placeholder'] = '上傳頭像照片'

    class Meta():
        model = InternPerson
        fields = '__all__'
        exclude = ['user']


class CommentForm(ModelForm):
    comments = forms.CharField(widget=forms.Textarea(attrs={'rows': 4, 'cols': 100}))
    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields['organization'].widget.attrs['disabled'] = 'true'
        self.fields['intern'].widget.attrs['disabled'] = 'true'
        self.fields['organization'].label = "評論機構"
        self.fields['intern'].label = "伙伴稱呼"
        #self.fields['internshipType'].label = "實習類型"
        self.fields['hashTags'].label = "可選標籤"
        self.fields['comments'].label = "心得分享"
        #self.fields['score'].label = "評分"

    class Meta:
        # Specify 2 fields for basic model
        # need to know which model we are going to build the form for
        model = Comment
        # which fields are allow, use '__all__' to allow all
        fields = '__all__'