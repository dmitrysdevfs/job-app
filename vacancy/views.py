from django.shortcuts import render, get_object_or_404
from .models import Vacancy

def vacancy_list(request):
    """Список активних вакансій"""
    vacancies = Vacancy.objects.filter(is_active=True)
    return render(request, "vacancy/list.html", {"vacancies": vacancies})

def vacancy_detail(request, pk):
    """Детальна сторінка вакансії"""
    vacancy = get_object_or_404(Vacancy, pk=pk)
    return render(request, "vacancy/detail.html", {"vacancy": vacancy})
