import keys
import boto3
from botocore.config import Config
import json

my_config = Config(
    region_name = 'us-east-1',
    signature_version = 'v4',
    retries = {
        'max_attempts': 10,
        'mode': 'standard'
    }
)

brt = boto3.client(service_name='bedrock-runtime', config=my_config, 
                   aws_access_key_id=keys.aws_access_key_id,
                   aws_secret_access_key=keys.aws_secret_access_key
                   )

accept = 'application/json'
contentType = 'application/json'

body = json.dumps({
    "prompt": "\n\nHuman: explain black holes to 8th graders\n\nAssistant:",
    "max_gen_len": 300,
    "temperature": 0.1,
    "top_p": 0.9,
})

modelId = 'meta.llama3-8b-instruct-v1:0'
accept = 'application/json'
contentType = 'application/json'

response = brt.invoke_model(body=body, modelId=modelId, accept=accept, contentType=contentType)

response_body = json.loads(response.get('body').read())

# text
print(response_body.get('generation'))
