import boto3


def list_items(limit, last_key=None):
    dynamodb = boto3.resource('dynamodb')
    TABLE_NAME = 'Items'
    table = dynamodb.Table(TABLE_NAME)

    scan_kwargs = {
        'ConsistentRead': True,
        'Limit': limit
    }

    if last_key:
        scan_kwargs['ExclusiveStartKey'] = last_key

    response = table.scan(**scan_kwargs)
    result = {'items': response.get('Items', [])}

    return result
