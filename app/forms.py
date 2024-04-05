from django import forms
from .models import *



class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'body']


class CheckForm(forms.Form):
    type_choises = (
        ('report', 'گزارش'),
        ('suggest', 'پیشنهاد'),
        ('شکایت', 'شکایت')
    )
    name = forms.CharField(max_length=100)
    body = forms.CharField(widget=forms.Textarea)
    type = forms.ChoiceField(choices=type_choises)


class UserCreationForm(forms.ModelForm):
    # password1 = forms.CharField(max_length=25, widget=forms.PasswordInput, label='پسورد')
    password2 = forms.CharField(max_length=25, widget=forms.PasswordInput, label='تکرار پسورد', help_text=
    'لطفا پسورد خود را تکرار نمایید')

    class Meta:
        model = CustomUser2
        fields = ['username', 'first_name', 'age', 'phone', 'email', 'location_name',
                  'password']

    def clean_password(self):
        if self.cleaned_data['password'] != self.cleaned_data['password2']:
            raise Exception('پسورد 1و2 مطابقت ندارد')
        else:
            return self.cleaned_data['password']
