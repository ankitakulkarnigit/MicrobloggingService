import boto3
from boto3.dynamodb.conditions import Key, Attr
from datetime import datetime

def create_tables():
    # Get the service resource.
    dynamodb = boto3.resource('dynamodb')

    # Instantiate your dynamo client object
    client = boto3.client('dynamodb')

    # Get an array of table names associated with the current account and endpoint.
    tables = client.list_tables()

    if 'messageTable' in tables['TableNames']:
        table = dynamodb.Table('messageTable')
        table.delete()
    elif 'replyTable' in tables['TableNames']:
        table = dynamodb.Table('replyTable')
        table.delete()
    else:
        # Get the service resource.
        dynamodb = boto3.resource('dynamodb')

    # Create the DynamoDB table called messageTable
    print("----------Creating Message Table------------")
    table = dynamodb.create_table(
        TableName='messageTable',
        KeySchema=[
            {
            'AttributeName': 'messageId',
            'KeyType': 'HASH'
            },
            {
            'AttributeName': 'to',
            'KeyType': 'RANGE'
            }
        ],
        AttributeDefinitions=[
            {
            'AttributeName': 'messageId',
            'AttributeType': 'S'
            },
            {
            'AttributeName': 'to',
            'AttributeType': 'S'
            },
        ],
        ProvisionedThroughput={
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
        }
    )

    # Wait until the table exists.
    table.meta.client.get_waiter('table_exists').wait(TableName='messageTable')

    # Instantiate a table resource object without actually
    # creating a DynamoDB table. Note that the attributes of this table
    # are lazy-loaded: a request is not made nor are the attribute
    # values populated until the attributes
    table = dynamodb.Table('messageTable')

    currentTime = datetime.now()
    now = currentTime.strftime('%c')

    # creates a new item in the table
    table.put_item(
        Item={
            'messageId': '7d529dd4-548b-4258-aa8e-23e34dc8d43d',
            'to': 'Doe',
            'from': 'Jane',
            'message': 'I am Jane Doe',
            'timestamp': now,
            'quickReplies': '',
        }
    )   

    # batch writing
    with table.batch_writer() as batch:
        batch.put_item(
            Item={
                'messageId': '8d529dd4-548b-4258-aa8e-23e34dc8d45t',
                'to': 'Julie',
                'from': 'Jane',
                'message': 'I am enjoying at the beach',
                'timestamp': now,
                'quickReplies': '',
            }
        )
        batch.put_item(
            Item={
                'messageId': '9d529dd4-548b-4258-aa8e-23e34dc8d48i',
                'to': 'Rick',
                'from': 'Martin',
                'message': 'I am watching elections',
                'timestamp': now,
                'quickReplies': '',
            }

        )
        batch.put_item(
            Item={
                'messageId': '7d529dd4-548b-4258-aa8e-23e34dc8d467',
                'to': 'Rick',
                'from': 'Brian',
                'message': 'Hurray',
                'timestamp': now,
                'quickReplies': '',
            }   
        )
        batch.put_item(
        Item={
                'messageId': '9d529dd4-548b-4258-aa8e-23e34dc8d47h',
                'to': 'Rachael',
                'from': 'Malia',
                'message': 'Whats up',
                'timestamp': now,
                'quickReplies': '',
            }
        )   
    print("Table messageTable Initialized and Populated!")

    # Create the DynamoDB table called messageTable
    print("----------Creating Reply Table------------")
    table = dynamodb.create_table(
    TableName='replyTable',
    KeySchema=[
        {
        'AttributeName': 'replyId',
        'KeyType': 'HASH'
        },
        {
        'AttributeName': 'messageId',
        'KeyType': 'RANGE'
        }
    ],
    AttributeDefinitions=[
        {
        'AttributeName': 'replyId',
        'AttributeType': 'S'
        },
        {
        'AttributeName': 'messageId',
        'AttributeType': 'S'
        },
    ],
    ProvisionedThroughput={
    'ReadCapacityUnits': 5,
    'WriteCapacityUnits': 5
    }
    )

    # Wait until the table exists.
    table.meta.client.get_waiter('table_exists').wait(TableName='replyTable')

    # Instantiate a table resource object without actually
    # creating a DynamoDB table. Note that the attributes of this table
    # are lazy-loaded: a request is not made nor are the attribute
    # values populated until the attributes
    table = dynamodb.Table('replyTable')

    currentTime = datetime.now()
    now = currentTime.strftime('%c')
    # creates a new item in the table
    table.put_item(
        Item={
            'replyId': 'rd529dd4-548b-4258-aa8e-23e34dc8d43d',
            'messageId': '7d529dd4-548b-4258-aa8e-23e34dc8d43d',
            'message': 'I am Jane Doe',
            'timestamp': now,
            'quickReplies': '',
        }
    )
    # batch writing
    with table.batch_writer() as batch:
        batch.put_item(
            Item={
                'replyId': 'rd529dd4-548b-4258-aa8e-23e34dc8d45t',
                'messageId': '8d529dd4-548b-4258-aa8e-23e34dc8d45t',
                'message': 'I am enjoying at the beach',
                'timestamp': now,
                'quickReplies': '',
            }

        )
        batch.put_item(
            Item={
                'replyId': 'rd529dd4-548b-4258-aa8e-23e34dc8d48i',
                'messageId': '9d529dd4-548b-4258-aa8e-23e34dc8d48i',
                'message': 'I am watching elections',
                'timestamp': now,
                'quickReplies': '',
            }
        )
    print("Table replyTable Initialized and Populated!")

if __name__ == '__main__':
    create_tables()