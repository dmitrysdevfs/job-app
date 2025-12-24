from django.views.generic import ListView, DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from .models import Employer
from core.utils import get_paginated_page

class EmployerListView(ListView):
    """Список роботодавців з використанням Class-Based Views"""
    model = Employer
    template_name = "employer/list.html"
    context_object_name = "employers"
    paginate_by = 9
    queryset = Employer.objects.select_related(
        "location__community__district__region", 
        "kved"
    ).all().order_by("name")

class EmployerDetailView(DetailView):
    """Детальна сторінка роботодавця зі списком його вакансій"""
    model = Employer
    template_name = "employer/employer_detail.html"
    context_object_name = "employer"

    def get_queryset(self):
        return super().get_queryset().select_related(
            "location__community__district__region", 
            "kved"
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Підтягуємо вакансії цього роботодавця з глибокою оптимізацією локацій
        vacancies_qs = self.object.vacancies.select_related(
            "location__community__district__region"
        ).all().order_by("-published_at")
        
        # Використовуємо універсальну пагінацію для списку вакансій (7 на сторінку)
        page_obj = get_paginated_page(self.request, vacancies_qs, per_page=7)
        
        context["vacancies"] = page_obj.object_list
        context["page_obj"] = page_obj
        context["total_vacs"] = vacancies_qs.count()
        context["list_page"] = self.request.GET.get("list_page")
        return context

class EmployerUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Редагування профілю роботодавця"""
    model = Employer
    fields = [
        'name', 'brand_name', 'tax_id', 'employer_type', 
        'kved', 'location', 'description', 'website', 
        'address', 'logo'
    ]
    template_name = "employer/employer_form.html"
    
    def test_func(self):
        employer = self.get_object()
        return self.request.user == employer.owner or self.request.user in employer.staff.all()

    def get_success_url(self):
        return reverse_lazy('employer:detail', kwargs={'pk': self.object.pk})
