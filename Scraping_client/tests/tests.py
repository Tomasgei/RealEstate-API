from django.test import TestCase, SimpleTestCase
from django.urls import reverse, resolve
from Scraping_client.scrapper import scrapper
from .. import views
# Create your tests here.

class TestUrls(SimpleTestCase):

    def project_url_resolved(self):
        url = reverse("project")
        self.assertEquals(resolve(url).func,views.ProjectsListAPIView )
    
    def property_all_url_resolved(self):
        url = reverse("property_all")
        self.assertEquals(resolve(url).func,views.ApartmentsListAPIView)

    def project_url_resolved(self):
        url = reverse("property_detail", args=[1])
        self.assertEquals(resolve(url).func,views.PropertyDetailAPIView )


