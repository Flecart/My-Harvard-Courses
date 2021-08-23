from django.test import Client, TestCase

from .models import User, Post, Follow

# Create your tests here.

class case(TestCase):

    def setUp(self):

        # users
        u1 = User.objects.create(username="billy", password="password", email="mail@foo.com")
        u2 = User.objects.create(username="John", password="password", email="mail2@foo.com")


        # posts
        Post.objects.create(user=u1, body="billy posts wa")
        Post.objects.create(user=u1, body="billy second posts wa")
        Post.objects.create(user=u2, body="John wants to post!")


    def test_user_posts(self):
        user = User.objects.get(username="billy")
        self.assertEqual(Post.objects.filter(user=user).count(), 2)

        user = User.objects.get(username="John")
        self.assertEqual(Post.objects.filter(user=user).count(), 1)
