import time

from list_views.utils import offline_support
from list_views.utils.item_constructor import ItemConstructor

if offline_support.is_offline():
    dynamodb = offline_support.dynamodb()
else:
    dynamodb = boto3.resource('dynamodb')


def update(event, context):
    data = json.loads(json.dumps(event))

    timestamp = int(time.time() * 1000)

    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

    item = ItemConstructor(data)
    item.itemize()

    result = table.update_item(
        Key=item.primary_key,
        ExpressionAttributeNames=item.attribute_names,
        UpdateExpression=item.update_expression,
        ReturnValues='UPDATED_NEW'
    )

    response = {
        "statusCode": 200,
        'body': json.dumps(result.get('Item', '{}'))
    }

    return response
