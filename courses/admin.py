from django.contrib import admin
from courses.models import Course, Lesson


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):

    list_display = ('id', 'title')
    list_filter = ('id', 'title')
    search_fields = ('id', 'title')


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):

    list_display = ('id', 'title', 'link')
    list_filter = ('id', 'title', 'link')
    search_fields = ('id', 'title', 'link')
