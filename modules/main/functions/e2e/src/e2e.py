#!/usr/bin/python3.9

import os
import sys
import json
import boto3
import urllib3

http = urllib3.PoolManager()
base_url = os.environ.get('BASEURL')
headers = {'Content-Type': 'application/json'}
s3 = boto3.resource('s3')

def list_todos():
    url = f'{base_url}/v1/todo'
    resp = http.request('GET', url, headers=headers)
    json_object = json.loads(resp.data)

    return json_object


def get_todo(id):
    url = f'{base_url}/v1/todo/{id}'
    resp = http.request('GET', url, headers=headers)
    json_object = json.loads(resp.data)

    return json_object


def create_todo(data):
    body = json.dumps(data)
    url = f'{base_url}/v1/todo'
    resp = http.request('PUT', url, headers=headers, body=body)
    json_object = json.loads(resp.data)

    return json_object


def delete_todo(id):
    url = f'{base_url}/v1/todo/{id}'
    resp = http.request('DELETE', url, headers=headers)
    json_object = json.loads(resp.data)

    return json_object


def update_todo(id, data):
    body = json.dumps(data)
    url = f'{base_url}/v1/todo/{id}'
    resp = http.request('PUT', url, headers=headers, body=body)
    json_object = json.loads(resp.data)
    print(json_object)

    return json_object


def lambda_handler(event, context):
    print(f'List todos')
    todos = list_todos()
    print(todos)
    if len(todos) == 0:
        print(f'No todos found.')
        sys.exit(-1)

    print(f'Found: {len(todos)}')

    id = todos[0]['id']
    print(f'Get todo')
    todo = get_todo(id)
    if id != todo[0]['id']:
        print(f'Todo not found.')
        sys.exit(-1)

    print(f'Found: {todo[0]["id"]}')

    print(f'Create todo')
    response = create_todo({"id": "12345", "title": "title12345", "description": "description12345"})
    if not 'message' in response['message'] and response['message'] != 'To-Do object created successfully.':
        print(f'Error creating todo.')
        sys.exit(-1)

    todo = get_todo("12345")
    print(f'Created: {todo[0]["id"]}, {todo[0]["title"]}, {todo[0]["description"]}')

    response = update_todo("12345", {"id": "12345", "title": "title22222", "description": "description22222"})
    if not 'message' in response['message'] and response['message'] != 'To-Do object updated successfully.':
        print(f'Error updating todo.')
        sys.exit(-1)

    todo = get_todo("12345")
    print(f'Updated: {todo[0]["id"]}, {todo[0]["title"]}, {todo[0]["description"]}')

    print(f'Delete todo')
    delete_todo("12345")
    todos = list_todos()
    print(todos)

    #fields = {
    #    "file": ("data.csv", data_original),
    #}

    #resp = http.request('POST', url, headers=headers, fields=fields)

    # give process enough time to finish
    # time.sleep(5)
    #
    # temp_file = '/tmp/file.csv'
    # bucket_name = 'wow-shop-773914668429-dev-price-upload'
    # key = f'{country}/{identifier}_{country}_upload_{date}.csv'
    # print(key)
    # s3 = boto3.resource('s3')
    # try:
    #     s3.Bucket(bucket_name).download_file(key, temp_file)
    # except botocore.exceptions.ClientError as e:
    #     if e.response['Error']['Code'] == "404":
    #         print("The object does not exist.")
    #     else:
    #         raise
    #
    # with open(temp_file) as f:
    #     lines = f.readlines()
    #
    # data_processed = "".join(lines)
    #
    # if data_original != data_processed:
    #     print("Data does not match!")
    #
    # s3.Bucket(bucket_name).delete_objects(Delete={'Objects': [{'Key': key}]})


if __name__ == "__main__":
    event = {'Records': [{'eventVersion': '2.1', 'eventSource': 'aws:s3', 'awsRegion': 'eu-central-1', 'eventTime': '2022-05-11T06:04:04.089Z', 'eventName': 'ObjectCreated:Put', 'userIdentity': {'principalId': 'AWS:AROA3IMHIVWGQ6HFHN7GD:BackplaneAssumeRoleSession'}, 'requestParameters': {'sourceIPAddress': '3.70.195.235'}, 'responseElements': {'x-amz-request-id': '7Y3TVE2HJQ0VY71V', 'x-amz-id-2': 'SA/8WEiouRn892jWB778uxk2XbR0+dx6PKD3SsgiS6fJ6lDG54loPvPULd4OZ885URZ1I96zWkPooLUhGA1eoGHR6oCGHdhL'}, 's3': {'s3SchemaVersion': '1.0', 'configurationId': 'tf-s3-lambda-20220511060151935300000002', 'bucket': {'name': 'wow-shop-773914668429-price-upload', 'ownerIdentity': {'principalId': 'AISKW0Z79CHVY'}, 'arn': 'arn:aws:s3:::wow-shop-773914668429-price-upload'}, 'object': {'key': 'test/de/test.csv', 'size': 12, 'eTag': '6f5902ac237024bdd0c176cb93063dc4', 'sequencer': '00627B51D3F89A5AA0'}}}]}
    context = []
    lambda_handler(event, context)
