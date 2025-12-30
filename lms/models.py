from django.db import models
from django.conf import settings


class Course(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    preview = models.ImageField(upload_to="courses/", blank=True, null=True)
    price = models.PositiveIntegerField(default=0)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="courses",
    )

    def __str__(self):
        return self.title


class Lesson(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="lessons",
    )
    title = models.CharField(max_length=255)
    description = models.TextField()
    preview = models.ImageField(upload_to="lessons/", blank=True, null=True)
    video_url = models.URLField(blank=True, null=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="lessons",
    )

    def __str__(self):
        return self.title


class Subscription(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="subscriptions",
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="subscriptions",
    )

    class Meta:
        unique_together = ("user", "course")
