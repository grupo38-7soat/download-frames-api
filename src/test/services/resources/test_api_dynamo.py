import unittest
from unittest.mock import patch, MagicMock
from flask import Flask
from flask_restx import Api
from services.resources.api_dynamo import dynamo_ns, ReadResource

class TestDynamoNamespace(unittest.TestCase):

    def setUp(self):
        self.app = Flask(__name__)
        self.api = Api(self.app)
        self.api.add_namespace(dynamo_ns)
        self.client = self.app.test_client()

    @patch('services.resources.api_dynamo.get_dynamo_repository')
    def test_read_resource_get(self, mock_get_dynamo_repository):
        mock_repo = MagicMock()
        mock_repo.read_item.return_value = {
            'user': 'test_user',
            'video_name': 'test_video',
            'date': '2023-01-01'
        }
        mock_get_dynamo_repository.return_value = mock_repo

        response = self.client.get('/consult-frames-history/find-ids', query_string={
            'user': 'test_user',
            'video_name': 'test_video',
            'date': '2023-01-01'
        })

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {
            'user': 'test_user',
            'video_name': 'test_video',
            'date': '2023-01-01'
        })

    @patch('services.resources.api_dynamo.get_dynamo_repository')
    def test_read_resource_get_item_not_found(self, mock_get_dynamo_repository):
        mock_repo = MagicMock()
        mock_repo.read_item.return_value = None
        mock_get_dynamo_repository.return_value = mock_repo

        response = self.client.get('/consult-frames-history/find-ids', query_string={
            'user': 'test_user',
            'video_name': 'test_video',
            'date': '2023-01-01'
        })

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, {'message': 'Item not found'})

if __name__ == '__main__':
    unittest.main()