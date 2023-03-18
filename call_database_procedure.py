import pymysql
import sys, os

db_inst_endpoint = 'example.rds.amazonaws.com'
db_inst_username = 'admin'
db_inst_password = '1qaz2wsx'
database_name = 'example_database_name'


def lambda_handler(event, context):
  try:
    data = json.loads(event["body"])    
    job = do_job(data)
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps([job])
    }
  except Exception as err:
    result={
        "info":"",
    }
    exc_type, exc_obj, exc_tb = sys.exc_info()
    result["info"]="There was a server error: "+str(err)+ " type: "+str(exc_type)+ " in: "+ str(exc_tb.tb_lineno)

    return {
        "statusCode": 200,
        "body": json.dumps([result])
    }

      
def do_job(type,data):
  result={
      "info":"",
      "data":[]
  }
  connection=pymysql.connect(host=db_inst_endpoint, user=db_inst_username, passwd=db_inst_password, db=database_name_for_projects)
  cursor=connection.cursor()
  input=[]
  try:
    input=[data['example_input']]
    cursor.callproc("example_procedure",input)
    result["data"] = cursor.fetchall()
  except Exception as err:
      result["info"]="There was a database error"

      
      
