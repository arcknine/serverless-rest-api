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

    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

    item_details = {
        'createdAt': timestamp,
        'updatedAt': timestamp
    }.update(event)

    constructor = ItemConstructor(item_details)
    item = constructor.itemize()

    table.put_item(Item=item.json)

    response = {
        'statusCode': 200,
        'body': json.dumps(item)
    }

    return response
