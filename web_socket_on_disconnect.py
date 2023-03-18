import json
import boto3
import sys, os


dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('conns')

def lambda_handler(event, context):
    print("*******")
    print(event)
    print("*******")

    
    result={"info":0}
    
    
    try:
        connectionId = event["requestContext"]["connectionId"]
        resp = table.delete_item(Key={'ID': str(connectionId)})
        
        return {'statusCode': 200,'body':json.dumps("gg")}
    except Exception as err:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        result["info"]="There was a server error 1: "+str(err)+ " type: "+str(exc_type)+ " in: "+ str(exc_tb.tb_lineno)
        return {
            "statusCode": 200  ,
            "body": json.dumps(result)
        }
        
