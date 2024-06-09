from courses.apps import CoursesConfig
from rest_framework.routers import DefaultRouter
from courses.views import (CoursesViewSet,
                           LessonCreateAPIView,
                           LessonListAPIView,
                           LessonRetrieveAPIView,
                           LessonUpdateAPIView,
                           LessonDestroyAPIView,
                           SubscriptionAPIView,
                           PaymentCreateAPIView,)
from django.urls import path


app_name = CoursesConfig.name

router = DefaultRouter()
router.register(r'courses', CoursesViewSet, basename='courses')

urlpatterns = [
    path('lessons/create', LessonCreateAPIView.as_view(), name='lesson_create'),
    path('lessons/', LessonListAPIView.as_view(), name='lessons_list'),
    path('lessons/<int:pk>/', LessonRetrieveAPIView.as_view(), name='lesson'),
    path('lessons/update/<int:pk>/', LessonUpdateAPIView.as_view(), name='lesson_update'),
    path('lessons/delete/<int:pk>/', LessonDestroyAPIView.as_view(), name='lesson_delete'),
    path('courses/<int:pk>/subscribtion', SubscriptionAPIView.as_view(), name='course_subscription'),
    path('payment/', PaymentCreateAPIView.as_view(), name='payment_create'),
] + router.urls
