import unittest
from unittest.mock import patch, MagicMock
from flask_testing import TestCase
from flask_restx import Api
from services.expose_api_service import app, ApiService


class TestApiService(TestCase):
    def create_app(self):
        return app

    @patch("services.expose_api_service.dynamo_ns")
    @patch("services.expose_api_service.s3_ns")
    def test_api_initialization(self, mock_s3_ns, mock_dynamo_ns):
        service = ApiService()
        self.assertIsNotNone(service.api)
        self.assertEqual(service.api.version, '1.0')
        self.assertEqual(service.api.title, 'API')
        self.assertEqual(service.api.description, 'Descricao da API')


if __name__ == "__main__":
    unittest.main()
