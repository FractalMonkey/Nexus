from django import forms
from captcha.fields import CaptchaField

class ContactForm(forms.Form):
    from_email = forms.CharField(required=True, max_length=25, widget=forms.TextInput( attrs={ 'id':"inputName" ,'class':"form-control", 'placeholder': "Email" }))
    subject = forms.CharField(required=True, max_length=25, widget=forms.TextInput( attrs={ 'id':"inputName" ,'class':"form-control", 'placeholder': "Subject" }))
    message = forms.CharField(required=True, widget=forms.Textarea( attrs={ 'class':"form-control", 'rows':"5", 'id':"comment", 'placeholder':"Message" }))
    captcha = CaptchaField()

class GuestForm(forms.Form):
    name = forms.CharField( max_length=25, widget=forms.TextInput( attrs={ 'id':"inputName" ,'class':"form-control", 'placeholder': "Name" }))
    comment = forms.CharField( widget=forms.Textarea( attrs={ 'class':"form-control", 'rows':"5", 'id':"comment", 'placeholder':"Comment" }))
    captcha = CaptchaField()