from network.views import following
from django.test import Client, TestCase

from .models import User, Post, Follow, Likes

# Create your tests here.

class case(TestCase):

    def setUp(self):

        # users
        u1 = User.objects.create(username="billy", password="password", email="mail@foo.com")
        u2 = User.objects.create(username="John", password="password", email="mail2@foo.com")


        # posts
        p1 = Post.objects.create(user=u1, body="billy posts wa")
        Post.objects.create(user=u1, body="billy second posts wa")
        Post.objects.create(user=u2, body="John wants to post!")

        Follow.objects.create(follower=u1, followed=u2)

        Likes.objects.create(post=p1, user=u1)

    def test_user_posts(self):
        user = User.objects.get(username="billy")
        self.assertEqual(Post.objects.filter(user=user).count(), 2)

        user = User.objects.get(username="John")
        self.assertEqual(Post.objects.filter(user=user).count(), 1)


    def test_follow(self):
        c1 = Follow.objects.filter(follower__username="billy").count()
        c2 = Follow.objects.filter(followed__username="John").count()
        self.assertEqual(c1, 1)
        self.assertEqual(c2, 1)


    def test_register_like(self):
        self.assertEqual(Likes.objects.filter(user__username="billy").count(), 1)
        self.assertEqual(Likes.objects.filter(user__username="John").count(), 0)
        self.assertEqual(Likes.objects.filter(post__user__username="billy").count(), 1)
        self.assertEqual(Likes.objects.filter(post__user__username="John").count(), 0)

    # error, i can create more user likes for the single post, but i don't know how to prevent this
    # only using django models.

    def test_valid_get_no_login(self):
        c = Client()

        # should be accessible without login
        accessible_urls = ['/', '/login', '/register']

        for url in accessible_urls:
            response = c.get(url)
            self.assertEqual(response.status_code, 200)
        