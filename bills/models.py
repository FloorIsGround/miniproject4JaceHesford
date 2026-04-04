from django.db import models
from django.contrib.auth.models import User


class Bill(models.Model):
    bill_number = models.CharField(max_length=20, primary_key=True)
    short_title = models.CharField(max_length=255, blank=True)
    long_title = models.TextField(blank=True)
    status = models.CharField(max_length=100, blank=True)
    sponsors = models.TextField(blank=True)
    effective_date = models.TextField(blank=True, null=True)
    last_fetched = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.bill_number


class BillAnalysis(models.Model):
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE, related_name="analyses")
    body = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "bill analyses"

    def __str__(self):
        return f"Analysis for {self.bill_id} by {self.created_by}"


class Comment(models.Model):
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author} on {self.bill_id}"


class Vote(models.Model):
    UPVOTE = 1
    DOWNVOTE = -1
    VALUE_CHOICES = [(UPVOTE, "Upvote"), (DOWNVOTE, "Downvote")]

    bill = models.ForeignKey(Bill, on_delete=models.CASCADE, related_name="votes")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    value = models.IntegerField(choices=VALUE_CHOICES)

    class Meta:
        unique_together = ("bill", "user")

    def __str__(self):
        return f"{self.user} {'↑' if self.value == self.UPVOTE else '↓'} {self.bill_id}"
