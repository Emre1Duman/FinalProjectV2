from flask import Flask, request, jsonify
import boto3, requests, sys, getopt
import sched, time

app = Flask(__name__)
app.config["DEBUG"] = True

sqs = boto3.client('sqs')
queue_url ='https://sqs.us-east-1.amazonaws.com/900076774107/PriorityBugQueue'

s = sched.scheduler(time.time, time.sleep)

@app.route('/', methods=['POST'])

def dequeue_message(): #recieve message from SQS Queue      
    response = sqs.receive_message(
        QueueUrl=queue_url,
        AttributeNames=[
            'SentTimestamp',  
        ],
        MaxNumberOfMessages=1,
        MessageAttributeNames=[
            'ALL'
        ],
        VisibilityTimeout=0,
        WaitTimeSeconds=0
    )
    print(response)

    messageAsDictionary = response
    if 'Messages' in messageAsDictionary:
        message = response['Messages'][0]
        print(message) 
        print(messageAsDictionary)
        receipt_handle = message['ReceiptHandle']

        sqs.delete_message(
            QueueUrl=queue_url,
            ReceiptHandle=receipt_handle
        )
        #Send_slack_message(message)
        #print(messageAsDictionary)
        #print('Received and deleted message: %s' % message)

def Send_slack_message(Slack_message):
    payload = '{"text":"%s"}' % Slack_message
    response = requests.post('', data=payload)
    print(response.text)
'''
def getting_message(argv, message):

    Slack_message = ' '

    try: opts, args = getopt.getopt(argv, "hm:", ["Slack_message"])
    except getopt.GetoptError:
        print('SendBugToSlackV2.py -m <Slack_message>')
        sys.exit(2)
    if len(opts) == 0:
        Slack_message = message
    for opt, arg in opts:
        if opt == '-h':
            print('SendBugToSlackV2.py -m <Slack_message>')
            sys.exit()
        elif opt in ("-m", "--Slack_message"):
            Slack_message = arg
    
    Send_slack_message(Slack_message)

'''
    


def main(sc):
    #Call method to dequeue
    #if dequeue_message != null, send to slack
    dequeue_message()
        
    
    #call method to send message to slack if there is a message

    s.enter(1, 1, main, (sc,))
s.enter(1, 1, main, (s,))
s.run()


if __name__ == '__main__':
    app.run(host="localhost", port=8000, debug=True)

    

