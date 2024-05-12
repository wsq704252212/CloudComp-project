import json
import boto3
from boto3.dynamodb.conditions import Key

def lambda_handler(event, context):
    email = event['requestContext']['authorizer']['claims']['email']
     
    db = boto3.resource('dynamodb')
    table = db.Table("friend-user")
    resp = table.query(KeyConditionExpression=Key("Email").eq(email))
    if len(resp["Items"]) != 0: 
            user = resp["Items"][0]
    else:
          return {
                'statusCode': 404,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                }
          }
    
    print(json.dumps(user))
    return {
        'statusCode': 200,
        'body': json.dumps(user),
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        }
    }