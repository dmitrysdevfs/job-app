from django.views.generic import ListView
from .models import Employer

class EmployerListView(ListView):
    """Список роботодавців з використанням Class-Based Views"""
    model = Employer
    template_name = "employer/list.html"
    context_object_name = "employers"
    paginate_by = 9
    queryset = Employer.objects.all().order_by('name')

# Create your views here.
