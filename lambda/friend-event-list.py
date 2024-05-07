import json
import boto3
from boto3.dynamodb.conditions import Key


campaign_arn = 'arn:aws:personalize:us-east-1:590183760509:campaign/friend-campaign'

def lambda_handler(event, context):
    uid = getUidByEmail('sw6195@nyu.edu')

    personalize_runtime = boto3.client('personalize-runtime')
    get_recommendations_response = personalize_runtime.get_recommendations(
        campaignArn = campaign_arn,
        userId = str(uid),
        numResults=40
    )

    event_list = get_recommendations_response['itemList']

    print(event_list)

    events = getEventFromDB(event_list)


    return {
        'statusCode': 200,
        'body': json.dumps(events)
    }

def getEventFromDB(event_list):
    db = boto3.resource('dynamodb')
    table = db.Table("friend-event")

    events = []
    for event in event_list:
        id = event['itemId']
        resp = table.query(KeyConditionExpression=Key("Eid").eq(id))
        if len(resp["Items"]) != 0: 
            events.append(resp["Items"][0])
    
    return events

def getUidByEmail(email):
    db = boto3.resource('dynamodb')
    table = db.Table("friend-user")

    resp = table.query(KeyConditionExpression=Key("Email").eq(email))
    uid = resp["Items"][0]['Uid']
    return uid

lambda_handler('', '')