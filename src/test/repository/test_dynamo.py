import unittest
from unittest.mock import patch, MagicMock
from botocore.exceptions import ClientError
from repository.dynamo import DynamoRepository

class TestDynamoRepository(unittest.TestCase):

    @patch('boto3.resource')
    def setUp(self, mock_boto_resource):
        self.mock_table = MagicMock()
        mock_dynamodb = MagicMock()
        mock_dynamodb.Table.return_value = self.mock_table
        mock_boto_resource.return_value = mock_dynamodb

        self.repo = DynamoRepository(region_name='us-west-2', table_name='test_table')

    def test_read_item(self):
        self.mock_table.scan.return_value = {
            'Items': [{'user': 'test_user', 'video_name': 'test_video', 'date': '2023-01-01'}],
            'LastEvaluatedKey': None
        }

        result = self.repo.read_item(user='test_user', video_name='test_video', date='2023-01-01')
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['user'], 'test_user')
        self.assertEqual(result[0]['video_name'], 'test_video')
        self.assertEqual(result[0]['date'], '2023-01-01')

    @patch('loguru.logger.exception')
    def test_read_item_client_error(self, mock_logger_exception):
        self.mock_table.scan.side_effect = ClientError(
            error_response={'Error': {'Message': 'Test error'}},
            operation_name='Scan'
        )

        result = self.repo.read_item(user='test_user', video_name='test_video', date='2023-01-01')
        self.assertIsNone(result)
        mock_logger_exception.assert_called_once_with('Error reading item: Test error')

if __name__ == '__main__':
    unittest.main()