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

    try:
        event['pathParameters']
    except:
        params = event
    else:
        params = {}
        params['section_id'] = event['pathParameters']['id']
        params['application_id'] = '0'
        if event['queryStringParameters'] is not None:
            params['application_id'] = event['queryStringParameters']['application_id'] if 'application_id' in event['queryStringParameters'] else '0'
            params['listing_type'] = event['queryStringParameters']['listing_type'] if 'listing_type' in event['queryStringParameters'] else '0'
            params['listing_id'] = event['queryStringParameters']['listing_id'] if 'listing_id' in event['queryStringParameters'] else '0'

    data = json.loads(json.dumps(params))


    item = ItemConstructor(data)
    item.itemize()

    table.delete_item(Key=item.primary_key)

    response = {
        "statusCode": 200,
        "primaryKey": item.primary_key
    }

    return response
