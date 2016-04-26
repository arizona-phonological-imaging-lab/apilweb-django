from django.test import TestCase
from django.core.urlresolvers import reverse
from UATracker.models import Image
from UATracker.textGridReader import readTextGrid
# Create your tests here.

class ViewTests(TestCase):
#     def test_index_view_with_no_questions(self):
#         """
#         If no questions exist, an appropriate message should be displayed.
#         """
#         response = self.client.get(reverse('uatracker:imageList',kwargs={'page':10}))
#         self.assertEqual(response.status_code, 200)
    def textGridReaderTester(self):
        images = Image.objects.all()[:10000]
        readTextGrid('/Users/Updates/git/apilweb-django/APILWeb/UATracker/example.TextGrid',images)
        randomImages = Image.objects.filter(word__spelling='cuip')
        print(len(randomImages))
        self.assertGreater(len(randomImages), 0)