import json
import boto3
from boto3.dynamodb.types import TypeSerializer,TypeDeserializer

deserializer = TypeDeserializer()
serializer = TypeSerializer()
table_name = "userDetail"
ddb_client = boto3.client('dynamodb', region_name='ap-south-1')

def lambda_handler(event, context):
    # TODO implement
    print(event)
    pathParameters = event.get('pathParameters')#json.dumps()
    print(pathParameters)
    item =dict()
    item['contactNumber']=pathParameters.get('contactNumber')

    print (item)
    Item = ddb_client.get_item(
        TableName=table_name,
        Key={k: serializer.serialize(v) for k, v in item.items() if v and v != ""}
        ).get("Item")

    if Item:
        Item_value= {k: deserializer.deserialize(v) for k, v in Item.items()}
    else:
        Item_value={"error":"No Value Found"}
    print(Item_value)
    
    return {
        'statusCode': 200,
        'headers':{
			"Access-Control-Allow-Headers" : "Content-Type",
            "Access-Control-Allow-Origin" : "*", #Required for CORS support to work
            "Access-Control-Allow-Credentials" : True #// Required for cookies, authorization headers with HTTPS 
            
        },
        'body': json.dumps(Item_value)
    
    }
