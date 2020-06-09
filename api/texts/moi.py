from rest_framework.test import APITestCase
from rest_framework import status
from ..models import Credentials


# Create your tests here.
# Using the standard RequestFactory API to create a form POST request
class CredentialsTests(APITestCase):
    def setUp(self):
        self.url = '/api/credential/'
        self.data = {"key": "key", "shared_secret": "ss"}

    def test_create_credentials(self):
        response = self.client.put(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_credential_request(self):
        response = self.client.put(self.url, {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class ExistingCredentialTest(APITestCase):
    def setUp(self):
        Credentials.objects.create(key="key", shared_secret="shared_secret")

    def test_existing_credentials(self):
        url = '/api/credential/'
        data = {"key": "key", "shared_secret": "ss"}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
