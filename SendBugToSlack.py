from flask import Flask, request, jsonify
import boto3, requests, sys, getopt
import sched, time


app = Flask(__name__)
app.config["DEBUG"] = True

sqs = boto3.client('sqs')
queue_url ='https://sqs.us-east-1.amazonaws.com/900076774107/PriorityBugQueue'


s = sched.scheduler(time.time, time.sleep)

@app.route('/sendToSlack', methods=['POST'])
def send_message(sc):

    ##recieve message from SQS Queue##
    response = sqs.receive_message(
        QueueUrl=queue_url,
        AttributeNames=[
            'SentTimestamp'  
        ],
        MaxNumberOfMessages=1,
        MessageAttributeNames=[
            'All'
        ],
        VisibilityTimeout=0,
        WaitTimeSeconds=0
    )

    messageAsDictionary = response
    if 'Messages' in messageAsDictionary:   
        message = response['Messages'][0]
        receipt_handle = message['ReceiptHandle']
    # Delete received message from queue
        sqs.delete_message(
            QueueUrl=queue_url,
            ReceiptHandle=receipt_handle
            )
    #print('Received and deleted message: %s' % message)

##Send message to SLACK##
    def send_slack_message(Smessage):
        payload = '{"text":"%s"}' % Smessage
        response = requests.post('insert webhook link',
                                data=payload)
        print(response.text)

    def main(argv):

        Smessage = ' '

        try: opts, args = getopt.getopt(argv, "hm:", ["Smessage"])

        except getopt.GetoptError:
            print('SlackMessage.py -m <Smessage>')
            sys.exit(2)
       # if len(opts) == 0:
           # Smessage = message
        for opt, arg in opts:
            if opt == '-h':
                print('SlackMessage.py -m <Smessage')
                sys.exit()
            elif opt in ("-m", "--Smessage"):
                Smessage = arg

        send_slack_message(Smessage)

    if __name__ == "__main__":
        main(sys.argv[1:])
    
    s.enter(1, 1, send_message, (sc,))

s.enter(1, 1, send_message, (s,))
s.run()

if __name__ == '__main__': 
    app.run(host="localhost", port=8000, debug=True) 
   # host="localhost", port=8000, debug=True