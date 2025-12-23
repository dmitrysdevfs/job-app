from django.shortcuts import render, get_object_or_404
from .models import Vacancy
from core.utils import get_paginated_page

def vacancy_list(request):
    """Список активних вакансій з пагінацією"""
    vacancy_qs = Vacancy.objects.filter(is_active=True)
    page_obj = get_paginated_page(request, vacancy_qs, per_page=8)
    
    return render(request, "vacancy/list.html", {"page_obj": page_obj})

def vacancy_detail(request, pk):
    """Детальна сторінка вакансії з підтримкою повернення на сторінку пагінації"""
    vacancy = get_object_or_404(Vacancy, pk=pk)
    page = request.GET.get('page')
    return render(request, "vacancy/detail.html", {"vacancy": vacancy, "page": page})
