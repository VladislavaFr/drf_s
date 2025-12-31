from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from lms.models import Course, Subscription

@shared_task
def send_course_update_email(course_id):
    try:
        course = Course.objects.get(id=course_id)
    except Course.DoesNotExist:
        return

    subscriptions = Subscription.objects.filter(course=course)
    emails = [s.user.email for s in subscriptions]

    if not emails:
        return

    send_mail(
        subject=f"Обновление курса: {course.title}",
        message=f"В курсе '{course.title}' появились новые материалы.",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=emails,
        fail_silently=True,
    )
