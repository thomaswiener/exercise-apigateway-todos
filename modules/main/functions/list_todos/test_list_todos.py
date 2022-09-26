import unittest
import boto3
import json
import os
from unittest import mock
from moto import mock_s3
from moto.s3.responses import DEFAULT_REGION_NAME
from src.list_todos import lambda_handler

class ListTodosTestCase(unittest.TestCase):
    """
    Tests list_todo
    """

    @mock_s3
    @mock.patch.dict(os.environ, {"BUCKET_STORAGE": "testbucket"})
    def test_lambda_handler_list_object_success_single_result(self):
        """
        Test Lambda Handler
        """

        bucket = "testbucket"
        body = {"test": "123"}

        s3 = boto3.client('s3', region_name=DEFAULT_REGION_NAME)
        s3.create_bucket(Bucket=bucket)
        s3.put_object(Bucket=bucket, Key='1111111111', Body=json.dumps(body))

        event = {}
        context = []
        result = lambda_handler(event, context)
        body_json = json.loads(result['body'])

        self.assertEqual(200, result['statusCode'])
        self.assertEqual(1, len(body_json))


    @mock_s3
    @mock.patch.dict(os.environ, {"BUCKET_STORAGE": "testbucket"})
    def test_lambda_handler_list_object_success_empty_result(self):
        """
        Test Lambda Handler
        """

        bucket = "testbucket"

        s3 = boto3.client('s3', region_name=DEFAULT_REGION_NAME)
        s3.create_bucket(Bucket=bucket)

        event = {}
        context = []
        result = lambda_handler(event, context)

        body_json = json.loads(result['body'])
        self.assertEqual(200, result['statusCode'])
        self.assertEqual(0, len(body_json))


    @mock_s3
    @mock.patch.dict(os.environ, {"BUCKET_STORAGE": "testbucket"})
    def test_lambda_handler_list_object_missing_bucket(self):
        """
        Test Lambda Handler
        """

        bucket = "missingbucket"

        s3 = boto3.client('s3', region_name=DEFAULT_REGION_NAME)
        s3.create_bucket(Bucket=bucket)

        event = {}
        context = []
        result = lambda_handler(event, context)

        body_json = json.loads(result['body'])
        self.assertEqual(400, result['statusCode'])


if __name__ == '__main__':
    unittest.main()

# python3 -m unittest test_get_todo.py