from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import Course, Lesson, Subscription

User = get_user_model()


class CourseLessonTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='testuser@example.com', password='testpassword')
        self.user2 = User.objects.create_user(email='user2@example.com', password='password56')

        self.client.force_authenticate(user=self.user)

        self.course = Course.objects.create(title='Python Course', description='Learn Python', owner=self.user)

        self.lesson1 = Lesson.objects.create(course=self.course, title='Lesson 1', video_url='https://youtube.com/video1')
        self.lesson2 = Lesson.objects.create(course=self.course, title='Lesson 2', video_url='https://youtube.com/video2')

    def test_create_lesson(self):
        data = {
            'course': self.course.id,
            'title': 'New Lesson',
            'video_url': 'https://youtube.com/video3'
        }
        response = self.client.post('/api/lessons/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_invalid_video_url(self):
        data = {
            'course': self.course.id,
            'title': 'Invalid Lesson',
            'video_url': 'https://notyoutube.com/video'
        }
        response = self.client.post('/api/lessons/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_toggle_subscription(self):
        data = {'course_id': self.course.id}
        response = self.client.post('/api/subscriptions/toggle/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Подписка добавлена')

        response = self.client.post('/api/subscriptions/toggle/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Подписка удалена')
