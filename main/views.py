from django.shortcuts import render, redirect
from django.http import HttpResponse


def home(request):
    if not request.user.is_authenticated:
        return redirect('/auth/login')

    return redirect('/polls')
