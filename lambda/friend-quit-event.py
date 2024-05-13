import json
import boto3
from boto3.dynamodb.conditions import Key


def removeParticipant(event_id, email):
    db = boto3.resource('dynamodb')
    table = db.Table("friend-event")

    response = table.get_item(
        Key={
            'Eid': int(event_id)
        }
    )
    if 'Item' not in response:
        return {
            'statusCode': 404,
            'body': json.dumps('Event not found'),
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            }
        }

    print(response)
    participants = response['Item'].get('Participants', [])
    new_participants = [participant for participant in participants if participant != email]
    print(new_participants)
    update_response = table.update_item(
        Key={
            'Eid': int(event_id)
        },
        UpdateExpression='SET Participants = :val',
        ExpressionAttributeValues={
            ':val': new_participants
        },
        ReturnValues="UPDATED_NEW"
    )
    return update_response


def lambda_handler(event, context):
    print(event)

    email = event['requestContext']['authorizer']['claims']['email']
    body = json.loads(event['body'])
    event_id = body['eid']
    print(event_id)
    remove_response = removeParticipant(event_id, email)
    if 'Attributes' not in remove_response:
        return {
            'statusCode': 500,
            'body': json.dumps('Failed to remove participant'),
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            }
        }

    return {
        'statusCode': 200,
        'body': json.dumps('User removed from event successfully'),
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        }
    }
