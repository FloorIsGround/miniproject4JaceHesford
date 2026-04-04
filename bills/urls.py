from django.urls import path
from . import views

app_name = "bills"

urlpatterns = [
    path("", views.home, name="home"),
    path("bills/", views.bill_list, name="bill_list"),
    path("bills/<str:bill_number>/", views.bill_detail, name="bill_detail"),
]
