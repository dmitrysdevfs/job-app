from django.views.generic import ListView, DetailView
from .models import Employer
from core.utils import get_paginated_page

class EmployerListView(ListView):
    """Список роботодавців з використанням Class-Based Views"""
    model = Employer
    template_name = "employer/list.html"
    context_object_name = "employers"
    paginate_by = 9
    queryset = Employer.objects.all().order_by('name')

class EmployerDetailView(DetailView):
    """Детальна сторінка роботодавця зі списком його вакансій"""
    model = Employer
    template_name = "employer/employer_detail.html"
    context_object_name = "employer"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Підтягуємо вакансії цього роботодавця
        vacancies_qs = self.object.vacancies.all().order_by('-published_at')
        
        # Використовуємо універсальну пагінацію для списку вакансій (7 на сторінку)
        page_obj = get_paginated_page(self.request, vacancies_qs, per_page=7)
        
        context['vacancies'] = page_obj.object_list
        context['page_obj'] = page_obj
        context['total_vacs'] = vacancies_qs.count()
        context['list_page'] = self.request.GET.get('list_page')
        return context
