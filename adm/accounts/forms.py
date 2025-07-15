from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
User = get_user_model()

class RegisterForm(UserCreationForm):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].label = _('رمز عبور')
        
    email = forms.EmailField(
        label='ایمیل',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'example@domain.com'
        })
    )
    
    first_name = forms.CharField(
        label='نام',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'نام شما'
        })
    )
    
    last_name = forms.CharField(
        label='نام خانوادگی',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'نام خانوادگی شما'
        })
    )

    
        
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']
        
        labels = {
            'username': 'نام کاربری',
            'password1': 'رمز عبور',
            'password2': 'تکرار رمز عبور',
        }
        
        help_texts = {
            'username': '',
            'password1': '''
                <ul class="text-muted small mt-2">
                    <li>رمز عبور نباید شبیه اطلاعات شخصی شما باشد</li>
                    <li>رمز عبور باید حداقل ۸ کاراکتر داشته باشد</li>
                    <li>رمز عبور نباید از کلمات متداول باشد</li>
                    <li>رمز عبور نمی‌تواند کاملاً عددی باشد</li>
                </ul>
            ''',
        }
        
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'نام کاربری شما'
            }),
            'password1' : forms.PasswordInput(attrs={
                'class' : 'form-control',
                'placeholder' : 'رمز عبور',
            }),
            'password2' : forms.PasswordInput(attrs={
                'class' : 'form-control',
                'placeholder' : 'تکرار رمز عبور',
            }),

        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})
        self.fields['password1'].widget.attrs.update({'placeholder' : 'رمز عبور'})
        self.fields['password2'].widget.attrs.update({'placeholder' : 'تکرار رمز عبور'})
    

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()
    class Meta:
        fields = ['username', 'password']

        labels = {
            'username' : 'نام کاربری',
            'password' : 'رمز عبور',
        }

        widgets = {
            'username' : forms.TextInput(attrs={'class' : 'form-control'}),
            'password' : forms.PasswordInput(attrs={'class' : 'form-control'}),
        }