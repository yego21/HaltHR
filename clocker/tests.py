from django.test import TestCase

# Create your tests here.
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.utils import timezone
from .models import Clocker
from django.urls import reverse

class ClockerViewsTest(TestCase):

    def setUp(self):


        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')
        self.clock_in_url = '/clock-in/'  # Update with your actual URL pattern name if different
        self.clock_out_url = '/clock-out/'  # Update with your actual URL pattern name if different

    def test_clock_in(self):
        response = self.client.post(self.clock_in_url)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'status': 'success', 'message': 'Clock in time recorded successfully.'})
        clocker = Clocker.objects.get(user=self.user, date=timezone.localdate())
        self.assertIsNotNone(clocker.time_in)

    def test_double_clock_in(self):
        self.client.post(self.clock_in_url)
        response = self.client.post(self.clock_in_url)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'status': 'failure', 'message': 'testuser has already clocked in for today, please proceed to clock out or contact your system administrator'})
        clockers = Clocker.objects.filter(user=self.user, date=timezone.localdate())
        self.assertEqual(clockers.count(), 1)


    def test_clock_out_after_clock_in(self):
        self.client.post(self.clock_in_url)
        response = self.client.post(self.clock_out_url)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'status': 'success', 'message': 'Clock out time recorded successfully.'})
        clocker = Clocker.objects.get(user=self.user, date=timezone.localdate())
        self.assertIsNotNone(clocker.time_out)

    def test_double_clock_out(self):
        self.client.post(self.clock_in_url)
        self.client.post(self.clock_out_url)
        response = self.client.post(self.clock_out_url)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'status': 'failure', 'message': 'testuser has already clocked out for today, record not submitted.'})
        clockers = Clocker.objects.filter(user=self.user, date=timezone.localdate())
        self.assertEqual(clockers.count(), 1)
        clocker = clockers.first()
        self.assertIsNotNone(clocker.time_out)


    def test_clock_in_and_out_on_different_dates(self):
        # Simulate clocking in on one day
        clock_in_time = timezone.make_aware(timezone.datetime(2024, 7, 28, 9, 0, 0))
        Clocker.objects.create(user=self.user, date=clock_in_time.date(), time_in=clock_in_time)

        # Simulate clocking out on the next day
        clock_out_time = timezone.make_aware(timezone.datetime(2024, 7, 29, 17, 0, 0))
        response = self.client.post(self.clock_out_url, {'confirm': 'yes'}, HTTP_X_CSRFTOKEN='your_csrf_token')
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content,
                             {'status': 'success', 'message': 'Clock out time recorded successfully.'})

    def test_clock_in_and_out_on_the_same_day(self):
        # Simulate clocking in and out on the same day
        clock_in_time = timezone.make_aware(timezone.datetime(2024, 7, 28, 9, 0, 0))
        Clocker.objects.create(user=self.user, date=clock_in_time.date(), time_in=clock_in_time)

        # Simulate clocking out on the same day
        clock_out_time = timezone.make_aware(timezone.datetime(2024, 7, 28, 17, 0, 0))
        response = self.client.post(self.clock_out_url, {'confirm': 'yes'}, HTTP_X_CSRFTOKEN='your_csrf_token')
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content,
                             {'status': 'success', 'message': 'Clock out time recorded successfully.'})

    def test_clock_out_without_clock_in(self):
        # Simulate clocking in without clocking out on the same day
        clock_in_time = timezone.make_aware(timezone.datetime(2024, 7, 28, 9, 0, 0))
        Clocker.objects.create(user=self.user, date=clock_in_time.date(), time_in=clock_in_time)

        # Attempting to clock out without clocking in should result in a failure
        response = self.client.post(self.clock_out_url)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'status': 'confirm',
                                                'message': 'testuser does not have Clock in record for today, are you sure you want to Clock out?'})

    def test_multiple_clock_ins(self):
        # Perform initial clock in
        response = self.client.post(self.clock_in_url)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'status': 'success', 'message': 'Clock in time recorded successfully.'})

        # Attempt another clock in
        response = self.client.post(self.clock_in_url)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'status': 'failure', 'message': 'testuser has already clocked in for today, please proceed to clock out or contact your system administrator'})

    def test_clock_out_without_clock_in(self):
        # Simulate an attempt to clock out without any prior clock in
        response = self.client.post(self.clock_out_url)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content,
                             {'status': 'confirm', 'message': 'testuser does not have Clock in record for today, are you sure you want to Clock out?'})





