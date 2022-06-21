from flask import Flask, request, jsonify
import json
import boto3, requests, sys, getopt
import sched, time

app = Flask(__name__)
app.config["DEBUG"] = True

##SQS##
sqs = boto3.client('sqs')
queue_url ='https://sqs.us-east-1.amazonaws.com/900076774107/PriorityBugQueue'

##Trello Connections##
trello_url = "https://api.trello.com/1/cards"
trello_token = "7614ef6bcfe62f06280173cd28c08848c85a773239ab8d1da62c92ad52771ba5"
trello_key = "64dd7fb11f2e28dac1d87ff746056da4"
trello_idList = "62ac7cd109f0525519df3c55"


s = sched.scheduler(time.time, time.sleep)

@app.route('/', methods=['POST'])
#recieve message from SQS Queue
def dequeue_message():       
    response = sqs.receive_message(
        QueueUrl=queue_url,
        AttributeNames=[
            'SentTimestamp',
              
        ],
        MaxNumberOfMessages=1,
        MessageAttributeNames=[
            'name',
            'priority'
        ],
        VisibilityTimeout=0,
        WaitTimeSeconds=0
    )

    messageAsDictionary = response
    if 'Messages' in messageAsDictionary:
        message = messageFormatter(response)    
        
    

def messageFormatter(response):
    message = response['Messages'][0]
    print(message)
    messageAtrributes = message['MessageAttributes']
    
    if messageAtrributes['priority']['StringValue'] == "high":
        Send_slack_message("Warning! New Bug! Priority: " + messageAtrributes['priority']['StringValue'] + ", Bug Message: " + messageAtrributes['name']['StringValue'])
    else: #messageAtrributes['priority']['StringValue'] == "low" or messageAtrributes['priority']['StringValue'] == "medium":
        create_trello_card("New Bug! Priority: " + messageAtrributes['priority']['StringValue'], messageAtrributes['name']['StringValue'])
    
        
    receipt_handle = message['ReceiptHandle']
    sqs.delete_message(
        QueueUrl=queue_url,
        ReceiptHandle=receipt_handle
    )
    

##Slack##
def Send_slack_message(Slack_message):
    payload = '{"text":"%s"}' % Slack_message
    response = requests.post('https://hooks.slack.com/services/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', data=payload)
    print(response.text)

##Trello##
def create_trello_card(card_name, card_desc):
    trello_Obj = {"key":trello_key,"token":trello_token,"idList":trello_idList, "name":card_name,"desc":card_desc} #jsonObj
    new_card = requests.post(trello_url,json=trello_Obj)
 

def main(sc):
    dequeue_message()
    s.enter(1, 1, main, (sc,))
s.enter(1, 1, main, (s,))
s.run()


if __name__ == '__main__':
    app.run(host="localhost", port=8000, debug=True)

    

