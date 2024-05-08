import boto3, time, json

TRACKING_ID = 'b6fcc596-8b3e-4c32-acb4-72eb4a78521a'

# For join
def putInteraction(email, eventID):
    personalize_events = boto3.client('personalize-events')
    resp = personalize_events.put_events(
        trackingId = TRACKING_ID,
        userId= email,
        sessionId = email,
        eventList = [{
            'itemId': str(eventID),
            'sentAt': int(time.time()),
            'eventType': 'EVENT_TYPE',
            }]
    )
    print(resp)


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

def putEvent(event):
    personalize_events = boto3.client('personalize-events')

    properties = {
        "Type": event['Type'],
    }
    properties_json = json.dumps(properties)

    personalize_events.put_items(
        datasetArn='arn:aws:personalize:us-east-1:590183760509:dataset/friend-dataset-group-v2/ITEMS',
        items=[
            {
                'itemId': str(event['Eid']),
                'properties': properties_json
            },
        ]
    )