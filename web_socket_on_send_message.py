import json
import urllib3
import boto3
import sys, os

client = boto3.client('apigatewaymanagementapi', endpoint_url="https://example.amazonaws.com/test")

client_dynamo = boto3.client('dynamodb')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('conns')

def lambda_handler(event, context):
    
    result={
        "info":0,
    }
    
    try:
        print(event)
        data = json.loads(event["body"])
        connectionId = event["requestContext"]["connectionId"]

        #############  TEST ################
        # connectionId = 1234
        # data = {"action":"sendMessage", "messageType":"to_welders"}
        #####################################


        responseMessage = ""
        if 'messageType' in data:
            type = data['messageType']
            if type == "define_yourself":
                responseMessage = "responding... hula hop "
                resp = table.update_item(
                    Key={'ID': str(connectionId)},
                    UpdateExpression="SET who= :s",
                    ExpressionAttributeValues={':s': "welder"},
                    ReturnValues="UPDATED_NEW")
            elif type == "to_application_in_windows":
                responseMessage = data['message']
                connectionIDs_1 = get_workers("admin")
                connectionIDs_1 = get_workers("welder")
                connectionIDs = connectionIDs_1
                send_back_message_to_all_interested(connectionIDs, responseMessage)
            else:
                responseMessage = "{'project_name':'no_project','drawing_name':'no_drawing','subject':'This subject doest exist'}"
                send_back_message_to_author(connectionId, responseMessage)
            
        else:
            responseMessage = "you are not defining type " + str(data)
            send_message_to_all(responseMessage)

        
        
        #Do something interesting... 
        
        #Form response and post back to connectionId
        
        return { "statusCode": 200 , "body": json.dumps("gg")}
    except Exception as err:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        result["info"]="There was a server error 1: "+str(err)+ " type: "+str(exc_type)+ " in: "+ str(exc_tb.tb_lineno)
        return {
            "statusCode": 200  ,
            "body": json.dumps(result)
        }
            
    
    
def query_status(asset_id, dynamodb, table):
    try:        
        response = table.query(
            ProjectionExpression="#asset_id, status_id" ,
            ExpressionAttributeNames={"#asset_id": "asset_id"},
            KeyConditionExpression=Key('asset_id').eq(asset_id)        
        )
        if response['Items']:
            return response['Items'][0]["status_id"]
    except:
        pass # if attribute does not exists, return None
    

def send_message_to_all(responseMessage):
    connectionIDs = table.scan()['Items']
    for element in connectionIDs:
        id = element['ID']
        response = client.post_to_connection(ConnectionId=id, Data=json.dumps(responseMessage).encode('utf-8'))
        
def send_back_message_to_author(id, responseMessage):
    response = client.post_to_connection(ConnectionId=id, Data=json.dumps(responseMessage).encode('utf-8'))

def send_back_message_to_all_interested(connectionIDs, message):
    for element in connectionIDs:
        id = element['ID']["S"]
        response = client.post_to_connection(ConnectionId=id, Data=json.dumps(message).encode('utf-8'))


def get_workers(worker_name):
    connectionIDs = client_dynamo.scan(
        ExpressionAttributeNames={
        '#AT': 'ID',
        },
        ExpressionAttributeValues={
            ':a': {
                'S': worker_name,
            },
        },
        FilterExpression='who = :a',
        ProjectionExpression='#AT',
        TableName='conns',
        )['Items']
    return connectionIDs
