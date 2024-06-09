from rest_framework.test import (APITestCase,
                                 APIClient)
from rest_framework import status
from courses.models import Course, Lesson
from users.models import CustomUser


class LessonsTestCase(APITestCase):

    def setUp(self) -> None:
        self.user = CustomUser.objects.create(email='user@sky.pro', password='hghghg777')

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.course = Course.objects.create(
            title='Course4test',
            description='Course4test'
        )

        self.lesson = Lesson.objects.create(
            title='Lesson4test',
            description='Lesson4test',
            course=self.course,
            link='http://localhost:8000/lessons/12/',
            owner=self.user
        )

    def test_lesson_create(self):

        data = {
            'title': self.lesson.title,
            'description': self.lesson.description,
            'course': Course.objects.get(id=1).id,
            'link': self.lesson.link
        }

        response = self.client.post(
            '/lessons/create',
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertEqual(
            response.json(),
            {'id': 2, 'title': 'Lesson4test', 'description': 'Lesson4test',
             'preview': None, 'link': 'http://localhost:8000/lessons/12/',
             'course': 1, 'owner': 1}
        )

    def test_lesson_read(self):

        response = self.client.get(
            f'/lessons/{self.lesson.id}/'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_lesson_update(self):

        data = {
            'title': 'update',
            'description': 'update'
        }

        response = self.client.patch(
            f'/lessons/update/{self.lesson.id}/',
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json(),
            {'id': 5, 'title': 'update', 'description': 'update',
             'preview': None, 'link': 'http://localhost:8000/lessons/12/',
             'course': 4, 'owner': 4}
        )

    def test_lesson_delete(self):

        response = self.client.delete(f'/lessons/delete/{self.lesson.id}/')

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )

    def test_subscription(self):

        data = {
            'user': self.user,
            'course': self.course.id
        }

        response = self.client.post(
            f'/courses/{Course.objects.get(id=self.course.id).id}/subscription',
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
