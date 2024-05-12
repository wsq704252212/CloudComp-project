import json
import boto3
from boto3.dynamodb.conditions import Key
    
def lambda_handler(event, context):
    email = event['requestContext']['authorizer']['claims']['email']

    body = json.loads(event['body'])
    print(body)

    interests = body['Interests']
    
    db = boto3.resource('dynamodb')
    table = db.Table("friend-user")
    user = {
            'Email': email,
            'Interests': interests
        }
    table.put_item(Item=user)
    putUser(user)

    return {
        'statusCode': 200,
        'body': json.dumps(user),
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        }
    }


def putUser(user):
    personalize_events = boto3.client('personalize-events')

    properties = {
        "Interests": '|'.join(user['Interests']),
    }
    properties_json = json.dumps(properties)

    personalize_events.put_users(
        datasetArn='arn:aws:personalize:us-east-1:590183760509:dataset/friend-dataset-group-v2/USERS',
        users=[
            {
                'userId': user['Email'],
                'properties': properties_json
            },
        ]
    )