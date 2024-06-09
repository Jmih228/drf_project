from rest_framework import serializers
from courses.models import Course, Lesson, Subscription, Payment
from courses.validators import TitleLinksValidator, DescriptionLinksValidator


class PaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payment
        fields = '__all__'


class LessonSerializer(serializers.ModelSerializer):

    validators = [TitleLinksValidator(field='title'), DescriptionLinksValidator(field='description')]

    class Meta:
        model = Lesson
        fields = '__all__'


class SubscriptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subscription
        fields = '__all__'


class CoursesSerializer(serializers.ModelSerializer):

    validators = [TitleLinksValidator(field='title'), DescriptionLinksValidator(field='description')]

    is_subscribed = serializers.SerializerMethodField()
    lessons_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(source='lesson_set', read_only=True, many=True)

    class Meta:
        model = Course
        fields = ('id', 'title', 'description', 'owner', 'lessons_count', 'lessons', 'is_subscribed')

    def get_lessons_count(self, instance):
        return len(Lesson.objects.filter(id=instance.id))

    def get_is_subscribed(self, instance):
        return bool(Subscription.objects.filter(user=self.context['request'].user, course=instance))
