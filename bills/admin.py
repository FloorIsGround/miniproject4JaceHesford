from django.contrib import admin
from .models import Bill, BillAnalysis, Comment, Vote


class BillAnalysisInline(admin.StackedInline):
    model = BillAnalysis
    extra = 1
    readonly_fields = ("created_by", "created_at")

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(Bill)
class BillAdmin(admin.ModelAdmin):
    list_display = ("bill_number", "short_title", "status", "last_fetched")
    search_fields = ("bill_number", "short_title", "long_title")
    inlines = [BillAnalysisInline]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("author", "bill", "created_at")
    list_filter = ("bill",)
    actions = ["delete_selected"]
    readonly_fields = ("author", "bill", "body", "created_at")


@admin.register(BillAnalysis)
class BillAnalysisAdmin(admin.ModelAdmin):
    list_display = ("bill", "created_by", "created_at")
    readonly_fields = ("created_by", "created_at")

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ("user", "bill", "value")
    list_filter = ("value", "bill")
    readonly_fields = ("user", "bill", "value")

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False
