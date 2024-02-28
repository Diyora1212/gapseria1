from django.test import TestCase

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Opinion


class UserOpinionTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')

        Opinion.objects.create(author=self.user, body='Opinion 1')
        Opinion.objects.create(author=self.user, body='Opinion 2')

    def test_user_login(self):
        response = self.client.post(reverse('gap:login-page'), {'username': 'testuser', 'password': 'testpass'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse(
            'gap:rooms'))

    def test_user_register(self):
        response = self.client.post(reverse('gap:register-page'),
                                    {'username': 'newuser', 'password1': 'newpass123', 'password2': 'newpass123'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse(
            'gap:rooms'))
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_opinion_list(self):
        self.client.login(username='testuser', password='testpass')

        response = self.client.get(reverse('gap:opinion-list'))
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, 'Opinion 1')
        self.assertContains(response, 'Opinion 2')
