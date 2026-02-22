from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView, View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Resume, ContactRequest

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

class PublicResumeListView(ListView):
    """Спільний список резюме для рекрутерів"""
    model = Resume
    template_name = 'resume/public_list.html'
    context_object_name = 'resumes'

    def get_queryset(self):
        return Resume.objects.filter(is_active=True).order_by('-updated_at')

class ResumeDetailView(DetailView):
    """Детальний перегляд резюме з логікою приватності"""
    model = Resume
    template_name = 'resume/resume_detail.html'
    context_object_name = 'resume'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        resume = self.object
        user = self.request.user
        
        context['can_see_contacts'] = False
        
        if not resume.is_anonymous:
            context['can_see_contacts'] = True
        elif user.is_authenticated:
            if user == resume.user or user.is_superuser:
                context['can_see_contacts'] = True
            else:
                # Check if there is an approved contact request from this recruiter
                request_status = ContactRequest.objects.filter(
                    resume=resume, recruiter=user, status=ContactRequest.Status.APPROVED
                ).exists()
                context['can_see_contacts'] = request_status
                
                # Check if a request is already pending
                context['has_pending_request'] = ContactRequest.objects.filter(
                    resume=resume, recruiter=user, status=ContactRequest.Status.PENDING
                ).exists()
        
        return context

class RequestContactView(LoginRequiredMixin, View):
    """Рекрутер запитує контакти кандидата"""
    def post(self, request, pk):
        resume = get_object_or_404(Resume, pk=pk)
        if not (request.user.is_recruiter or request.user.is_superuser):
            messages.error(request, "Тільки рекрутери можуть запитувати контакти.")
            return redirect('resume:detail', pk=pk)
        
        ContactRequest.objects.get_or_create(
            resume=resume, 
            recruiter=request.user,
            defaults={'message': request.POST.get('message', '')}
        )
        messages.success(request, "Запит надіслано. Очікуйте на підтвердження від кандидата.")
        return redirect('resume:detail', pk=pk)

class ApproveContactRequestView(LoginRequiredMixin, View):
    """Кандидат схвалює запит рекрутера"""
    def post(self, request, pk):
        contact_request = get_object_or_404(ContactRequest, pk=pk, resume__user=request.user)
        contact_request.status = ContactRequest.Status.APPROVED
        contact_request.save()
        messages.success(request, "Запит схвалено. Рекрутер тепер бачить ваші контакти.")
        return redirect('user:dashboard')

class RejectContactRequestView(LoginRequiredMixin, View):
    """Кандидат відхиляє запит рекрутера"""
    def post(self, request, pk):
        contact_request = get_object_or_404(ContactRequest, pk=pk, resume__user=request.user)
        contact_request.status = ContactRequest.Status.REJECTED
        contact_request.save()
        messages.info(request, "Запит відхилено.")
        return redirect('user:dashboard')
