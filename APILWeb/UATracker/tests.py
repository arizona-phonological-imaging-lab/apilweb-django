from django.test import TestCase
from django.core.urlresolvers import reverse

# Create your tests here.

class ViewTests(TestCase):
    def test_index_view_with_no_questions(self):
        """
        If no questions exist, an appropriate message should be displayed.
        """
        response = self.client.get(reverse('uatracker:imageList',kwargs={'page':10}))
        self.assertEqual(response.status_code, 200)
