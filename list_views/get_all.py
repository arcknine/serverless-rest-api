import boto3
import os
import json

from boto3.dynamodb.conditions import Key

from list_views.utils.constants import *
from list_views.utils import offline_support
from list_views.utils.item_constructor import ItemConstructor

if offline_support.is_offline():
    dynamodb = offline_support.dynamodb()
else:
    dynamodb = boto3.resource('dynamodb')


def get_all(event, context):
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

    try:
        event['pathParameters']
    except:
        params = event
    else:
        params = {}
        params['section_id'] = event['pathParameters']['id']

    data = json.loads(json.dumps(params))

    item = ItemConstructor(data)
    item.itemize(True)

    result = table.query(
        KeyConditionExpression=Key(PARTITION_KEY).eq(item.partition_key)
    )

    response = {
        'statusCode': 200,
        'body': json.dumps(result['Items'])
    }

    return response
