import json

from rest_framework import status
from rest_framework.test import APITestCase

from ..models import Credentials, Messages


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


class Message(APITestCase):
    def setUp(self):
        Credentials.objects.create(key="key", shared_secret="ss")
        Messages.objects.create(msg="test message 01", tag="tag")

    def test_create_with_valid_authentication(self):
        url = "/api/message/"
        data = {'msg': 'test message 01', 'tag': 'test'}
        http_x_key = "key"
        http_x_route = "/message/"
        http_x_signature = "8cb2f197587ed8366a4da71bb9f5f96357d448589e7c3cff4d67c86eea531bac"

        headers = {
            "HTTP_X_KEY": http_x_key,
            "HTTP_X_SIGNATURE": http_x_signature,
            "HTTP_X_ROUTE": http_x_route
        }

        response = self.client.post(
            url,
            json.dumps(data),
            content_type='application/json',
            **headers
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_with_invalid_authentication(self):
        url = "/api/message/"
        data = {'msg': 'test message 01', 'tag': 'test'}
        http_x_key = "NOT VALID"
        http_x_route = "/message/"
        http_x_signature = "8cb2f197587ed8366a4da71bb9f5f96357d448589e7c3cff4d67c86eea531bac"
        headers = {
            "HTTP_X_KEY": http_x_key,
            "HTTP_X_SIGNATURE": http_x_signature,
            "HTTP_X_ROUTE": http_x_route
        }

        response = self.client.post(
            url,
            json.dumps(data),
            content_type='application/json',
            **headers
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_read_message_with_valid_authentication(self):
        url = "/api/message/1/"
        http_x_key = "key"
        http_x_route = "/message/"
        http_x_signature = "578c990edf8572b98bfd1bf86bd236bb477837e9b2d188771973cf8fd798dd8c"
        headers = {
            "HTTP_X_KEY": http_x_key,
            "HTTP_X_SIGNATURE": http_x_signature,
            "HTTP_X_ROUTE": http_x_route
        }

        response = self.client.get(
            url,
            content_type='application/json',
            **headers
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_read_message_with_invalid_authentication(self):
        url = "/api/message/1/"
        http_x_key = "NOT VALID"
        http_x_route = "/message/"
        http_x_signature = "578c990edf8572b98bfd1bf86bd236bb477837e9b2d188771973cf8fd798dd8c"
        headers = {
            "HTTP_X_KEY": http_x_key,
            "HTTP_X_SIGNATURE": http_x_signature,
            "HTTP_X_ROUTE": http_x_route
        }

        response = self.client.get(
            url,
            content_type='application/json',
            **headers
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_read_messages_by_tag_with_valid_authentication(self):
        url = "/api/messages/test/"
        http_x_key = "key"
        http_x_route = "/message/"
        http_x_signature = "578c990edf8572b98bfd1bf86bd236bb477837e9b2d188771973cf8fd798dd8c"
        headers = {
            "HTTP_X_KEY": http_x_key,
            "HTTP_X_SIGNATURE": http_x_signature,
            "HTTP_X_ROUTE": http_x_route
        }

        response = self.client.get(
            url,
            content_type='application/json',
            **headers
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_read_messages_by_tag_with_invalid_authentication(self):
        url = "/api/messages/test/"
        http_x_key = "NOT VALID"
        http_x_route = "/message/"
        http_x_signature = "578c990edf8572b98bfd1bf86bd236bb477837e9b2d188771973cf8fd798dd8c"
        headers = {
            "HTTP_X_KEY": http_x_key,
            "HTTP_X_SIGNATURE": http_x_signature,
            "HTTP_X_ROUTE": http_x_route
        }

        response = self.client.get(
            url,
            content_type='application/json',
            **headers
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
