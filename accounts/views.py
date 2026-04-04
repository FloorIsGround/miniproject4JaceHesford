from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


def register(request):
    return render(request, "accounts/register.html")


@login_required
def profile(request):
    return render(request, "accounts/profile.html")
