import requests
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

from bs4 import BeautifulSoup

ld_sdk_key = keys.ls_sdk_key

feature_flag_key = "use-model"
agent_key = "agent-type"

ldclient.set_config(LDConfig(ld_sdk_key))
client = ldclient.get()

if not ldclient.get().is_initialized():
    print("*** SDK failed to initialize. Please check your internet connection and SDK credential for any typo.")
    exit()

print("*** SDK successfully initialized")

context = \
    Context.builder('example-user-key').kind('user').key('student').build()

agent_context = ldclient.get().variation(agent_key, context, False)

print(agent_context)

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


accept = 'application/json'
contentType = 'application/json'

llama_id = 'meta.llama2-13b-chat-v1'
claude_id = 'anthropic.claude-3-haiku-20240307-v1:0'
mistral_id = 'mistral.mistral-large-2402-v1:0'
modelId = llama_id

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
    
    agent_context = ldclient.get().variation(agent_key, context, False)
    print(agent_context)

    all_text = ""
    for text in url_text:
        all_text += text[-700:] + "\n"

    prompt = agent_context + all_text + " " + "Here is the current working text: " + query

    print(prompt)

    body = json.dumps({
        "prompt": prompt,
        "max_gen_len": 400,
        "temperature": 0.1,
        "top_p": 0.9,
    })

    response = brt.invoke_model(body=body, modelId=modelId, accept=accept, contentType=contentType)

    response_body = json.loads(response.get('body').read())

    print(response_body)
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
url_text = []
convex_url = "http://172.20.10.8:5002/store_text"

@app.route("/embedding", methods=['POST'])
def embedding():
    global url_text
    data = request.data.decode('utf-8')
    print(data)
    print(json.loads(data))
    data = json.loads(data)
    url = data['url']
    if url not in visited_urls:
        visited_urls.append(url)
    print(visited_urls)

    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    paragraphs = soup.find_all('p')
    article_content = "\n".join([p.text.strip() for p in paragraphs])
    url_text.append(article_content)

    data = {
        'text': article_content
    }

    json_data = json.dumps(data)
    try:
        response = requests.post(convex_url, json=json_data, 
                                 headers={'Content-Type': 'application/json'})
        print(response)
    except Exception as e:
        print(e)

    print(url_text)
    return jsonify({ "url": url })
