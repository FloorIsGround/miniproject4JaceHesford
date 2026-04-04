from django.shortcuts import render


def home(request):
    return render(request, "home.html")


def bill_list(request):
    return render(request, "bills/bill_list.html")


def bill_detail(request, bill_number):
    return render(request, "bills/bill_detail.html")
