import boto3, time, json

TRACKING_ID = 'eb13d987-c0b3-46a4-bd38-f6fdd9e89dc6'

# For join
def putInteraction(uid, eventID):
    personalize_events = boto3.client('personalize-events')
    resp = personalize_events.put_events(
        trackingId = TRACKING_ID,
        userId= str(uid),
        sessionId = str(uid),
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
        datasetArn='arn:aws:personalize:us-east-1:590183760509:dataset/friend-dataset-group/USERS',
        users=[
            {
                'userId': str(user['Uid']),
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
        datasetArn='arn:aws:personalize:us-east-1:590183760509:dataset/friend-dataset-group/ITEMS',
        items=[
            {
                'itemId': str(event['Eid']),
                'properties': properties_json
            },
        ]
    )