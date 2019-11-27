from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(label='',max_length=100,widget=forms.TextInput(
        attrs={'id':'username','placeholder':'User'}))
    password = forms.CharField(label='',widget=forms.PasswordInput(
        attrs={'id':'password','placeholder':'Password'}))