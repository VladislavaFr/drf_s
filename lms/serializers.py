from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from lms.models import Course, Lesson, Subscription
from lms.validators import validate_video_url


class LessonSerializer(serializers.ModelSerializer):
    video_url = serializers.URLField(
        required=False,
        allow_null=True,
        validators=[validate_video_url],
    )

    class Meta:
        model = Lesson
        fields = "__all__"
        read_only_fields = ("owner",)


class CourseSerializer(serializers.ModelSerializer):
    lesson_count = SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)
    is_subscribed = SerializerMethodField()

    def get_lesson_count(self, obj):
        return obj.lessons.count()

    def get_is_subscribed(self, obj):
        user = self.context["request"].user
        if user.is_anonymous:
            return False
        return Subscription.objects.filter(user=user, course=obj).exists()

    class Meta:
        model = Course
        fields = (
            "id",
            "title",
            "description",
            "preview",
            "price",
            "owner",
            "lesson_count",
            "lessons",
            "is_subscribed",
        )
        read_only_fields = ("owner",)
