import boto3
import json
import os
from boto3 import client
from botocore.errorfactory import ClientError

def get_error_response(code, message):
    return {
        "isBase64Encoded": "false",
        "statusCode": code,
        "body": json.dumps({"message": message})
    }


def get_success_response(body, code=200):
    return {
        "isBase64Encoded": "false",
        "statusCode": code,
        "body": json.dumps(body)
    }


def lambda_handler(event, context):
    client = boto3.client('s3')
    BUCKET = os.environ.get('BUCKET_STORAGE')
    try:
        response = client.get_object(Bucket=BUCKET, Key=event['pathParameters']['id'])
    except ClientError as ex:
        return get_error_response(400, "There was an error loading the To-Do objects.")

    body = json.loads(response['Body'].read().decode("utf-8"))
    return get_success_response([body])


if __name__ == "__main__":
    context = []
    event = {
      'resource': '/v1/todo/{id}',
      'path': '/v1/todo/bb73670b-d5e6-42af-9e5a-ce4797841d39',
      'httpMethod': 'GET',
      'headers': {
        'Accept': '*/*',
        'CloudFront-Forwarded-Proto': 'https',
        'CloudFront-Is-Desktop-Viewer': 'true',
        'CloudFront-Is-Mobile-Viewer': 'false',
        'CloudFront-Is-SmartTV-Viewer': 'false',
        'CloudFront-Is-Tablet-Viewer': 'false',
        'CloudFront-Viewer-ASN': '6805',
        'CloudFront-Viewer-Country': 'DE',
        'Host': 'b8xsmkn1f8.execute-api.eu-central-1.amazonaws.com',
        'User-Agent': 'curl/7.64.1',
        'Via': '2.0 f67cb1e6517f8abcedeb3b0734a257bc.cloudfront.net (CloudFront)',
        'X-Amz-Cf-Id': '3Mx_nptkewr23F710xMl0N8TWtSYj3mROyr5nRMdEAep_MftuQTvXQ==',
        'X-Amzn-Trace-Id': 'Root=1-632b5f39-2b5258a21962f304200d6476',
        'X-Forwarded-For': '78.54.98.19, 130.176.211.202',
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
          '6805'
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
          '2.0 f67cb1e6517f8abcedeb3b0734a257bc.cloudfront.net (CloudFront)'
        ],
        'X-Amz-Cf-Id': [
          '3Mx_nptkewr23F710xMl0N8TWtSYj3mROyr5nRMdEAep_MftuQTvXQ=='
        ],
        'X-Amzn-Trace-Id': [
          'Root=1-632b5f39-2b5258a21962f304200d6476'
        ],
        'X-Forwarded-For': [
          '78.54.98.19, 130.176.211.202'
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
      'pathParameters': {
        'id': 'bb73670b-d5e6-42af-9e5a-ce4797841d38'
      },
      'stageVariables': None,
      'requestContext': {
        'resourceId': 'qxs3mc',
        'resourcePath': '/v1/todo/{id}',
        'httpMethod': 'GET',
        'extendedRequestId': 'Y0vRFGbcFiAFTUA=',
        'requestTime': '21/Sep/2022:19:00:09 +0000',
        'path': '/dev/v1/todo/bb73670b-d5e6-42af-9e5a-ce4797841d39',
        'accountId': '643355622722',
        'protocol': 'HTTP/1.1',
        'stage': 'dev',
        'domainPrefix': 'b8xsmkn1f8',
        'requestTimeEpoch': 1663786809903,
        'requestId': '042f5dfd-6541-4de0-b4a5-918ece8c1698',
        'identity': {
          'cognitoIdentityPoolId': None,
          'accountId': None,
          'cognitoIdentityId': None,
          'caller': None,
          'sourceIp': '78.54.98.19',
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
