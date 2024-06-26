import json
import boto3
from boto3.dynamodb.conditions import Key
from decimal import Decimal
import redis

campaign_arn = 'arn:aws:personalize:us-east-1:590183760509:campaign/friend-campaign-v1'

class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return json.JSONEncoder.default(self, obj)
    
def lambda_handler(event, context):
    #email = event['requestContext']['authorizer']['claims']['email']

    email = 'davismichael@example.org'
    personalize_runtime = boto3.client('personalize-runtime')
    get_recommendations_response = personalize_runtime.get_recommendations(
        campaignArn = campaign_arn,
        userId = email,
        numResults=40
    )

    event_list = get_recommendations_response['itemList']
    #print(event_list)
    events = getEventFromDB(event_list)
    print(json.dumps(events, cls=JSONEncoder))

    return {
        'statusCode': 200,
        'body': json.dumps(events, cls=JSONEncoder),
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        }
    }


def getEventFromDB(event_list):
    r = redis.StrictRedis(host='friend-redis-5qxyfp.serverless.use1.cache.amazonaws.com', port=6379)

    # get events in redis
    eventsInCache = []
    eventsIdInDB = []
    for event in event_list:
        e = r.hgetall(event['itemId'])
        if e is None: 
            eventsIdInDB.append(event['itemId'])
        else:
            eventsInCache.append(e)
    print(eventsIdInDB)
    print(eventsInCache)

    # search in DB if not in redis
    db = boto3.resource('dynamodb')
    table = db.Table("friend-event")
    eventsInDB = []
    for eventid in eventsIdInDB:
        id = int(eventid)
        resp = table.query(KeyConditionExpression=Key("Eid").eq(id))
        if len(resp["Items"]) != 0: 
            eventsInDB.append(resp["Items"][0])
    
    # put events to Cache
    for event in eventsIdInDB:
        id = str(event['Eid'])
        r.hset(id, mapping=event)
    
    return eventsInCache + eventsInDB