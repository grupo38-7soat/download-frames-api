import unittest
from unittest.mock import patch, MagicMock
from flask import Flask
from flask_restx import Api
from services.resources.api_s3 import s3_ns

class TestS3Namespace(unittest.TestCase):

    def setUp(self):
        self.app = Flask(__name__)
        self.api = Api(self.app)
        self.api.add_namespace(s3_ns)
        self.client = self.app.test_client()

    @patch('services.resources.api_s3.s3_client')
    def test_read_resource_get_error(self, mock_s3_client):
        mock_s3_client.download_fileobj.side_effect = Exception('Download error')

        response = self.client.get('/download-frames/find-ids', query_string={
            'user': 'test_user',
            's3_file_name': 'test_file'
        })

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {'error': 'Download error'})

if __name__ == '__main__':
    unittest.main()