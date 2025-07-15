from django.shortcuts import render
from django.views import View

from django.views import View
from django.shortcuts import render, redirect
from .models import Document
from django.contrib import messages

class Upload(View):
    template_name = 'docs/upload.html'
    success_url = 'docs:upload'
    upload_url = 'docs:upload'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        files = request.FILES.getlist('documents')
        title = request.POST.get('title')
        category = request.POST.get('category')
        suffix = request.POST.get('tags', '')  # Using 'tags' field as suffix
        
        if not files:
            print('here')
            messages.error(request, "لطفاً حداقل یک فایل انتخاب کنید")
            return redirect(self.upload_url)
        
        try:
            for file in files:
                Document.objects.create(
                    file=file,
                    title=title,
                    category=category,
                    suffix=suffix
                )
            messages.success(request, "اسناد با موفقیت آپلود شدند")
            return redirect(self.success_url)
        except Exception as e:
            messages.error(request, f"خطا در آپلود: {str(e)}")
            return redirect(self.upload_url)