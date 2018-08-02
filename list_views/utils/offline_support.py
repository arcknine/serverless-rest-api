import os
import boto3

def is_offline():
    return os.environ.get('IS_OFFLINE')

def dynamodb():
    endpoint_url = os.environ.get('ENDPOINT_URL', 'http://localhost:8000')

    return boto3.resource('dynamodb', region_name='localhost', endpoint_url=endpoint_url)
