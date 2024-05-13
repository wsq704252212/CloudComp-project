import json
import boto3
from boto3.dynamodb.conditions import Key
import time

TRACKING_ID = 'b6fcc596-8b3e-4c32-acb4-72eb4a78521a'


def lambda_handler(event, context):
    print(event)
    email = event['requestContext']['authorizer']['claims']['email']
    print(email)
    print(event['body'])
    body = json.loads(event['body'])
    event_id = body['eid']
    print(event_id)

    event_info = getEventFromDB(event_id)
    if not event_info:
        return {
            'statusCode': 404,
            'body': json.dumps('Event not found'),
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            }
        }

    updateParticipants(event_id, email)
    putInteraction(email, event_id)
    return {
        'statusCode': 200,
        'body': json.dumps('User added to event successfully'),
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        }
    }


def getEventFromDB(event_id):
    db = boto3.resource('dynamodb')
    table = db.Table("friend-event")
    id = int(event_id)
    resp = table.query(KeyConditionExpression=Key("Eid").eq(id))
    print(resp)
    return resp


def updateParticipants(event_id, email):
    db = boto3.resource('dynamodb')
    table = db.Table("friend-event")

    response = table.update_item(
        Key={
            'Eid': int(event_id)
        },
        UpdateExpression='SET Participants = list_append(Participants, :val)',
        ExpressionAttributeValues={
            ':val': [email]
        },
        ReturnValues="UPDATED_NEW"
    )
    return response


def putInteraction(email, eventID):
    personalize_events = boto3.client('personalize-events')
    resp = personalize_events.put_events(
        trackingId=TRACKING_ID,
        userId=email,
        sessionId=email,
        eventList=[{
            'itemId': str(eventID),
            'sentAt': int(time.time()),
            'eventType': 'EVENT_TYPE',
        }]
    )
    print(resp)
