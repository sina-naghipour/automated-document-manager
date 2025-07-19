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




class CustomUserAdminForm(UserCreationForm):
    # Individual permission fields
    create_permission = forms.BooleanField(
        label='ایجاد محتوا',
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    
    edit_permission = forms.BooleanField(
        label='ویرایش محتوا',
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    
    delete_permission = forms.BooleanField(
        label='حذف محتوا',
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    
    manage_permission = forms.BooleanField(
        label='مدیریت کاربران',
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'first_name', 
            'last_name',
            'role',
            'is_active',
            'password1',
            'password2'
        ]
        labels = {
            'username': _('نام کاربری'),
            'email': _('ایمیل'),
            'first_name': _('نام'),
            'last_name': _('نام خانوادگی'),
            'role': _('نقش کاربری'),
            'is_active': _('فعال'),
            'password1': _('رمز عبور'),
            'password2': _('تکرار رمز عبور')
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'role': forms.Select(attrs={'class': 'form-select'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Set initial values for permission checkboxes
        if self.instance and self.instance.pk:
            permissions = self.instance.get_permissions_list()
            self.fields['create_permission'].initial = 'create' in permissions
            self.fields['edit_permission'].initial = 'edit' in permissions
            self.fields['delete_permission'].initial = 'delete' in permissions
            self.fields['manage_permission'].initial = 'manage' in permissions

    def save(self, commit=True):
        user = super().save(commit=False)
        
        # Handle permissions
        permissions = []
        if self.cleaned_data.get('create_permission'):
            permissions.append('create')
        if self.cleaned_data.get('edit_permission'):
            permissions.append('edit')
        if self.cleaned_data.get('delete_permission'):
            permissions.append('delete')
        if self.cleaned_data.get('manage_permission'):
            permissions.append('manage')
            
        user.permissions = ','.join(permissions) if permissions else ''
        
        if commit:
            user.save()
        return user
    
    


class UserPermissionsForm(forms.ModelForm):
    # Individual permission fields
    create_permission = forms.BooleanField(
        label='ایجاد محتوا',
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    
    edit_permission = forms.BooleanField(
        label='ویرایش محتوا',
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    
    delete_permission = forms.BooleanField(
        label='حذف محتوا',
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    
    manage_permission = forms.BooleanField(
        label='مدیریت کاربران',
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    class Meta:
        model = User
        fields = ['role', 'permissions', 'is_active']
        widgets = {
            'role': forms.Select(attrs={'class': 'form-select'}),
            'permissions': forms.HiddenInput(),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }
        labels = {
            'is_active': 'حساب فعال'
        }
        help_texts = {
            'is_active': 'تعیین می‌کند آیا کاربر می‌تواند وارد سیستم شود یا خیر'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance:
            permissions = self.instance.get_permissions_list()
            self.fields['create_permission'].initial = 'create' in permissions
            self.fields['edit_permission'].initial = 'edit' in permissions
            self.fields['delete_permission'].initial = 'delete' in permissions
            self.fields['manage_permission'].initial = 'manage' in permissions
    
    def save(self, commit=True):
        user = super().save(commit=False)
        permissions = []
        
        if self.cleaned_data.get('create_permission'):
            permissions.append('create')
        if self.cleaned_data.get('edit_permission'):
            permissions.append('edit')
        if self.cleaned_data.get('delete_permission'):
            permissions.append('delete')
        if self.cleaned_data.get('manage_permission'):
            permissions.append('manage')
        
        user.permissions = ','.join(permissions) if permissions else ''
        
        if commit:
            user.save()
        return user
    
    
    
    
    