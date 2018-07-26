import boto3
import logging
import json
import os
import uuid
import time

from list_views.utils import offline_support

if offline_support.is_offline():
    dynamodb = offline_support.dynamodb()
else:
    dynamodb = boto3.resource('dynamodb')


def create(event, context):
    data = json.loads(event['body'])

    if 'videos' not in data:
        logging.error('Validation failed')
        raise Exception("Couldn't create the video item")
        return

    timestamp = int(time.time() * 1000)

    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

    item = {
        'id': str(uuid.uuid1()),
        'name': data['name'],
        'country': data['country'],
        'app_id': data['app_id'],
        'videos': data['videos'],
        'createdAt': timestamp,
        'updatedAt': timestamp
    }

    table.put_item(Item=item)

    response = {
        'statusCode': 200,
        'body': json.dumps(item)
    }

    return response
