from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from rest_framework import viewsets, generics
from courses.serializers import (CoursesSerializer,
                                 LessonSerializer,
                                 SubscriptionSerializer,
                                 PaymentSerializer,)
from courses.models import Course, Lesson, Subscription, Payment
from rest_framework.permissions import IsAuthenticated
from users.permissions import IsNotStaff, IsOwner
from courses.paginators import CoursesPaginator, LessonsPaginator
from courses.services import creating_stripe_price, create_stripe_session
from courses.tasks import _send_mail_course_update
from users.models import CustomUser


class CoursesViewSet(viewsets.ModelViewSet):
    serializer_class = CoursesSerializer
    queryset = Course.objects.all()
    pagination_class = CoursesPaginator

    def perform_create(self, serializer):
        new_course = serializer.save()
        new_course.owner = self.request.user
        new_course.save()

    def perform_update(self, serializer):
        updated_course = serializer.save()
        recipidents = [CustomUser.objects.get(pk=Subscription.user.id).email for Subscription in Subscription.objects.filter(course=updated_course.id)]
        _send_mail_course_update.delay(*recipidents)
        updated_course.save()

    def get_permissions(self):
        if self.action == 'list':
            self.permission_classes = [IsAuthenticated]
        if self.action == 'create':
            self.permission_classes = [IsAuthenticated, IsNotStaff]
        elif self.action == 'retrieve':
            self.permission_classes = [IsAuthenticated, ~IsNotStaff | IsOwner]
        elif self.action == 'update':
            self.permission_classes = [IsAuthenticated, ~IsNotStaff | IsOwner]
        elif self.action == 'partial_update':
            self.permission_classes = [IsAuthenticated, ~IsNotStaff | IsOwner]
        elif self.action == 'destroy':
            self.permission_classes = [IsAuthenticated, IsNotStaff & IsOwner]
        return [permission() for permission in self.permission_classes]


class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsNotStaff]

    def perform_create(self, serializer):
        new_lesson = serializer.save()
        new_lesson.owner = self.request.user
        new_lesson.save()


class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated]
    pagination_class = LessonsPaginator


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, ~IsNotStaff | IsOwner]


class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, ~IsNotStaff | IsOwner]


class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsNotStaff, IsOwner]


class SubscriptionAPIView(generics.GenericAPIView):
    serializer_class = SubscriptionSerializer
    queryset = Subscription.objects.all()
    permission_classes = [IsAuthenticated]

    def post(self, *args, **kwargs):

        user = self.request.user
        course_id = self.request.parser_context['kwargs']['pk']
        course_item = get_object_or_404(Course, pk=course_id)

        subs_item = Subscription.objects.filter(user=user, course=course_id)

        if subs_item.exists():
            subs_item.delete()
            message = 'подписка удалена'
        else:
            Subscription.objects.create(user=user, course=course_item)
            message = 'подписка оформлена'

        return HttpResponse(message)


class PaymentCreateAPIView(generics.CreateAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]
    queryset = Payment.objects.all()

    def perform_create(self, serializer):
        payment = serializer.save(user=self.request.user)
        price = creating_stripe_price(payment.amount)
        session_id, payment_link = create_stripe_session(price)
        payment.session_id, payment.link = session_id, payment_link
        payment.save()
