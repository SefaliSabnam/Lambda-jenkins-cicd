import json

def lambda_handler(event, context):
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda! Deployed via Jenkins by Sefali!')
    }
