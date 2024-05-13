import json
import boto3
from boto3.dynamodb.conditions import Attr
from decimal import Decimal


class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return json.JSONEncoder.default(self, obj)


def lambda_handler(event, context):
    email = event['requestContext']['authorizer']['claims']['email']
    print(email)

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('friend-event')

    scan_kwargs = {
        'FilterExpression': Attr('Participants').contains(email)
    }
    response = table.scan(**scan_kwargs)
    print(response)

    events = response['Items']

    formatted_data = json.dumps({'events': events}, cls=JSONEncoder)
    print(formatted_data)

    return {
        'statusCode': 200,
        'body': formatted_data,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        }
    }
