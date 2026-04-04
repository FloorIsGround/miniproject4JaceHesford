from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("bills.urls")),
    path("accounts/", include("accounts.urls")),
]
