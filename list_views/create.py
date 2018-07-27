import boto3
import logging
import json
import os
import uuid
import time

from list_views.utils.item_constructor import ItemConstructor
from list_views.utils import offline_support

if offline_support.is_offline():
    dynamodb = offline_support.dynamodb()
else:
    dynamodb = boto3.resource('dynamodb')

def create(event, context):
    timestamp = int(time.time() * 1000)
    data = json.loads(json.dumps(event))

    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

    item_details = {
        'createdAt': str(timestamp),
        'updatedAt': str(timestamp)
    }

    item_details.update(data)

    item = ItemConstructor(item_details)
    item.itemize()

    table.put_item(Item=item.json_details)

    response = {
        'statusCode': 200,
        'body': item.json_details
    }

    return response
