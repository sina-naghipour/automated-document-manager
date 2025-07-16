from django.shortcuts import render, get_object_or_404
from django.views import View
from django.core.paginator import Paginator

from django.views import View
from django.shortcuts import render, redirect
from .models import Document
from django.contrib import messages
from django.db.models import Q
from django.http import Http404, FileResponse
import os
from django.conf import settings


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


class List(View):
    template_name = 'docs/list.html'
    def get(self, request):
        return render(request, self.template_name)



class DocumentListView(View):
    template_name = 'docs/list.html'
    paginate_by = 10

    def get(self, request):
        queryset = Document.objects.filter(is_trash=False)
        
        # Title filter
        if title := request.GET.get('title', '').strip():
            queryset = queryset.filter(title__icontains=title)
        
        # File path search (searches in entire path)
        if file_path := request.GET.get('filename', '').strip():
            queryset = queryset.filter(file__icontains=file_path)
        
        # Category filter
        if category := request.GET.get('category'):
            queryset = queryset.filter(category=category)
        
        # Suffix filter
        if suffix := request.GET.get('suffix', '').strip():
            queryset = queryset.filter(suffix__icontains=suffix)
        
        # File type filtering
        if file_type := request.GET.get('file_type'):
            file_type = file_type.lower()
            if file_type == 'pdf':
                queryset = queryset.filter(file__icontains='.pdf')
            elif file_type == 'doc':
                queryset = queryset.filter(Q(file__icontains='.doc') | Q(file__icontains='.docx'))
            elif file_type == 'xls':
                queryset = queryset.filter(Q(file__icontains='.xls') | Q(file__icontains='.xlsx'))
            elif file_type == 'ppt':
                queryset = queryset.filter(Q(file__icontains='.ppt') | Q(file__icontains='.pptx'))
            elif file_type == 'image':
                queryset = queryset.filter(
                    Q(file__icontains='.jpg') | Q(file__icontains='.jpeg') | 
                    Q(file__icontains='.png') | Q(file__icontains='.gif') |
                    Q(file__icontains='.bmp') | Q(file__icontains='.svg') |
                    Q(file__icontains='.webp')
                )
            elif file_type == 'video':
                queryset = queryset.filter(
                    Q(file__icontains='.mp4') | Q(file__icontains='.avi') |
                    Q(file__icontains='.mov') | Q(file__icontains='.wmv') |
                    Q(file__icontains='.flv') | Q(file__icontains='.mkv')
                )
            elif file_type == 'audio':
                queryset = queryset.filter(
                    Q(file__icontains='.mp3') | Q(file__icontains='.wav') |
                    Q(file__icontains='.ogg') | Q(file__icontains='.aac') |
                    Q(file__icontains='.flac') | Q(file__icontains='.m4a')
                )
            elif file_type == 'archive':
                queryset = queryset.filter(
                    Q(file__icontains='.zip') | Q(file__icontains='.rar') |
                    Q(file__icontains='.7z') | Q(file__icontains='.tar') |
                    Q(file__icontains='.gz') | Q(file__icontains='.bz2')
                )
            elif file_type == 'other':
                queryset = queryset.exclude(
                    Q(file__icontains='.pdf') |
                    Q(file__icontains='.doc') | Q(file__icontains='.docx') |
                    Q(file__icontains='.xls') | Q(file__icontains='.xlsx') |
                    Q(file__icontains='.ppt') | Q(file__icontains='.pptx') |
                    Q(file__icontains='.jpg') | Q(file__icontains='.jpeg') |
                    Q(file__icontains='.png') | Q(file__icontains='.gif') |
                    Q(file__icontains='.bmp') | Q(file__icontains='.svg') |
                    Q(file__icontains='.webp') |
                    Q(file__icontains='.mp4') | Q(file__icontains='.avi') |
                    Q(file__icontains='.mov') | Q(file__icontains='.wmv') |
                    Q(file__icontains='.flv') | Q(file__icontains='.mkv') |
                    Q(file__icontains='.mp3') | Q(file__icontains='.wav') |
                    Q(file__icontains='.ogg') | Q(file__icontains='.aac') |
                    Q(file__icontains='.flac') | Q(file__icontains='.m4a') |
                    Q(file__icontains='.zip') | Q(file__icontains='.rar') |
                    Q(file__icontains='.7z') | Q(file__icontains='.tar') |
                    Q(file__icontains='.gz') | Q(file__icontains='.bz2')
                )

        # Sorting
        sort = request.GET.get('sort', '-date_created')
        queryset = queryset.order_by(sort)

        # Pagination
        paginator = Paginator(queryset, self.paginate_by)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {
            'documents': page_obj,
            'document_categories': Document.DocumentChoices.choices,
            'file_type_choices': [
                ('pdf', 'PDF'),
                ('doc', 'Word'),
                ('xls', 'Excel'),
                ('ppt', 'PowerPoint'),
                ('image', 'تصاویر'),
                ('video', 'ویدئو'),
                ('audio', 'صوت'),
                ('archive', 'فشرده'),
                ('other', 'سایر')
            ],
            'page_obj': page_obj,
        }
        
        return render(request, self.template_name, context)


