from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from .forms import LoginForm, RegisterForm, UserProfileForm, AdminUserEditForm
from .models import User
from evidence.models import AuditLog, Evidence

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard_dispatch')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                if user.status != 'active':
                    messages.error(request, 'Your account is deactivated. Please contact an Administrator.')
                    return render(request, 'login.html', {'form': form})

                login(request, user)
                AuditLog.objects.create(
                    user=user,
                    action='USER_LOGIN',
                    details=f"User {user.username} logged in successfully.",
                    ip_address=get_client_ip(request)
                )
                messages.success(request, f"Welcome back, {user.first_name or user.username}!")
                return redirect('dashboard_dispatch')
            else:
                messages.error(request, 'Invalid username or password. Please try again.')
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})


def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard_dispatch')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()

            AuditLog.objects.create(
                user=user,
                action='USER_REGISTER',
                details=f"New user {user.username} registered with role: {user.role}.",
                ip_address=get_client_ip(request)
            )
            messages.success(request, 'Registration successful! You may now sign in with your credentials.')
            return redirect('login')
    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})


@login_required
def logout_view(request):
    user = request.user
    AuditLog.objects.create(
        user=user,
        action='USER_LOGOUT',
        details=f"User {user.username} logged out.",
        ip_address=get_client_ip(request)
    )
    logout(request)
    messages.info(request, 'You have been logged out securely.')
    return redirect('login')


@login_required
def dashboard_dispatch(request):
    if request.user.is_admin():
        return redirect('admin_dashboard')
    return redirect('user_dashboard')


@login_required
def profile_view(request):
    user = request.user
    if request.method == 'POST':
        if 'update_profile' in request.POST:
            profile_form = UserProfileForm(request.POST, instance=user)
            pwd_form = PasswordChangeForm(user)
            if profile_form.is_valid():
                profile_form.save()
                messages.success(request, 'Profile information updated successfully.')
                return redirect('profile')
        elif 'change_password' in request.POST:
            pwd_form = PasswordChangeForm(user, request.POST)
            profile_form = UserProfileForm(instance=user)
            if pwd_form.is_valid():
                user_updated = pwd_form.save()
                update_session_auth_hash(request, user_updated)
                AuditLog.objects.create(
                    user=user,
                    action='PASSWORD_CHANGE',
                    details="Password changed successfully.",
                    ip_address=get_client_ip(request)
                )
                messages.success(request, 'Your password was updated successfully.')
                return redirect('profile')
    else:
        profile_form = UserProfileForm(instance=user)
        pwd_form = PasswordChangeForm(user)

    upload_count = Evidence.objects.filter(user=user).count()
    verified_count = Evidence.objects.filter(user=user, status='Verified').count()

    context = {
        'profile_form': profile_form,
        'pwd_form': pwd_form,
        'upload_count': upload_count,
        'verified_count': verified_count,
    }
    return render(request, 'user/profile.html', context)
