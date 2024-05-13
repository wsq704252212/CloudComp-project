import boto3
import json
import time
from decimal import Decimal


def lambda_handler(event, context):
    event_body = json.loads(event['body'])
    print(event_body)

    email = event['requestContext']['authorizer']['claims']['email']
    print(email)

    event_type = event_body['EventType']
    address = event_body['Location']
    # float to Decimal
    latitude = Decimal(str(event_body['Latitude']))
    longitude = Decimal(str(event_body['Longitude']))
    start_time = event_body['StartTime']
    number_of_people = event_body['NumberOfPeople']

    eid = int(time.time() * 1000)
    print(eid)

    event_item = {
        'Eid': eid,
        'Type': event_type,
        'Address': address,
        'Latitude': latitude,
        'Longitude': longitude,
        'StartTime': start_time,
        'NumberOfPeople': int(number_of_people),
        'Participants': [email]
    }
    print(event_item)
    response = put_event_into_db(event_item)
    print(response)
    return {
        'statusCode': 200,
        'body': json.dumps({'eventId': eid}),
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        }
    }


def put_event_into_db(event_item):
    db = boto3.resource('dynamodb')
    table = db.Table("friend-event")
    response = table.put_item(Item=event_item)
    return response