def download_file(request, path):
    # Construct the absolute file path
    absolute_path = os.path.join(settings.MEDIA_ROOT, path)
    print(absolute_path)
    # Security checks
    if not os.path.exists(absolute_path):
        raise Http404("File does not exist")
    
    if not absolute_path.startswith(settings.MEDIA_ROOT):
        raise Http404("Access denied")
    
    # Open and serve the file
    try:
        file = open(absolute_path, 'rb')
        response = FileResponse(file)
        response['Content-Disposition'] = f'attachment; filename="{os.path.basename(path)}"'
        return response
    except IOError:
        raise Http404("File access error")


def delete_document(request, pk):
    document = get_object_or_404(Document, pk=pk)
    
    if request.method == 'POST':
        document.is_trash = True
        document.save()
        messages.success(request, 'سند با موفقیت حذف شد')
        return redirect('docs:list')
    
    messages.error(request, 'درخواست نامعتبر')
    return redirect('docs:list')



def restore_document(request, pk):
    document = get_object_or_404(Document, pk=pk)
    
    if request.method == 'POST':
        document.is_trash = False
        document.save()
        messages.success(request, 'سند با موفقیت بازیابی شد')
        return redirect('docs:trash')
    
    messages.error(request, 'درخواست نامعتبر')
    return redirect('docs:trash')


def permenant_delete(request, pk):
    document = get_object_or_404(Document, pk=pk)
    
    if request.method == 'POST':
        document.file.delete()
        document.delete()
        messages.success(request, 'سند با موفقیت حذف شد')
        return redirect('docs:trash')
    
    messages.error(request, 'درخواست نامعتبر')
    return redirect('docs:trash')


def empty_trash(request):
    if request.method == 'POST':
        # Get all trashed documents
        trashed_documents = Document.objects.filter(is_trash=True)
        
        count = trashed_documents.count()
        
        if count == 0:
            messages.info(request, "سطل آشغال در حال حاضر خالی است")
            return redirect('docs:trash')
        
        try:
            for document in trashed_documents:
                if document.file:
                    file_path = os.path.join(settings.MEDIA_ROOT, str(document.file))
                    if os.path.exists(file_path):
                        os.remove(file_path)
                document.delete()
            
            messages.success(request, f"تعداد {count} سند برای همیشه حذف شدند")
        except Exception as e:
            messages.error(request, f"خطا در خالی کردن سطل آشغال: {str(e)}")
        
        return redirect('docs:trash')
    
    messages.error(request, "درخواست نامعتبر")
    return redirect('docs:trash')
    

class Trash(View):
    template_name = 'docs/trash.html'
    paginate_by = 10

    def get(self, request):
        # Get only trashed documents
        queryset = Document.objects.filter(is_trash=True)
        
        # Search functionality
        search_query = request.GET.get('search', '').strip()
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(file__icontains=search_query) |
                Q(suffix__icontains=search_query)
            )
        
        # File type filtering
        file_type = request.GET.get('file_type', '').lower()
        if file_type:
            if file_type == 'pdf':
                queryset = queryset.filter(file__icontains='.pdf')
            elif file_type == 'doc':
                queryset = queryset.filter(Q(file__icontains='.doc') | Q(file__icontains='.docx'))
            elif file_type == 'image':
                queryset = queryset.filter(
                    Q(file__icontains='.jpg') | 
                    Q(file__icontains='.jpeg') | 
                    Q(file__icontains='.png') | 
                    Q(file__icontains='.gif')
                )
            # Add other file types as needed

        # Pagination
        paginator = Paginator(queryset, self.paginate_by)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {
            'documents': page_obj,
            'document_categories': Document.DocumentChoices.choices,
            'file_type_choices': [
                ('pdf', 'PDF'),
                ('doc', 'Word'),
                ('image', 'تصاویر'),
                # Add other file types as needed
            ],
            'page_obj': page_obj,
            'search_query': search_query,
            'selected_file_type': file_type,
        }
        
        return render(request, self.template_name, context)



