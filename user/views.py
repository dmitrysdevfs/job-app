from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('user:dashboard')
    else:
        form = UserRegistrationForm()
    return render(request, 'user/register.html', {'form': form})

@login_required
def dashboard(request):
    if request.user.is_recruiter:
        return render(request, 'user/dashboard_recruiter.html')
    return render(request, 'user/dashboard_candidate.html')
