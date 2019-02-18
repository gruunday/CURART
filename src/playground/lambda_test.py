import boto3
import json

client = boto3.client('lambda')

money_shot = {
             "Number1": 12,
             "Number2": 18
             }

response = client.invoke(
    FunctionName='testFunction',
    InvocationType='RequestResponse',
    LogType='Tail',
    Payload=json.dumps(money_shot)
    )

print(response['Payload'].read().decode('utf-8'))
