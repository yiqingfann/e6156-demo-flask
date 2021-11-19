import re
import boto3
import json

subscription = {
    "^/users/?$": {"POST"},
    "^/users/[0-9]+/?$": {"PUT", "DELETE"}
}

sns_arn = "arn:aws:sns:us-east-2:066201190499:MyTopic"

def notify(request, response):
    path = request.path
    method = request.method
    for reg in subscription:
        if re.match(reg, path) and method in subscription[reg]:
            notification = {}
            try:
                request_data = request.get_json()
            except Exception as e:
                request_data = None

            notification["change"] = method
            if method != "DELETE":
                notification["new_state"] = request_data
            notification["params"] = path
            # notification["resp"] = response

            publish_it(notification)
            print("Published\n")

def publish_it(msg):

    # TODO: security problem!
    # need to put into environment variables later
    client = boto3.client('sns',
                          region_name='us-east-2',
                          aws_access_key_id="AKIAQ62PGABR2OIPZMVU",
                          aws_secret_access_key="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",
                          )
    txt_msg = json.dumps(msg)

    client.publish(TopicArn=sns_arn,
                   Message=json.dumps({'default': txt_msg}))
