import os
import boto3

def is_offline():
    return os.environ.get('IS_OFFLINE')

def dynamodb():
    return boto3.resource('dynamodb', region_name='localhost', endpoint_url='http://localhost:8000')
