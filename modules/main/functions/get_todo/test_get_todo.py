import unittest
import boto3
import json
import os
from unittest import mock
from moto import mock_s3
from moto.s3.responses import DEFAULT_REGION_NAME
from src.get_todo import lambda_handler

class GetTodoTestCase(unittest.TestCase):
    """
    Tests get_todo
    """

    @mock_s3
    @mock.patch.dict(os.environ, {"BUCKET_STORAGE": "testbucket"})
    def test_lambda_handler_get_object_success(self):
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
        self.assertEqual(body, body_json[0])


    @mock_s3
    @mock.patch.dict(os.environ, {"BUCKET_STORAGE": "testbucket"})
    def test_lambda_handler_get_object_failure(self):
        """
        Test Lambda Handler
        """

        bucket = "testbucket"
        body = {"test": "123"}

        s3 = boto3.client('s3', region_name=DEFAULT_REGION_NAME)
        s3.create_bucket(Bucket=bucket)
        s3.put_object(Bucket=bucket, Key='9999999999', Body=json.dumps(body))

        event = {
            'pathParameters': {
                'id': '1111111111'
            }
        }
        context = []
        result = lambda_handler(event, context)
        body_json = json.loads(result['body'])

        self.assertEqual(400, result['statusCode'])
        self.assertEqual('There was an error loading the To-Do objects.', body_json['message'])


    @mock_s3
    @mock.patch.dict(os.environ, {"BUCKET_STORAGE": "testbucket"})
    def test_lambda_handler_get_object_missing_bucket(self):
        """
        Test Lambda Handler
        """

        bucket = "otherbucket"
        body = {"test": "123"}

        s3 = boto3.client('s3', region_name=DEFAULT_REGION_NAME)
        s3.create_bucket(Bucket=bucket)
        s3.put_object(Bucket=bucket, Key='9999999999', Body=json.dumps(body))

        event = {
            'pathParameters': {
                'id': '1111111111'
            }
        }
        context = []
        result = lambda_handler(event, context)
        body_json = json.loads(result['body'])

        self.assertEqual(400, result['statusCode'])
        self.assertEqual('There was an error loading the To-Do objects.', body_json['message'])


if __name__ == '__main__':
    unittest.main()

# python3 -m unittest test_get_todo.py