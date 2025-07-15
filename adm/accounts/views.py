from django.shortcuts import render, redirect
from django.views import View
from accounts.forms import RegisterForm, LoginForm
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import get_user_model, login, logout, authenticate

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
        return render(request, self.template_name)
    

class Logout(View):
    def get(self, request):
        if isinstance(request.user, AnonymousUser):
            return redirect('accounts:login')
        else:
            logout(request)
            return redirect('accounts:login')