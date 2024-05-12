import json
import boto3

def lambda_handler(event, context):
    email = event['request']['userAttributes']['email']

    db = boto3.resource('dynamodb')
    table = db.Table("friend-user")
    user = {
            'Email': email,
            'Interests': []
        }
    table.put_item(Item=user)
    putUser(user)

    return event


def putUser(user):
    personalize_events = boto3.client('personalize-events')

    properties = {
        "Interests": 'NULL',
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
