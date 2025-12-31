from django.db import models
from django.conf import settings
from lms.models import Course


class Payment(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="payments",
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="payments",
    )
    amount = models.PositiveIntegerField()
    stripe_session_id = models.CharField(max_length=255, blank=True, null=True)
    payment_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} — {self.course}"
