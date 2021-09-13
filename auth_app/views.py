from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm, GenUser
import string
import random
from django.contrib.auth import get_user_model
from .models import CustomUser


def SignupView(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()

            return redirect('home')
    form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form, })


def gen_user(request):
    # username = form.cleaned_data['username']
    options = string.digits + string.ascii_letters
    # password = ''.join(random.choice(options) for _ in range(8))
    username = 'test' + ''.join(random.choice(options) for _ in range(3))
    password = 'testpass123'
    User = get_user_model()
    user = User.objects.create_user(
        username=username, password=password)
    print(user, password)

    return render(request, 'gen_user.html', {'username': username, 'password': password})
