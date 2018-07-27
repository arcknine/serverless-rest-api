import boto3
import os
import json

from list_views.utils import offline_support
from list_views.utils.item_constructor import ItemConstructor

if offline_support.is_offline():
    dynamodb = offline_support.dynamodb()
else:
    dynamodb = boto3.resource('dynamodb')


def delete(event, context):
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])
    data = json.loads(json.dumps(event))

    item = ItemConstructor(data)
    item.itemize()

    table.delete_item(Key=item.primary_key)

    response = {
        "statusCode": 200,
        "primaryKey": item.primary_key
    }

    return response
