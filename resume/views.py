from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from .models import Resume

class ResumeListView(LoginRequiredMixin, ListView):
    model = Resume
    template_name = 'resume/resume_list.html'
    context_object_name = 'resumes'

    def get_queryset(self):
        # Candidates only see their own resumes
        return Resume.objects.filter(user=self.request.user).order_by('-updated_at')

class ResumeCreateView(LoginRequiredMixin, CreateView):
    model = Resume
    fields = ['title', 'description', 'expected_salary', 'is_anonymous', 'is_active']
    template_name = 'resume/resume_form.html'
    success_url = reverse_lazy('resume:list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class ResumeUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Resume
    fields = ['title', 'description', 'expected_salary', 'is_anonymous', 'is_active']
    template_name = 'resume/resume_form.html'
    success_url = reverse_lazy('resume:list')

    def test_func(self):
        resume = self.get_object()
        return self.request.user == resume.user

class ResumeDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Resume
    template_name = 'resume/resume_confirm_delete.html'
    success_url = reverse_lazy('resume:list')

    def test_func(self):
        resume = self.get_object()
        return self.request.user == resume.user
