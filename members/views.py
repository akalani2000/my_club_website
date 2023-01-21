from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .forms import RegisterUserForm


# Login user
def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'You logged in successfully')
            return redirect('home')
        else:
            messages.success(request, 'Login failed, Please try again!')
            return redirect('login-user')
    else:
        return render(request, 'authenticate/login.html', {})


# logout user
def logout_user(request):
    logout(request)
    messages.success(request, 'Your are Logged out from system')
    return redirect('home')


# Register user
def register_user(request):
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, 'Registration Successful!')
            return redirect('home')
    else:
        form = RegisterUserForm()

    return render(request, 'authenticate/registration.html', {'form': form})
