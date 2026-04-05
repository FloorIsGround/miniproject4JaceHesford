from django.urls import path
from . import views

app_name = "bills"

urlpatterns = [
    path("", views.home, name="home"),
    path("bills/", views.bill_list, name="bill_list"),
    path("bills/<str:bill_number>/", views.bill_detail, name="bill_detail"),
    path("bills/<str:bill_number>/comment/", views.add_comment, name="add_comment"),
    path("bills/<str:bill_number>/comment/<int:comment_id>/delete/", views.delete_comment, name="delete_comment"),
    path("bills/<str:bill_number>/vote/", views.vote, name="vote"),
]
