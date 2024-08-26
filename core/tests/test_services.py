import uuid

from django.test import TestCase
from service_objects.services import ServiceOutcome

from apps.users.models import Customer
from core.models import Comment, Post
from core.services.comment.get import CommentGetService


class TestCommentServices(TestCase):
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
        self.data['comment'] = Comment.objects.create(
            post=self.data['post'],
            user=self.data['user'],
            text='test_comment 0'
        )

    def test_comment_get_service(self):
        comment_from_manager = Comment.objects.get(user=self.data['user'], post=self.data['post'])
        comment_from_service = ServiceOutcome(
            CommentGetService,
            {'slug': comment_from_manager.slug}
        ).result
        self.assertIsInstance(comment_from_service, Comment)
        self.assertEqual(comment_from_manager, comment_from_service)
