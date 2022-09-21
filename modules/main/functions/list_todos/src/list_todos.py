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
        "body": json.dumps({"error": message})
    }


def get_success_response(body, code=200):
  return {
    "isBase64Encoded": "false",
    "statusCode": code,
    "body": body
  }


def lambda_handler(event, context):
    items = []
    for key in client.list_objects(Bucket=BUCKET)['Contents']:
        response = client.get_object(Bucket=BUCKET, Key=key['Key'])
        try:
            item = json.loads(response['Body'].read().decode('utf-8'))
            items.append(item)
        except Exception as ex:
            return get_error_response(400, "There was an error loading the To-Do objects.")

    return get_success_response(json.dumps(items))


if __name__ == "__main__":
    context = []
    event = {
      'resource': '/v1/todo/{id}',
      'path': '/v1/todo/what',
      'httpMethod': 'GET',
      'headers': {
        'Accept': '*/*',
        'CloudFront-Forwarded-Proto': 'https',
        'CloudFront-Is-Desktop-Viewer': 'true',
        'CloudFront-Is-Mobile-Viewer': 'false',
        'CloudFront-Is-SmartTV-Viewer': 'false',
        'CloudFront-Is-Tablet-Viewer': 'false',
        'CloudFront-Viewer-ASN': '3320',
        'CloudFront-Viewer-Country': 'DE',
        'Host': 'b8xsmkn1f8.execute-api.eu-central-1.amazonaws.com',
        'User-Agent': 'curl/7.64.1',
        'Via': '2.0 4a0b7683a1d33d6d186965e831f2de96.cloudfront.net (CloudFront)',
        'X-Amz-Cf-Id': 'XvPERgssw4VfYYKKDOQp5rqIsUGrxn7v6fJR1XjsC6fGM1-Zb8Zg8A==',
        'X-Amzn-Trace-Id': 'Root=1-632b045c-4b45cd633b4fa1280fd9b7ef',
        'X-Forwarded-For': '80.187.102.57, 130.176.223.246',
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
        'Host': [
          'b8xsmkn1f8.execute-api.eu-central-1.amazonaws.com'
        ],
        'User-Agent': [
          'curl/7.64.1'
        ],
        'Via': [
          '2.0 4a0b7683a1d33d6d186965e831f2de96.cloudfront.net (CloudFront)'
        ],
        'X-Amz-Cf-Id': [
          'XvPERgssw4VfYYKKDOQp5rqIsUGrxn7v6fJR1XjsC6fGM1-Zb8Zg8A=='
        ],
        'X-Amzn-Trace-Id': [
          'Root=1-632b045c-4b45cd633b4fa1280fd9b7ef'
        ],
        'X-Forwarded-For': [
          '80.187.102.57, 130.176.223.246'
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
      'stageVariables': None,
      'requestContext': {
        'resourceId': 'qxs3mc',
        'resourcePath': '/v1/todo/{id}',
        'httpMethod': 'GET',
        'extendedRequestId': 'Yz2eaFYnliAFXLA=',
        'requestTime': '21/Sep/2022:12:32:28 +0000',
        'path': '/dev/v1/todo/what',
        'accountId': '643355622722',
        'protocol': 'HTTP/1.1',
        'stage': 'dev',
        'domainPrefix': 'b8xsmkn1f8',
        'requestTimeEpoch': 1663763548050,
        'requestId': '6fa24a7a-e1cb-4cf2-9ebb-68753419e8b9',
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
      'body': None,
      'isBase64Encoded': False
    }

    data = lambda_handler(event, context)

    print(data)
