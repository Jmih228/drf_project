from rest_framework.pagination import PageNumberPagination


class CoursesPaginator(PageNumberPagination):
    page_size = 5


class LessonsPaginator(PageNumberPagination):
    page_size = 10
