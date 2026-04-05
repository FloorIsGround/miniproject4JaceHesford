from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum

from .models import Bill, Comment, Vote
from .forms import CommentForm
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
    comments = bill.comments.select_related("author").order_by("-created_at")
    vote_total = bill.votes.aggregate(total=Sum("value"))["total"] or 0
    user_vote = None
    if request.user.is_authenticated:
        try:
            user_vote = bill.votes.get(user=request.user).value
        except Vote.DoesNotExist:
            pass
    comment_form = CommentForm()
    return render(
        request,
        "bills/bill_detail.html",
        {
            "bill": bill,
            "analyses": analyses,
            "comments": comments,
            "comment_form": comment_form,
            "vote_total": vote_total,
            "user_vote": user_vote,
        },
    )


@login_required
def add_comment(request, bill_number):
    if request.method != "POST":
        return redirect("bills:bill_detail", bill_number=bill_number)
    bill = get_object_or_404(Bill, pk=bill_number)
    form = CommentForm(request.POST)
    if form.is_valid():
        Comment.objects.create(
            bill=bill,
            author=request.user,
            body=form.cleaned_data["body"],
        )
    return redirect("bills:bill_detail", bill_number=bill_number)


@login_required
def delete_comment(request, bill_number, comment_id):
    if request.method != "POST":
        return redirect("bills:bill_detail", bill_number=bill_number)
    comment = get_object_or_404(Comment, pk=comment_id, bill__bill_number=bill_number)
    if comment.author == request.user or request.user.is_staff:
        comment.delete()
    return redirect("bills:bill_detail", bill_number=bill_number)


@login_required
def vote(request, bill_number):
    if request.method != "POST":
        return redirect("bills:bill_detail", bill_number=bill_number)
    bill = get_object_or_404(Bill, pk=bill_number)
    value = request.POST.get("value")
    if value not in ("1", "-1"):
        return redirect("bills:bill_detail", bill_number=bill_number)
    value = int(value)
    existing = Vote.objects.filter(bill=bill, user=request.user).first()
    if existing:
        if existing.value == value:
            existing.delete()  # clicking the same button again removes the vote
        else:
            existing.value = value
            existing.save()
    else:
        Vote.objects.create(bill=bill, user=request.user, value=value)
    return redirect("bills:bill_detail", bill_number=bill_number)
