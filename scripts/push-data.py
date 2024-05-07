import boto3
import json
import decimal

db = boto3.resource('dynamodb')

f = open('../data/user.json')
 
users = json.load(f)
table = db.Table("friend-user")
for u in users:
    table.put_item(Item=u)

f.close()


f = open('../data/event.json')
 
# returns JSON object as 
# a dictionary
events = json.load(f)
table = db.Table("friend-event")
for e in events:
    event = json.loads(json.dumps(e), parse_float=decimal.Decimal)
    table.put_item(Item=event)

f.close()