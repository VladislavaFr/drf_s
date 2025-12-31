from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import get_user_model

User = get_user_model()

@shared_task
def block_inactive_users():
    one_month_ago = timezone.now() - timedelta(days=30)
    User.objects.filter(last_login__lt=one_month_ago, is_active=True).update(is_active=False)
