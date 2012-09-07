import unittest

from django.test import Client
from django.core import mail
from django.core.urlresolvers import reverse

from fusionbox.contact.models import Submission, Recipient


class ContactTest(unittest.TestCase):
    def setUp(self):
        self.client = Client(enforce_csrf_checks=True)

        def do_contact_form_submission(self, extra_post={}):
            url = reverse('contact_index')
            page = self.client.get(url)
            csrftoken = page.cookies['csrftoken'].value
            post_data = {
                'csrfmiddlewaretoken': csrftoken,
                'name': 'Test Name',
                'email': 'test_email@email.com',
                'uncaptcha': csrftoken,
                }
            post_data.update(extra_post)
            response = self.client.post(url, post_data)
            return response

        self.do_contact_form_submission = do_contact_form_submission

        Recipient.objects.create(name='name_1', email='email_1@email.com', is_active=True)
        Recipient.objects.create(name='name_2', email='email_2@email.com', is_active=True)
        Recipient.objects.create(name='name_3', email='email_3@email.com', is_active=False)

    def test_valid_contact_submission(self):
        count = Submission.objects.count()
        response = self.do_contact_form_submission(self)
        self.assertEquals(response.status_code, 302)
        self.assertEquals(Submission.objects.count(), count + 1)

    def test_no_name_contact_submission(self):
        count = Submission.objects.count()
        response = self.do_contact_form_submission(self, {'name': ''})
        self.assertEquals(response.status_code, 200)
        self.assertEquals(Submission.objects.count(), count)

    def test_invalid_email_contact_submission(self):
        count = Submission.objects.count()
        response = self.do_contact_form_submission(self, {'email': 'arst arst arst'})
        self.assertEquals(response.status_code, 200)
        self.assertEquals(Submission.objects.count(), count)

    def test_contact_submission_email(self):
        self.do_contact_form_submission(self)
        self.assertEquals(len(mail.outbox), 1)
        message = mail.outbox[0]
        for recipient in Recipient.objects.all():
            if recipient.is_active:
                self.assertTrue(recipient.email in message.to)
            else:
                self.assertFalse(recipient.email in message.to)
