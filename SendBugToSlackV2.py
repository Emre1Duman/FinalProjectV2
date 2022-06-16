from flask import Flask, request, jsonify
import boto3, requests, sys, getopt
import sched, time

app = Flask(__name__)
app.config["DEBUG"] = True

sqs = boto3.client('sqs')
queue_url ='https://sqs.us-east-1.amazonaws.com/900076774107/PriorityBugQueue'

s = sched.scheduler(time.time, time.sleep)

@app.route('/', methods=['GET'])
def send_message(sc):
    
#recieve message from SQS Queue
    response = sqs.receive_message(
        QueueUrl=queue_url,
        AttributeNames=[
            'SentTimestamp'
        ],
        MaxNumberOfMessages=1,
        MessageAttributeNames=[
            'ALL'
        ],
        VisibilityTimeout=0,
        WaitTimeSeconds=0
    )

    messageAsDictionary = response
    if 'Messages' in messageAsDictionary:
        message = response['Messages'][0]
        receipt_handle = message['ReceiptHandle']

        sqs.delete_message(
            QueueUrl=queue_url,
            ReceiptHandle=receipt_handle
        )
        print('Received and deleted message: %s' % message)
        



    s.enter(1, 1, send_message, (sc,))
s.enter(1, 1, send_message, (s,))
s.run()
    








if __name__ == '__main__':
    app.run(host="localhost", port=8000, debug=True)

    

