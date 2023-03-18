import json
import boto3
import sys, os

table_name = 'conns'
dynamodb_client = boto3.client('dynamodb')

# # put item into db
# dynamodb_client.put_item(TableName = table_name, Item= item_scarface)
# # get item
# resp = dynamodb_client.get_item(TableName = table_name, Key = item_get)

def lambda_handler(event, context):
    print("*******")
    print(event)
    print("*******")
    result={"info":0}
    received_who=event["headers"]["who"]
    # received_who="foreman"
    
    try:
        connectionId = event["requestContext"]["connectionId"]
        # connectionId = 2222
        db_item = {
            'ID':{'S': str(connectionId)},
            'who':{'S': received_who}
        }
        
        dynamodb_client.put_item(TableName = table_name, Item = db_item)
        
        return {'statusCode': 200,}
    except Exception as err:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        result["info"]="There was a server error 1: "+str(err)+ " type: "+str(exc_type)+ " in: "+ str(exc_tb.tb_lineno)
        return {
            "statusCode": 200  ,
            "body": json.dumps(result)
        }
