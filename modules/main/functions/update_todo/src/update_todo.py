import base64
import boto3
import json
import os
from boto3 import client
from botocore.errorfactory import ClientError

client = boto3.client('s3')
BUCKET = os.environ.get('BUCKET_STORAGE')

def get_error_response(code, message):
    return {
        "isBase64Encoded": "false",
        "statusCode": code,
        "body": json.dumps({"message": message})
    }


def get_success_response(message, code=200):
    return {
        "isBase64Encoded": "false",
        "statusCode": code,
        "body": json.dumps({"message": message})
    }


def lambda_handler(event, context):
    item = ""
    try:
        item = json.loads(base64.b64decode(event["body"]))
    except Exception as ex:
        return get_error_response(400, "There was an error while creating a new To-Do object.")

    response = client.put_object(Bucket=BUCKET, Body=json.dumps(item), Key=item['id'])

    return get_success_response("To-Do object created successfully.")


if __name__ == "__main__":
    context = []
    event = {
      'resource': '/v1/todo',
      'path': '/v1/todo',
      'httpMethod': 'PUT',
      'headers': {
        'Accept': '*/*',
        'CloudFront-Forwarded-Proto': 'https',
        'CloudFront-Is-Desktop-Viewer': 'true',
        'CloudFront-Is-Mobile-Viewer': 'false',
        'CloudFront-Is-SmartTV-Viewer': 'false',
        'CloudFront-Is-Tablet-Viewer': 'false',
        'CloudFront-Viewer-ASN': '3320',
        'CloudFront-Viewer-Country': 'DE',
        'content-type': 'application/x-www-form-urlencoded',
        'Host': 'b8xsmkn1f8.execute-api.eu-central-1.amazonaws.com',
        'User-Agent': 'curl/7.64.1',
        'Via': '2.0 4dd80d99fd5d0f6baaaf5179cd921f72.cloudfront.net (CloudFront)',
        'X-Amz-Cf-Id': 'JQVs5csn014UhM5YMVzlwrD_WFKmTYxax6gOwyH6jOVJfQjhD2xjPA==',
        'X-Amzn-Trace-Id': 'Root=1-632b11c7-79bfe4ff40b4b73c07e4fc7c',
        'X-Forwarded-For': '80.187.102.57, 130.176.223.210',
        'X-Forwarded-Port': '443',
        'X-Forwarded-Proto': 'https'
      },
      'multiValueHeaders': {
        'Accept': [
          '*/*'
        ],
        'CloudFront-Forwarded-Proto': [
          'https'
        ],
        'CloudFront-Is-Desktop-Viewer': [
          'true'
        ],
        'CloudFront-Is-Mobile-Viewer': [
          'false'
        ],
        'CloudFront-Is-SmartTV-Viewer': [
          'false'
        ],
        'CloudFront-Is-Tablet-Viewer': [
          'false'
        ],
        'CloudFront-Viewer-ASN': [
          '3320'
        ],
        'CloudFront-Viewer-Country': [
          'DE'
        ],
        'content-type': [
          'application/x-www-form-urlencoded'
        ],
        'Host': [
          'b8xsmkn1f8.execute-api.eu-central-1.amazonaws.com'
        ],
        'User-Agent': [
          'curl/7.64.1'
        ],
        'Via': [
          '2.0 4dd80d99fd5d0f6baaaf5179cd921f72.cloudfront.net (CloudFront)'
        ],
        'X-Amz-Cf-Id': [
          'JQVs5csn014UhM5YMVzlwrD_WFKmTYxax6gOwyH6jOVJfQjhD2xjPA=='
        ],
        'X-Amzn-Trace-Id': [
          'Root=1-632b11c7-79bfe4ff40b4b73c07e4fc7c'
        ],
        'X-Forwarded-For': [
          '80.187.102.57, 130.176.223.210'
        ],
        'X-Forwarded-Port': [
          '443'
        ],
        'X-Forwarded-Proto': [
          'https'
        ]
      },
      'queryStringParameters': None,
      'multiValueQueryStringParameters': None,
      'pathParameters': None,
      'stageVariables': None,
      'requestContext': {
        'resourceId': 'cvuc4n',
        'resourcePath': '/v1/todo',
        'httpMethod': 'PUT',
        'extendedRequestId': 'Yz-3MGH1FiAFbyQ=',
        'requestTime': '21/Sep/2022:13:29:43 +0000',
        'path': '/dev/v1/todo',
        'accountId': '643355622722',
        'protocol': 'HTTP/1.1',
        'stage': 'dev',
        'domainPrefix': 'b8xsmkn1f8',
        'requestTimeEpoch': 1663766983407,
        'requestId': 'e9e778d9-57b5-4182-ae1b-2466b1d732ce',
        'identity': {
          'cognitoIdentityPoolId': None,
          'accountId': None,
          'cognitoIdentityId': None,
          'caller': None,
          'sourceIp': '80.187.102.57',
          'principalOrgId': None,
          'accessKey': None,
          'cognitoAuthenticationType': None,
          'cognitoAuthenticationProvider': None,
          'userArn': None,
          'userAgent': 'curl/7.64.1',
          'user': None
        },
        'domainName': 'b8xsmkn1f8.execute-api.eu-central-1.amazonaws.com',
        'apiId': 'b8xsmkn1f8'
      },
      'body': 'eyJpZCI6ICJiYjczNjcwYi1kNWU2LTQyYWYtOWU1YS1jZTQ3OTc4NDFkMzEiLCAidGl0bGUiOiAiQVBJIiwgImRlc2NyaXB0aW9uIjogIkNyZWF0ZSBhbiBBUEkgdGhhdCBtZWV0cyB0aGUgcmVxdWlyZW1lbnRzIn0=',
      'isBase64Encoded': True
    }


    data = lambda_handler(event, context)

    print(data)
