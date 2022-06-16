from queue import PriorityQueue
from flask import Flask, request, jsonify
import boto3

app = Flask(__name__)
app.config["DEBUG"] = True

sqs = boto3.client('sqs')

queue_url = 'https://sqs.us-east-1.amazonaws.com/900076774107/PriorityBugQueue'
#queue_url = 'https://sqs.us-east-1.amazonaws.com/900076774107/NormalBugQueue'



@app.route('/submitBug', methods=['POST'])
def home():
    priority=request.args.get('priority')
    name=request.args.get('name')
    return sendtoqueue(name, priority)

def sendtoqueue(nameForMessage, priorityForMessage):

    response = sqs.send_message(
            QueueUrl=queue_url,
            DelaySeconds=10,
            MessageAttributes={
                'name': {
                    'DataType': 'String',
                    'StringValue': nameForMessage
                },
                'priority': {
                    'DataType': 'String',
                    'StringValue': priorityForMessage
                }
            },
            MessageBody=(
                'New bugs found!'
            )
    )
    return("Stored in queue with message ID "+response['MessageId'])

  

#if 'Priority' == 'high':





if __name__ == '__main__': 
    app.run() 