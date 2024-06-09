from django.db import models
from django.conf import settings


class Course(models.Model):

    title = models.CharField(max_length=150, verbose_name='Название')
    preview = models.ImageField(upload_to='previews/', null=True, blank=True, verbose_name='Превью')
    description = models.TextField(verbose_name='Описание')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                              null=True, blank=True, related_name='User_as_course_owner')

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'

    def __str__(self):
        return self.title


class Lesson(models.Model):

    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Курс')
    title = models.CharField(max_length=150, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    preview = models.ImageField(upload_to='lesson_prewivews/', null=True, blank=True, verbose_name='Превью')
    link = models.URLField(verbose_name='Ссылка')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                              null=True, blank=True, related_name='User_as_lesson_owner')

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'


class Subscription(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                             verbose_name='Пользователь', related_name='User_as_subscriber')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Курс')

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'


class Payment(models.Model):

    amount = models.PositiveIntegerField(verbose_name='Сумма оплаты')
    session_id = models.CharField(max_length=255, null=True, blank=True, verbose_name='id сессии оплаты')
    link = models.URLField(max_length=500, null=True, blank=True, verbose_name='Ссылка на оплату')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
                             null=True, blank=True, verbose_name='Пользователь',
                             related_name='User_as_payer')

    class Meta:
        verbose_name = 'Платеж'
        verbose_name_plural = 'Платежи'
