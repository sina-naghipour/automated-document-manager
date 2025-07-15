import os
from uuid import uuid4
from django.db import models
import os
import re
from django.core.files.storage import default_storage

def upload_to(instance, filename):
    """Dynamically organizes files into folders with sequential numbering continuing from existing files."""
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

    # Get the target directory path
    target_dir = f'{instance.title}-{instance.suffix}/{folder}/'
    
    # Find all existing files in the directory and extract their numbers
    existing_numbers = []
    try:
        dir_contents = default_storage.listdir(target_dir)[1]  # Get files only
        pattern = re.compile(rf'^{base}(_(\d+))?\.{extension}$')
        
        for existing_file in dir_contents:
            match = pattern.match(existing_file)
            if match:
                number = match.group(2)
                existing_numbers.append(int(number) if number else 0)
    except FileNotFoundError:
        pass  # Directory doesn't exist yet
    
    # Determine the next available number
    next_number = max(existing_numbers) + 1 if existing_numbers else 1
    
    # Generate the new filename
    print(next_number)
    if next_number == 1:
        new_filename = f'{folder}.{extension}'
    else:
        new_filename = f'{folder}_{next_number}.{extension}'
    
    return f'files/{target_dir}{new_filename}'



class Document(models.Model):
    class DocumentChoices(models.TextChoices):
        COIN = 's', 'Coin'
        MAGAZINE = 'm', 'Magazine'
        STUDENT = 'st', 'Student'

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

    class Meta:
        verbose_name = 'Document'
        verbose_name_plural = 'Documents'

    def __str__(self):
        return f"{self.title} ({self.get_category_display()})"