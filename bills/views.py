from django.shortcuts import render, get_object_or_404

from .models import Bill
from . import services


def home(request):
    # Show a handful of recently cached bills without triggering a full refresh
    recent_bills = Bill.objects.order_by("-last_fetched")[:5]
    return render(request, "home.html", {"recent_bills": recent_bills})


def bill_list(request):
    query = request.GET.get("q", "").strip()
    bills = services.get_bill_list()
    if query:
        bills = bills.filter(bill_number__icontains=query) | bills.filter(
            short_title__icontains=query
        )
        bills = bills.order_by("bill_number")
    return render(request, "bills/bill_list.html", {"bills": bills, "query": query})


def bill_detail(request, bill_number):
    bill = services.get_bill(bill_number)
    if bill is None:
        from django.http import Http404
        raise Http404("Bill not found.")
    analyses = bill.analyses.select_related("created_by").order_by("-created_at")
    return render(
        request,
        "bills/bill_detail.html",
        {"bill": bill, "analyses": analyses},
    )
