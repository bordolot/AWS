import pymysql
import hashlib
import json
import os
from base64 import b64encode


db_inst_endpoint = 'example.rds.amazonaws.com'
db_inst_username = 'admin'
db_inst_password = '1qaz2wsx'
database_name = 'projects'

pepper = 'somepepper'

def lambda_handler(event, context):
    auth="Deny"
    received_login=event["headers"]["login"]
    received_password=event["headers"]["password"]


    try:
        stored_pass_for_this_login=check_if_password_is_in_database(received_login)
        if stored_pass_for_this_login[0]:
            
            is_active=stored_pass_for_this_login[1][2]
            if is_active==True:
                stored_pass=bytes.fromhex(str(stored_pass_for_this_login[1][0])[2:-1])
                stored_salt=bytes.fromhex(str(stored_pass_for_this_login[1][1])[2:-1])
                if check_if_given_password_is_correct(received_password,stored_pass,stored_salt):
                    auth = "Allow"
    except Exception as err:
        auth = "Deny"


    # if received_password == "abc" and received_login=="123":
    #     auth = "Allow"
    # else:
    #     auth = "Deny"

    authResponse = { "principalId": received_login, "policyDocument": { "Version": "2012-10-17", 
    "Statement": [{"Action": "execute-api:Invoke", "Resource": [
# 		"example_aws_resource/test/POST/*",
    	"example_aws_resource/test/GET/firstgate"
    ],
    "Effect": auth}] }}
    return authResponse



def check_if_password_is_in_database(login):
    try:
        connection = pymysql.connect(host=db_inst_endpoint, user=db_inst_username, passwd=db_inst_password, db=database_name)
        cursor = connection.cursor()
        cursor.callproc('common_5_check_pass',[login])
        rows = cursor.fetchall()
        cursor.close()
        connection.close()
        if rows:
            return [True,[rows[0][0],rows[0][1],rows[0][2]] ]
        else:
            return [False]
    except Exception as err:
        return ["Errory wyszly z check_if_password_is_in_database", (f"Unexpected {err=}, {type(err)=}")]


def check_if_given_password_is_correct(given_pass,stored_pass,stored_salt):
    password_to_check_with_pepper=given_pass+pepper

    new_key = hashlib.pbkdf2_hmac(
        'sha256',
        password_to_check_with_pepper.encode('utf-8'), # Convert the password to bytes
        stored_salt,
        100000
    )
    if new_key == stored_pass:
        return True
    else:
        return False
        
def filter_input(input):
    for i in input:
        if not i in proper_input:
            print("Bad input!! --->" + i)
            return "Correct your input!"
    return "Login is OK and ready to be passed further to the database."





