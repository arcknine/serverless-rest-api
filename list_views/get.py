import boto3
import os
import json

from list_views.utils import offline_support

PARTITION_KEY = 'appId_sectionId'
SORT_KEY = 'listingType_listingId'

if offline_support.is_offline():
    dynamodb = offline_support.dynamodb()
else:
    dynamodb = boto3.resource('dynamodb')

def get(event, context):
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

    result = table.get_item(
        Key={
            PARTITION_KEY: __build_partition_key(event),
            SORT_KEY: __build_sort_key(event)
        }
    )

    item = result.get('Item', '{}')

    response = {
        'statusCode': 200,
        'body': json.dumps(item)
    }

    return response

def __build_partition_key(event):
    return ','.join([ event['application_id'], event['section_id'] ])

def __build_sort_key(event):
    return ','.join([ event['listing_type'], event['listing_id'] ])
