from rest_framework.test import APITestCase

from ..utilities.authentication import *


# Create your tests here.
class Authentication(APITestCase):
    def setUp(self):
        self.route = '/message/'
        self.key = "key"
        self.shared_key = "ss"
        self.parameters = {}
        self.x_signature = '578c990edf8572b98bfd1bf86bd236bb477837e9b2d188771973cf8fd798dd8c'

        Credentials.objects.create(key="key", shared_secret="ss")

    def test_valid_is_valid_x_signature(self):
        is_valid = is_valid_x_signature(
            self.x_signature, self.route, self.key, self.parameters
        )

        self.assertTrue(is_valid)

    def test_not_valid_is_valid_x_signature(self):
        x_signature = "another_signature"
        is_valid = is_valid_x_signature(
            x_signature, self.route, self.key, self.parameters
        )

        self.assertFalse(is_valid)

    def test_signature_generator(self):
        valid_signature = signature_generator(
            self.route, self.shared_key, self.parameters
        )

        self.assertEqual(
            valid_signature,
            '578c990edf8572b98bfd1bf86bd236bb477837e9b2d188771973cf8fd798dd8c'
        )

    def test_authenticate_non_existing_key(self):
        meta = {
            "HTTP_X_SIGNATURE": self.x_signature,
            "HTTP_X_ROUTE": self.route
        }
        data = self.parameters

        valid_authentication = authenticate(meta, data)
        self.assertFalse(valid_authentication)

    def test_authenticate_existing_key(self):
        meta = {
            "HTTP_X_KEY": self.key,
            "HTTP_X_SIGNATURE": self.x_signature,
            "HTTP_X_ROUTE": self.route
        }

        data = self.parameters

        valid_authentication = authenticate(meta, data)
        self.assertTrue(valid_authentication)

    def test_authenticate_not_valid_key(self):
        meta = {
            "HTTP_X_KEY": "Not valid",
            "HTTP_X_SIGNATURE": self.x_signature,
            "HTTP_X_ROUTE": self.route
        }

        data = self.parameters

        valid_authentication = authenticate(meta, data)
        self.assertFalse(valid_authentication)

    def test_authenticate_not_existing_route(self):
        meta = {
            "HTTP_X_KEY": self.key,
            "HTTP_X_SIGNATURE": self.x_signature,
        }

        data = self.parameters

        valid_authentication = authenticate(meta, data)
        self.assertFalse(valid_authentication)

    def test_authenticate_not_valid_route(self):
        meta = {
            "HTTP_X_KEY": self.key,
            "HTTP_X_SIGNATURE": self.x_signature,
            "HTTP_X_ROUTE": "/messages/other_route/"
        }

        data = self.parameters

        valid_authentication = authenticate(meta, data)
        self.assertFalse(valid_authentication)

    def test_authenticate_valid_route(self):
        meta = {
            "HTTP_X_KEY": self.key,
            "HTTP_X_SIGNATURE": self.x_signature,
            "HTTP_X_ROUTE": self.route
        }

        data = self.parameters

        valid_authentication = authenticate(meta, data)
        self.assertTrue(valid_authentication)

    def test_authenticate_not_existing_signature(self):
        meta = {
            "HTTP_X_KEY": self.key,
            "HTTP_X_ROUTE": self.route
            # "HTTP_X_SIGNATURE": self.x_signature,
        }

        data = self.parameters

        valid_authentication = authenticate(meta, data)
        self.assertFalse(valid_authentication)

    def test_authenticate_not_valid_signature(self):
        meta = {
            "HTTP_X_KEY": self.key,
            "HTTP_X_ROUTE": self.route,
            "HTTP_X_SIGNATURE": "Not valid",
        }

        data = self.parameters

        valid_authentication = authenticate(meta, data)
        self.assertFalse(valid_authentication)

    def test_authenticate_valid_signature(self):
        meta = {
            "HTTP_X_KEY": self.key,
            "HTTP_X_ROUTE": self.route,
            "HTTP_X_SIGNATURE": self.x_signature
        }

        data = self.parameters

        valid_authentication = authenticate(meta, data)
        self.assertTrue(valid_authentication)
