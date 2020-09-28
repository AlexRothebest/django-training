from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User as AuthUser

from authentication.models import User


def login(request):
    if request.method == 'GET':
        return render(request, 'auth/login.html')
    elif request.method == 'POST':
        request_body = dict(request.POST)

        email = request_body.get('email')[0]
        password = request_body.get('password')[0]

        if email == '' or password == '':
            return render(request, 'auth/login.html', {
                'error': 'The form has been filled out incorrectly'
            })

        user = authenticate(request, username=email, password=password)
        if user is None:
            return render(request, 'auth/login.html', {
                'error': 'Wrong email or password'
            })

        auth_login(request, user)

        return redirect('/')


def sign_up(request):
    if request.method == 'GET':
        return render(request, 'auth/sign_up.html')
    elif request.method == 'POST':
        request_body = dict(request.POST)

        name = request_body.get('name')[0]
        surname = request_body.get('surname')[0]
        email = request_body.get('email')[0]
        password = request_body.get('password')[0]
        retype_password = request_body.get('retype-password')[0]

        if name == '' or surname == '' or email == '' or password == '' or password != retype_password:
            return render(request, 'auth/sign_up.html', {
                'error': 'The form has been filled out incorrectly'
            })

        new_auth_user = AuthUser(
            first_name=name,
            last_name=surname,
            username=email,
            email=email
        )
        new_auth_user.set_password(password)
        new_auth_user.save()

        auth_login(request, new_auth_user)

        new_user = User(
            name=name,
            surname=surname,
            email=email,
            auth_user=new_auth_user
        )
        new_user.save()

        return redirect('/')


def logout(request):
    auth_logout(request)

    return redirect('/')
