import uuid

from django.test import TestCase
from django.urls import reverse

from apps.users.models import Customer
from core.models import Post


class TestPostViews(TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.data = dict()

    def setUp(self):
        self.data['user'] = Customer.objects.create_user(
            username='test_user0',
            email='test_email@test.com',
            password='testtesttest'
        )
        self.data['post'] = Post.objects.create(
            title='test000',
            image='/static/test/core/post/images/test.jpg',
            description='test',
            author=self.data['user']
        )

    def test_home(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_detail(self):
        response = self.client.get(reverse('post-detail', kwargs={'slug': self.data['post'].slug}))
        self.assertEqual(response.status_code, 404)  # post is still on validation

        self.data['post'].publish()
        self.data['post'].save()

        response = self.client.get(reverse('post-detail', kwargs={'slug': self.data['post'].slug}))
        self.assertEqual(response.status_code, 200)
