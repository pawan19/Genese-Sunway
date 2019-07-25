import json
import boto3

tablename = "sunway"
CHARSET = 'UTF-8'

# resource initialization
sesclient=boto3.client('ses', region_name="eu-west-1")
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(tablename)

#configure SNS
sns = boto3.resource('sns')
topic = sns.Topic('arn:aws:sns:us-east-1:821354820623:sunway')
topic_arn = 'arn:aws:sns:us-east-1:821354820623:sunway'

def send_ses_email(name, address, description, email):
    fromAddress = "manoj@phuyal.co.uk"
    toAddress = ['pawan@genese.com.np']
    body = "Details from the form \n Name: " + name + "\n Address: " + address + "\n Description: " + description + "\n Email: " + email
    try:
        response = sesclient.send_email(
            Destination={
                'ToAddresses': toAddress,
            },
            Message={
                'Body': {
                    'Text': {
                        'Charset': CHARSET,
                        'Data': body,
                    },
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': "New Form Received",
                },
            },
            Source=fromAddress
        )
        print("Email Sent")
    except Exception as e:
        print(e)

def send_sns_notification(name, address, description, email):
    body = "Details from the form \n Name: " + name + "\n Address: " + address + "\n Description: " + description + "\n Email: " + email
    response = topic.publish(
        TopicArn=topic_arn,
        Message=body,
        Subject="New Form Received"
    )

def lambda_handler(event, context):
    # Get event records
    try:

        data=event['Records']
        for record in data:
            action=record['eventName']
            if action != "REMOVE":
                print("Event triggered due to " + action + " operation")
                name = record['dynamodb']['NewImage']['Name']['S']
                address = record['dynamodb']['NewImage']['Address']['S']
                description = record['dynamodb']['NewImage']['Description']['S']
                email = record['dynamodb']['NewImage']['Email']['S']
                send_sns_notification(name, address, description, email)

    except Exception as e:
        print(e)
        name = event['Name']
        email = event['Email']
        address = event['Address']
        description = event['Description']
        table.put_item(
            Item={
                'Name': name,
                'Address':address,
                'Description':description,
                'Email':email
            }
        )
        return "data added successfully"

            
