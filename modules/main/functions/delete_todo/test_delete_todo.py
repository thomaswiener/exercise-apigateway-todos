import unittest
import base64
import boto3
import json
import os
from unittest import mock
from moto import mock_s3
from moto.s3.responses import DEFAULT_REGION_NAME
from src.delete_todo import lambda_handler

class DeleteTodoTestCase(unittest.TestCase):
    """
    Tests delete_todo
    """

    @mock_s3
    @mock.patch.dict(os.environ, {"BUCKET_STORAGE": "testbucket"})
    def test_lambda_handler_delete_object_success(self):
        """
        Test Lambda Handler
        """

        bucket = "testbucket"
        body = {"test": "123"}

        s3 = boto3.client('s3', region_name=DEFAULT_REGION_NAME)
        s3.create_bucket(Bucket=bucket)
        s3.put_object(Bucket=bucket, Key='1111111111', Body=json.dumps(body))

        event = {
            'pathParameters': {
                'id': '1111111111'
            }
        }
        context = []
        result = lambda_handler(event, context)

        body_json = json.loads(result['body'])

        self.assertEqual(200, result['statusCode'])
        self.assertEqual('To-Do object deleted successfully.', body_json['message'])


    @mock_s3
    @mock.patch.dict(os.environ, {"BUCKET_STORAGE": "testbucket"})
    def test_lambda_handler_delete_object_invalid_id(self):
        """
        Test Lambda Handler
        """

        bucket = "testbucket"
        body = {"test": "123"}

        s3 = boto3.client('s3', region_name=DEFAULT_REGION_NAME)
        s3.create_bucket(Bucket=bucket)
        s3.put_object(Bucket=bucket, Key='1111111111', Body=json.dumps(body))

        event = {
            'pathParameters': {
                'id': '2222222222'
            }
        }
        context = []
        result = lambda_handler(event, context)

        body_json = json.loads(result['body'])

        self.assertEqual(400, result['statusCode'])
        self.assertEqual('There has been an error while deleting the To-Do object.', body_json['error'])


    @mock_s3
    @mock.patch.dict(os.environ, {"BUCKET_STORAGE": "testbucket"})
    def test_lambda_handler_delete_object_invalid_bucket(self):
        """
        Test Lambda Handler
        """

        bucket = "invalidbucket"
        body = {"id": "123"}

        s3 = boto3.client('s3', region_name=DEFAULT_REGION_NAME)
        s3.create_bucket(Bucket=bucket)

        event = {
            'pathParameters': {
                'id': '1111111111'
            }
        }
        context = []
        result = lambda_handler(event, context)

        body_json = json.loads(result['body'])

        self.assertEqual(400, result['statusCode'])
        self.assertEqual('There has been an error while deleting the To-Do object.', body_json['error'])



if __name__ == '__main__':
    unittest.main()

# python3 -m unittest test_get_todo.py