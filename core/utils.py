import uuid
from pathlib import Path
from django.db import models
from django.utils.text import slugify


from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def upload_to(instance: models.Model, filename: str, folder_name: str) -> str:
    """Return the upload path for files with unique UUID and slugified name."""
    path = Path(filename)
    unique_filename = f"{slugify(path.stem)}_{uuid.uuid4().hex[:8]}{path.suffix}"
    return str(Path(folder_name) / unique_filename)


def get_paginated_page(request, queryset, per_page=20):
    """
    Універсальна функція для пагінації.
    Повертає page_obj для вказаного queryset.
    """
    paginator = Paginator(queryset, per_page)
    page_number = request.GET.get('page')
    
    try:
        page_obj = paginator.get_page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.get_page(1)
    except EmptyPage:
        page_obj = paginator.get_page(paginator.num_pages)
        
    return page_obj
