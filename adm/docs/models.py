import os
from uuid import uuid4
from django.db import models
import os
import re
from django.core.files.storage import default_storage

def upload_to(instance, filename):
    """Organizes files into categorized folders with sequential numbering."""
    base, extension = os.path.splitext(filename)
    extension = extension.lower()[1:]  # Remove the dot and make lowercase

    extension_categories = {
        'photos': ['jpeg', 'jpg', 'png', 'gif', 'bmp', 'svg', 'webp', 'tiff', 'ico'],
        'docs': ['pdf', 'doc', 'docx', 'odt', 'rtf', 'tex', 'txt', 'wpd'],
        'sheets': ['xls', 'xlsx', 'ods', 'csv'],
        'slides': ['ppt', 'pptx', 'odp'],
        'videos': ['mp4', 'avi', 'mov', 'wmv', 'flv', 'mkv', 'webm'],
        'audio': ['mp3', 'wav', 'ogg', 'aac', 'flac', 'm4a'],
        'archives': ['zip', 'rar', '7z', 'tar', 'gz', 'bz2'],
        'code': ['py', 'js', 'html', 'css', 'php', 'java', 'cpp', 'json', 'xml'],
        'binaries': ['exe', 'msi', 'dmg', 'pkg', 'deb', 'rpm'],
    }

    folder = 'misc'
    for category, extensions in extension_categories.items():
        if extension in extensions:
            folder = category
            break

    target_dir = os.path.join('files', f'{instance.title}-{instance.suffix}', folder)
    
    # Create directory if it doesn't exist
    if not default_storage.exists(target_dir):
        try:
            # Use os.makedirs for the actual filesystem path
            full_path = os.path.join(default_storage.location, target_dir)
            os.makedirs(full_path, exist_ok=True)
        except Exception as e:
            # Fallback to default behavior if directory creation fails
            pass
    
    existing_numbers = [0] 
    
    try:
        dir_contents = default_storage.listdir(target_dir)[1]  # Get files only
        pattern = re.compile(rf'^{folder}_?(\d*)\.{extension}$')
        
        for existing_file in dir_contents:
            match = pattern.match(existing_file)
            if match:
                number_str = match.group(1)
                number = int(number_str) if number_str else 1
                existing_numbers.append(number)
    except FileNotFoundError:
        pass 
    
    # Determine the next available number
    next_number = max(existing_numbers) + 1
    
    new_filename = f'{folder}_{next_number}.{extension}'
    
    return os.path.join(target_dir, new_filename)


class Document(models.Model):
    class DocumentChoices(models.TextChoices):
        COIN = 's', 'Coin'
        MAGAZINE = 'm', 'Magazine'
        STUDENT = 'st', 'Student'
    is_trash = models.BooleanField(default=False)
    file = models.FileField(upload_to=upload_to)
    title = models.CharField(max_length=120)
    category = models.CharField(
        max_length=2,
        choices=DocumentChoices.choices,
        default=DocumentChoices.COIN,
    )
    suffix = models.CharField(max_length=80)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    def get_icon(self):
        file_types = {
            'image': 'image',
            'pdf': 'file-pdf',
            'doc': 'file-word',
            'video': 'file-video',
            # Add more mappings as needed
        }
        return file_types.get(self.file_type, 'file')
    
    @property
    def file_type(self):
        ext = os.path.splitext(self.file.name)[1].lower()
        if ext in ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp']:
            return 'image'
        elif ext in ['.mp4', '.mov', '.avi', '.mkv', '.webm']:
            return 'video'
        elif ext in ['.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx', '.txt']:
            return 'document'
        else:
            return 'misc'
        
    def get_color(self):
        colors = {
            'image': 'primary',
            'pdf': 'danger',
            'doc': 'info',
            'video': 'warning',
            # Add more mappings as needed
        }
        return colors.get(self.file_type, 'secondary')
    
    class Meta:
        verbose_name = 'Document'
        verbose_name_plural = 'Documents'

    def __str__(self):
        return f"{self.title} ({self.get_category_display()})"
    
    
    