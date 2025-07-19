from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from accounts.forms import RegisterForm, LoginForm, CustomUserAdminForm, UserPermissionsForm
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import get_user_model, login, logout, authenticate
from docs.models import Document
from django.utils import timezone 
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.db import models 
from django.contrib import messages
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


User = get_user_model()


class Register(View):
    
    template_name = 'register.html'
    form_class = RegisterForm
 
    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form' : form})

    def post(self, request):
        user = request.user
        form = self.form_class(request.POST)
        if isinstance(user, AnonymousUser):
            
            if form.is_valid():
                print('is_valid')
                try:
                    if form.cleaned_data['password1'] == form.cleaned_data['password2']:
                        user = User.objects.create_user(
                            username=form.cleaned_data['username'],
                            email=form.cleaned_data['email'],
                            first_name=form.cleaned_data['first_name'],
                            last_name=form.cleaned_data['last_name'],
                            password=form.cleaned_data['password1'],
                            role='viewer',
                            permissions='create'
                        )
                        print('wtf')
                        login(request, user)
                        return redirect('accounts:dashboard')
                    else:
                        print('here')
                        form.add_error('password1', 'کلمه عبور و تکرار آن باید یکسان باشند.')
                        return render(request, self.template_name, {'form' : form}) 
                except Exception as e:
                    print('error', e)
                    form = self.form_class()
                    return render(request, self.template_name, {'form' : form})
            else:
                print('not valid!!!')
                return render(request, self.template_name, {'form' : form})

        return render(request, self.template_name, {'form' : form})


class Login(View):
    
    template_name = 'index.html'
    form_class = LoginForm
    def get(self, request):
        form = self.form_class()
        if not isinstance(request.user, AnonymousUser):
            return redirect('accounts:dashboard')
        return render(request, self.template_name, {'form' : form})

    def post(self, request):
        if isinstance(request.user, AnonymousUser):
            form = self.form_class(request.POST)

            if form.is_valid():
                print('done here')
                print(form.cleaned_data)
                try:
                    user = authenticate(request, username=form.cleaned_data['username'], password=form.cleaned_data['password'])
                    login(request, user)
                    print('done')
                    return redirect('accounts:dashboard')
                except Exception as e:
                    return render(request, self.template_name,  {'form' : form})
            else:
                form.add_error('username','نام کاربری یا رمز عبور اشتباه است.')
                return render(request, self.template_name, {'form' : form})
                
        else:
            return redirect('accounts:dashboard')
                


class Dashboard(View):
    template_name = 'dashboard.html'
    
    def get(self, request):
        # Count files by type
        image_count = Document.objects.filter(
            models.Q(file__iendswith='.jpg') | 
            models.Q(file__iendswith='.jpeg') |
            models.Q(file__iendswith='.png') |
            models.Q(file__iendswith='.gif') |
            models.Q(file__iendswith='.bmp') |
            models.Q(file__iendswith='.webp')
        ).count()

        video_count = Document.objects.filter(
            models.Q(file__iendswith='.mp4') |
            models.Q(file__iendswith='.mov') |
            models.Q(file__iendswith='.avi') |
            models.Q(file__iendswith='.mkv') |
            models.Q(file__iendswith='.webm')
        ).count()

        doc_count = Document.objects.filter(
            models.Q(file__iendswith='.pdf') |
            models.Q(file__iendswith='.doc') |
            models.Q(file__iendswith='.docx') |
            models.Q(file__iendswith='.xls') |
            models.Q(file__iendswith='.xlsx') |
            models.Q(file__iendswith='.ppt') |
            models.Q(file__iendswith='.pptx') |
            models.Q(file__iendswith='.txt')
        ).count()

        # Count everything else as miscellaneous
        all_count = Document.objects.count()
        misc_count = all_count - (image_count + video_count + doc_count)
        recent_documents = Document.objects.all().order_by('-date_created')[:10]

        context = {
            'image_count': image_count,
            'video_count': video_count,
            'doc_count': doc_count,
            'misc_count': misc_count,
            'documents' : recent_documents,
        }
        return render(request, self.template_name, context)



