import json
import boto3
from boto3.dynamodb.types import TypeSerializer

serializer = TypeSerializer()
table_name = "userDetail"
ddb_client = boto3.client('dynamodb', region_name='ap-south-1')

def lambda_handler(event, context):
    # TODO implement
    print(event)
    # print(type(event.get('body')))
    body = event#json.dumps()
    # print(body)
    item =dict()
    item['emailId']=body.get('emailID')
    item['Name']=body.get('firstName')
    item['SurName']=body.get('lastName')
    item['contactNumber']=body.get('contactNumber')
    item['datetime']=body.get('optTimestamp')
    
    ddb_client.put_item(
        TableName=table_name,
        Item={k: serializer.serialize(v) for k, v in item.items() if v and v != ""}

    )
    print('=====\nWritten item to dynamo table name %s\n=====' % table_name)
    
    return {
        'statusCode': 200,
        'headers':{
			"Access-Control-Allow-Headers" : "Content-Type",
            "Access-Control-Allow-Origin" : "*", #Required for CORS support to work
            "Access-Control-Allow-Credentials" : True #// Required for cookies, authorization headers with HTTPS 
            
        },
        'body': json.dumps('Sucessfully Entered')
    
    }
