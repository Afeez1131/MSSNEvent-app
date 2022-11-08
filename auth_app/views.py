import json

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from .forms import CustomUserCreationForm, GenUser
import string
import random
from django.contrib.auth import get_user_model
from .models import CustomUser


def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            return HttpResponseRedirect(reverse('login'))
    form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form, })


@login_required
def gen_user(request):
    User = get_user_model()
    options = string.digits + string.ascii_letters
    base_user = 'testuser'
    if request.method == 'POST':
        if request.POST.get('action') == 'create_user':
            while User.objects.filter(username=base_user).exists():
                base_user += random.choice(options)
            user = User.objects.create_user(username=base_user)
            user.set_password('password')
            user.save()
            print(user)
        elif request.POST.get('action') == 'reset_password':
            uid = request.POST.get('user')
            user = User.objects.get(id=uid)
            user.set_password('password')
            user.save()

    recent_users = User.objects.all().order_by('-id')[:10]
    return render(request, 'gen_user.html', {'username': base_user, 'recent_users': recent_users})


@login_required
def reset_password(request):
    User = get_user_model()

    if request.method == 'POST':
        if request.POST.get('action') == 'reset_password':
            uid = request.POST.get('uid')
            user = User.objects.get(id=uid)
            user.set_password('password')
            user.save()

    return JsonResponse({'success': 'Okay'})


def reload_users():
    User = get_user_model()
    users = User.objects.all()
    users = [user for user in users]
    print(users)
    out = []
    # for user in users:
    for i in range(len(users)):
        user = users[i]
        data = f'<tr><td>{i+1}</td><td>{user.username}</td><td><button type="submit" class="btn btn-md btn-warning" onclick="setFormValue({user.id});">Reset Password</button></td>'
        out.append(data)
    return out


def generate_user(request):
    User = get_user_model()
    options = string.digits + string.ascii_letters
    base_user = 'testuser' + ''.join(random.choice(options) for _ in range(3))
    user = User.objects.filter(username=base_user)
    if not user.exists():
        user = User.objects.create_user(username=base_user, password='password')

    return JsonResponse({'users': reload_users()})
