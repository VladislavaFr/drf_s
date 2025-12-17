from django.urls import path
from rest_framework.routers import DefaultRouter
from lms.views import (
    CourseViewSet,
    LessonCreateAPIView,
    LessonListAPIView,
    LessonRetrieveAPIView,
    LessonUpdateAPIView,
    LessonDestroyAPIView,
)

router = DefaultRouter()
router.register("courses", CourseViewSet)

urlpatterns = [
    path("lessons/", LessonListAPIView.as_view()),
    path("lessons/create/", LessonCreateAPIView.as_view()),
    path("lessons/<int:pk>/", LessonRetrieveAPIView.as_view()),
    path("lessons/<int:pk>/update/", LessonUpdateAPIView.as_view()),
    path("lessons/<int:pk>/delete/", LessonDestroyAPIView.as_view()),
]

urlpatterns += router.urls
