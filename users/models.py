from django.db import models
from django.contrib.auth.models import AbstractUser
from courses.models import Lesson, Course


class CustomUser(AbstractUser):
    username = None

    email = models.EmailField(unique=True, verbose_name='Почта')
    phone = models.CharField(max_length=15, null=True, blank=True, verbose_name='Телефон')
    city = models.CharField(max_length=100, null=True, blank=True, verbose_name='Город')
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True, verbose_name='Аватар')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email


class Payment(models.Model):
    WAYS_OF_PAYMENT = (
        ('cash_payment', 'Оплата наличными'),
        ('transaction', 'Перевод')
    )

    user = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING, null=True, blank=True, verbose_name='Пользователь')
    date = models.DateTimeField(auto_now_add=True, verbose_name='Дата исполнения платежа')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, blank=True, null=True)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, blank=True, null=True)
    cost = models.IntegerField(verbose_name='Сумма оплаты')
    way_of_payment = models.CharField(max_length=20, choices=WAYS_OF_PAYMENT, verbose_name='Способ оплаты')
