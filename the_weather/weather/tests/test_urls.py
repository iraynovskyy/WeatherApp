from django.test import TestCase, Client
from django.urls import reverse, resolve
from django.contrib.auth.models import User
# from api.views import home, user_signup
from weather.models import City

class TestUrls(TestCase):

    def setUp(self):
        test_user1 = User.objects.create_user(username='testuser1', password='12345') 
        test_user1.save()
        test_user2 = User.objects.create_user(username='testuser2', password='12345') 
        test_user2.save()

    def test_home_resolves(self):
        # assert 1 == 2
        # client = Client()
        url = reverse('home')
        resp = self.client.get(url)
        
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'weather.html')


    def test_redirect_if_not_logged_in(self):
        
        resp = self.client.get(reverse('delete_city', args=['Cuba']))
        # print('resp_not_logged_in=',resp)
        self.assertRedirects(resp, '/login/?next=/delete/Cuba/')

    def test_logged_in_uses_correct_template(self):

        login = self.client.login(username='testuser1', password='12345')
        resp = self.client.get(reverse('home'))

        # checking that user had logged in
        self.assertEqual(str(resp.context['user']), 'testuser1')
        # print('rest.context =',resp.context)

        # checking the response after request
        self.assertEqual(resp.status_code, 200)

        # checking that we use the right template
        self.assertTemplateUsed(resp, 'weather.html') 

    def test_logout_uses_correct_template(self):

        login = self.client.login(username='testuser1', password='12345')
        resp = self.client.get(reverse('home'))

        # checking that user had logged in
        self.assertEqual(str(resp.context['user']), 'testuser1')

        logout = self.client.logout()
        resp = self.client.get(reverse('home'))
        # checkign that user had logged out
        self.assertEqual(str(resp.context['user']), 'AnonymousUser')

        # checking the response after request
        self.assertEqual(resp.status_code, 200)

        # checking that we use the right template
        self.assertTemplateUsed(resp, 'weather.html') 

    def test_register_uses_correct_template(self):
        
        # checkign if it is an Anonynous user
        resp = self.client.get(reverse('home'))
        self.assertEqual(str(resp.context['user']), 'AnonymousUser')

        resp = self.client.get(reverse('register'))
        # checking the response after request
        self.assertEqual(resp.status_code, 200)

        # checking that we use the right template
        self.assertTemplateUsed(resp, 'register.html')
