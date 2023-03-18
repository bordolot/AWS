import boto3

s3 = boto3.client('s3')
bucket='example_bucket_name'


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
  try:
    object_name = 'example_object_name'
    link = generate_link_to_download(object_name)
    result["data"] = [link]
  except Exception as err:
    result["info"]="There was a s3 error"

def generate_link_to_download(object_name):
  link = s3.generate_presigned_url(
          'get_object',
          Params={
              'Bucket':bucket,
              'Key':object_name
          },
          ExpiresIn=60
          )
  return link
      
