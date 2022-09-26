import unittest
import base64
import boto3
import json
import os
from unittest import mock
from moto import mock_s3
from moto.s3.responses import DEFAULT_REGION_NAME
from src.update_todo import lambda_handler

class UpdateTodoTestCase(unittest.TestCase):
    """
    Tests update_todo
    """

    @mock_s3
    @mock.patch.dict(os.environ, {"BUCKET_STORAGE": "testbucket"})
    def test_lambda_handler_update_object_success(self):
        """
        Test Lambda Handler
        """

        bucket = "testbucket"
        body = {"id": "1111111111", "title": "topic-1", "description": "nothing"}

        base64_encoded = base64.b64encode(json.dumps(body).encode())

        s3 = boto3.client('s3', region_name=DEFAULT_REGION_NAME)
        s3.create_bucket(Bucket=bucket)
        s3.put_object(Bucket=bucket, Key='1111111111', Body=json.dumps(body))

        event = {
            'body': base64_encoded,
            'pathParameters': {
                'id': '1111111111'
            }
        }
        context = []
        result = lambda_handler(event, context)

        body_json = json.loads(result['body'])

        object = s3.get_object(Bucket=bucket, Key='1111111111')
        data = object['Body'].read()
        json_object = json.loads(data)

        self.assertEqual(200, result['statusCode'])
        self.assertEqual('To-Do object updated successfully.', body_json['message'])
        self.assertEqual('1111111111', json_object['id'])


    @mock_s3
    @mock.patch.dict(os.environ, {"BUCKET_STORAGE": "testbucket"})
    def test_lambda_handler_update_object_invalid_dict(self):
        """
        Test Lambda Handler
        """

        bucket = "testbucket"
        body = {"id": "1111111111", "invalid": "topic-1", "description": "nothing"}

        base64_encoded = base64.b64encode(json.dumps(body).encode())

        s3 = boto3.client('s3', region_name=DEFAULT_REGION_NAME)
        s3.create_bucket(Bucket=bucket)
        s3.put_object(Bucket=bucket, Key='1111111111', Body=json.dumps(body))

        event = {
            'body': base64_encoded,
            'pathParameters': {
                'id': '1111111111'
            }
        }
        context = []
        result = lambda_handler(event, context)

        body_json = json.loads(result['body'])

        self.assertEqual(400, result['statusCode'])
        self.assertEqual('There was an error while updating the To-Do object.', body_json['error'])


    @mock_s3
    @mock.patch.dict(os.environ, {"BUCKET_STORAGE": "testbucket"})
    def test_lambda_handler_create_object_invalid_base64(self):
        """
        Test Lambda Handler
        """

        bucket = "testbucket"

        base64_encoded = "whateverinvalidbase64"

        s3 = boto3.client('s3', region_name=DEFAULT_REGION_NAME)
        s3.create_bucket(Bucket=bucket)

        event = {
            'body': base64_encoded,
            'pathParameters': {
                'id': '1111111111'
            }
        }
        context = []
        result = lambda_handler(event, context)

        body_json = json.loads(result['body'])

        self.assertEqual(400, result['statusCode'])
        self.assertEqual('There was an error while updating the To-Do object.', body_json['error'])


    @mock_s3
    @mock.patch.dict(os.environ, {"BUCKET_STORAGE": "testbucket"})
    def test_lambda_handler_create_object_invalid_id(self):
        """
        Test Lambda Handler
        """

        bucket = "testbucket"

        base64_encoded = "whateverinvalidbase64"

        s3 = boto3.client('s3', region_name=DEFAULT_REGION_NAME)
        s3.create_bucket(Bucket=bucket)

        event = {
            'body': base64_encoded,
            'pathParameters': {
                'id': '2222222222'
            }
        }
        context = []
        result = lambda_handler(event, context)

        body_json = json.loads(result['body'])

        self.assertEqual(400, result['statusCode'])
        self.assertEqual('There was an error while updating the To-Do object.', body_json['error'])


    @mock_s3
    @mock.patch.dict(os.environ, {"BUCKET_STORAGE": "testbucket"})
    def test_lambda_handler_create_object_invalid_bucket(self):
        """
        Test Lambda Handler
        """

        bucket = "invalidbucket"
        body = {"id": "1111111111", "title": "topic-1", "description": "nothing"}

        base64_encoded = base64.b64encode(json.dumps(body).encode())

        s3 = boto3.client('s3', region_name=DEFAULT_REGION_NAME)
        s3.create_bucket(Bucket=bucket)

        event = {
            'body': base64_encoded,
            'pathParameters': {
                'id': '1111111111'
            }
        }
        context = []
        result = lambda_handler(event, context)

        body_json = json.loads(result['body'])

        self.assertEqual(400, result['statusCode'])
        self.assertEqual('There was an error while updating the To-Do object.', body_json['error'])



if __name__ == '__main__':
    unittest.main()

# python3 -m unittest test_get_todo.py