class Logout(View):
    def get(self, request):
        if isinstance(request.user, AnonymousUser):
            return redirect('accounts:login')
        else:
            logout(request)
            return redirect('accounts:login')
    
    
    
class CreateUserView(View):
    template_name = 'accounts/create_user.html'
    form_class = CustomUserAdminForm
    
    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        form = self.form_class(request.POST)
        
        if form.is_valid():
            user = form.save()
            messages.success(request, f'کاربر "{user.username}" با موفقیت ایجاد شد')
            return redirect('accounts:edit_user')
        
        # Handle form errors - this is what's missing
        for field, errors in form.errors.items():
            for error in errors:
                if field == '__all__':
                    messages.error(request, f"{error}")
                else:
                    messages.error(request, f"{form.fields[field].label}: {error}")
        
        return render(request, self.template_name, {
            'form': form,
            'form_errors': form.errors  
        })     
        
        
class EditUserView(View):
    template_name = 'accounts/edit_users.html'
    paginate_by = 10  
    def get(self, request):
        # Get filter parameters
        search_query = request.GET.get('q', '')
        role_filter = request.GET.get('role', '')
        status_filter = request.GET.get('status', '')
        
        # Start with all users
        users = User.objects.all().order_by('-date_joined')
        
        # Apply filters
        if search_query:
            users = users.filter(
                models.Q(username__icontains=search_query) |
                models.Q(email__icontains=search_query) |
                models.Q(first_name__icontains=search_query) |
                models.Q(last_name__icontains=search_query)
            )
        
        if role_filter:
            users = users.filter(role=role_filter)
            
        if status_filter:
            if status_filter == 'active':
                users = users.filter(is_active=True)
            elif status_filter == 'inactive':
                users = users.filter(is_active=False)

        # Pagination
        paginator = Paginator(users, self.paginate_by)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        context = {
            'users': page_obj,
            'user_roles': User.RoleChoices.choices,
            'is_paginated': page_obj.has_other_pages(),
            'page_obj': page_obj,
        }
        
        return render(request, self.template_name, context)


class RoleManagement(View):
    template_name = 'accounts/role_management.html'
    def get(self, request):
        return render(request, self.template_name)


class DetailUserView(View):
    template_name = 'accounts/detail_user.html'
    
    def get(self, request, id):
        user = get_object_or_404(User, id=id)
        password_form = PasswordChangeForm(user=user)
        permissions_form = UserPermissionsForm(instance=user)
        
        context = {
            'user': user,
            'password_form': password_form,
            'permissions_form': permissions_form,
        }
        return render(request, self.template_name, context)
    
    def post(self, request, id):
        user = get_object_or_404(User, id=id)
        
        # Determine which form was submitted
        if 'change_password' in request.POST:
            password_form = PasswordChangeForm(user=user, data=request.POST)
            permissions_form = UserPermissionsForm(instance=user)
            
            if password_form.is_valid():
                password_form.save()
                update_session_auth_hash(request, password_form.user)
                return redirect('accounts:detail_user', id=user.id)
        
        elif 'update_permissions' in request.POST:
            password_form = PasswordChangeForm(user=user)
            permissions_form = UserPermissionsForm(request.POST, instance=user)
            
            if permissions_form.is_valid():
                permissions_form.save()
                return redirect('accounts:detail_user', id=user.id)
        
        context = {
            'user': user,
            'password_form': password_form,
            'permissions_form': permissions_form,
        }
        return render(request, self.template_name, context)
    

class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/profile.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        

        context['now'] = timezone.now()
        return context 
    
    
class DeleteUserView(View):
    def post(self, request, id):
        user = get_object_or_404(User, id=id)
        username = user.username
        user.delete()
        return redirect('accounts:edit_user')
    
    
    
