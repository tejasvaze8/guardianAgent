import keys

import ldclient
from ldclient import Context
from ldclient.config import Config as LDConfig
from threading import Lock, Event

from flask import Flask
from flask import after_this_request, jsonify, request

import boto3
from botocore.config import Config
import json

ld_sdk_key = keys.ls_sdk_key

feature_flag_key = "use-model"

ldclient.set_config(LDConfig(ld_sdk_key))
client = ldclient.get()

if not ldclient.get().is_initialized():
    print("*** SDK failed to initialize. Please check your internet connection and SDK credential for any typo.")
    exit()

print("*** SDK successfully initialized")

context = \
    Context.builder('example-user-key').kind('user').name('Tejas').build()

flag_value = ldclient.get().variation(feature_flag_key, context, False)

print(flag_value)

bedrock_config = Config(
    region_name = 'us-east-1',
    signature_version = 'v4',
    retries = {
        'max_attempts': 10,
        'mode': 'standard'
    }
)

brt = boto3.client(service_name='bedrock-runtime', config=bedrock_config, 
                   aws_access_key_id=keys.aws_access_key_id,
                   aws_secret_access_key=keys.aws_secret_access_key
                   )

accept = 'application/json'
contentType = 'application/json'


modelId = 'meta.llama3-8b-instruct-v1:0'
accept = 'application/json'
contentType = 'application/json'


# text
# print(response_body.get('generation'))

app = Flask(__name__)

@app.route("/")
def hello_world():
    context = \
        Context.builder('example-user-key').kind('user').name('Tejas').build()

    flag_value = ldclient.get().variation(feature_flag_key, context, False)
    show_evaluation_result(feature_flag_key, flag_value)

    change_listener = FlagValueChangeListener()
    listener = ldclient.get().flag_tracker \
        .add_flag_value_change_listener(feature_flag_key, context, change_listener.flag_value_change_listener)

    try:
        Event().wait()
    except KeyboardInterrupt:
        pass

    return "<p>Hello, World!</p>"


query = "hello"

@app.route("/generate", methods=['GET'])
def generate():
    @after_this_request
    def add_header(response):
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response
    
    body = json.dumps({
        "prompt": "Given this context, give me relevant information: " 
                    + query,
        "max_gen_len": 30,
        "temperature": 0.1,
        "top_p": 0.9,
    })

    response = brt.invoke_model(body=body, modelId=modelId, accept=accept, contentType=contentType)

    response_body = json.loads(response.get('body').read())

    flag_value = ldclient.get().variation(feature_flag_key, context, False)
    print(flag_value)
    return jsonify(response_body)

@app.route("/guardian", methods=['GET', 'POST'])
def guardian(): 
    global query
    data = request.data.decode('utf-8')
    print(data)
    print(json.loads(data))
    data = json.loads(data)
    query = data['query']
    return jsonify({ "query": query })

visited_urls = []

@app.route("/embedding", methods=['POST'])
def embedding():
    data = request.data.decode('utf-8')
    print(data)
    print(json.loads(data))
    data = json.loads(data)
    url = data['url']
    visited_urls.append(url)
    return jsonify({ "url": url })
