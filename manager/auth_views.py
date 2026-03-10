"""
Authentication views for user registration, login, and logout
"""
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages


def register_view(request):
    """User registration view"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('manager:login')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserCreationForm()

    return render(request, 'registration/register.html', {'form': form})


def login_view(request):
    """User login view"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {username}!')
            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)
            return redirect('manager:file_manager')
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'registration/login.html')


@require_POST
def logout_view(request):
    """User logout view"""
    logout(request)
    messages.info(request, 'You have been logged out successfully.')
    return redirect('manager:login')


@login_required
def profile_view(request):
    """User profile view showing connected cloud drives"""
    from .models import CloudStorageToken

    tokens = CloudStorageToken.objects.filter(user=request.user)
    connected_providers = set(tokens.values_list('provider', flat=True))

    context = {
        'user': request.user,
        'tokens': tokens,
        'connected_providers': connected_providers,
    }

    return render(request, 'registration/profile.html', context)
