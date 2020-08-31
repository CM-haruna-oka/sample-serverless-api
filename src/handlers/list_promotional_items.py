import json


def handler(event, context):
    try:
        # TODO db connection
        result = [
            {'promotional_item_id': '0001',
                'promotional_item_name': 'サンプル品1', 'category': '販促物'},
            {'promotional_item_id': '0002',
                'promotional_item_name': 'サンプル品2', 'category': '販促物'}
        ]
    except Exception as e:
        print(e)
    return {
        'isBase64Encoded': False,
        'statusCode': 200,
        # ensure_ascii•••日本語文字化け対応
        'body': json.dumps(result, ensure_ascii=False)
    }
