import sqlite3, click, boto3, uuid, os
from flask import Flask, request, jsonify, g
from flask.cli import with_appcontext
from boto3.dynamodb.conditions import Key, Attr
from datetime import datetime
from flask_dynamo import Dynamo
from db_init import create_tables

TableName: any
KeySchema: any
AttributeDefinitions: any
ProvisionedThroughput: any

dynamodb = boto3.resource('dynamodb')

######################
# API USAGE
# Web server route for this API: localhost:5200
# --------------------
# Sends a direct message to a user: Send a POST request to route of sendDirectMessage() fn
# Example request:
#   curl -i -X POST -H 'Content-Type:application/json' -d '{"to":"ankita", "from":"aditi", "message":"How are you?"}' http://localhost:5200/sendMessage;
# --------------------
# Replies to a direct message: Send a GET request to route of replyToDirectMessage() fn
# Example request:
#   curl -i -X POST -H 'Content-Type:application/json' -d '{"messageId":"00bf7f51-4636-4008-80fe-f65d925c17ab", "reply":"I am fine"}' http://localhost:5200/reply;
# --------------------
# Lists a user's DMs: Send a POST request to route of listDirectMessagesFor() fn
# Example request:
#   curl -i -X GET -H 'Content-Type:application/json' -d '{"username":"Rick"}' http://localhost:5200/list/messages;
# --------------------
# Lists the replies to a DM: Send a DELETE request to route of listRepliesTo() fn
# Example request:
#   curl -i -X GET -H 'Content-Type:application/json' -d '{"messageId":"9d529dd4-548b-4258-aa8e-23e34dc8d48i"}' http://localhost:5200/list/replies;
# --------------------

######################
# SQLite3 Database
# db_name: UserPost.db

# table1: users
# username
# email
# pass

# table2: Followers
# username
# usernamefollowing

# table3: DM
# to
# from
# timestamp
# text
# quickReplies

# DynamoDB 
# table1: messageTable
# messageId
# to
# from
# message
# timestamp
# quickReplies

# table2: replyTable
# replyId
# messageId        
# message
# timestamp
# quickReplies

# config variables
app = Flask(__name__)
dynamodb = boto3.resource('dynamodb')
DATABASE = 'UserPost.db'

#dynamo = Dynamo(app)

'''
def create_app():
    app.config['DYNAMO_TABLES'] : [
    {
         TableName:'messageTable',
         KeySchema:[dict(AttributeName='messageId', KeyType='HASH'),dict(AttributeName='to', KeyType='RANGE')],
         AttributeDefinitions:[dict(AttributeName='messageId', AttributeType='S'),dict(AttributeName='to', AttributeType='S')],
         ProvisionedThroughput:dict(ReadCapacityUnits=5, WriteCapacityUnits=5)
    }, {
         TableName:'replyTable',
         KeySchema:[dict(AttributeName='replyId', KeyType='HASH'),dict(AttributeName='messageId', KeyType='RANGE')],
         AttributeDefinitions:[dict(AttributeName='replyId', AttributeType='S'),dict(AttributeName='messageId', AttributeType='S')],
         ProvisionedThroughput:dict(ReadCapacityUnits=5, WriteCapacityUnits=5)
    }
    ]
    dynamo = Dynamo()
    dynamo.init_app(app)
    return app
'''

# helper function to generate a response with status code and message
def get_response(status_code, message):
    return {"status_code": str(status_code), "message": str(message)}

# get db from flask g namespace
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

# function to execute a single query at once
def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

# helper function to update table for dm
def storeSentDm(messageId, receiver, sender, message, quickReplies):
    table = dynamodb.Table('messageTable')
    currentTime = datetime.now()
    currTime = currentTime.strftime('%c')
    # creates a new item in the table
    table.put_item(
        Item={
            'messageId': messageId,
            'to': receiver,
            'from': sender,
            'message': message,
            'timestamp': currTime,
            'quickReplies': quickReplies,
        }
    )
    response = jsonify(get_response(status_code=201, message="Table Updated"))
    return response

# helper function to update table for replies
def storeReplies(replyId,messageId,reply,qrFlag):
    table = dynamodb.Table('replyTable')
    currentTime = datetime.now()
    currTime = currentTime.strftime('%c')
    quickReply = ''
    if qrFlag == True:
        quickReply = reply
        reply = None

    table.put_item(
        Item={
            'replyId': replyId,
            'messageId': messageId,
            'message': reply,
            'timestamp': currTime,
            'quickReplies': quickReply,
        }
    )
    response = jsonify(get_response(status_code=201, message="Table Updated"))
    return response

# helper function to query message table
def query_message(messageId):
    table = dynamodb.Table('messageTable')
    print("Querying message table")
    response = table.query(
        KeyConditionExpression=Key('messageId').eq(messageId)
    )
    items = response['Items']
    return items

# helper function to query reply table
def query_reply(replyId):
    table = dynamodb.Table('replyTable')
    print("Querying reply table")
    response = table.query(
        KeyConditionExpression=Key('replyId').eq(replyId)
    )
    items = response['Items']
    return items

# initiate db with
# $FLASK_APP=app.py
# $flask init
@app.cli.command('init')
def init_db():
    create_tables()
    with app.app_context():
        #with app.open_resource('db_init.py', mode='r') as f:
        #   dynamo.create_all()
        print("----------Creating Users and Timeline Table------------")
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()
        print("User and Timeline Table Initialized and Populated!")

# home page
@app.route('/', methods=['POST'])
def home():
    return jsonify(get_response(status_code=200, message="Welcome to CPSC-449 Twitter like API application"))

# function to send a direct message to a user. The quickReplies parameter is optional
@app.route("/sendMessage", methods=['POST'])
def sendDirectMessage():
    params = request.get_json()
    to = params.get('to')
    from_ = params.get('from')
    message = params.get('message')
    quickReplies = params.get('quickReplies')
    if not to or not from_ or not message:
        return jsonify(get_response(status_code=409, message="to / from / message is not in request")), 409
    else:
        user1 = query_db('select * from users where username = ?', [to], one=True)
        user2 = query_db('select * from users where username = ?', [from_], one=True)
        if not user1 or not user2:
            return jsonify(get_response(status_code=409, message="Username/s does not exist. Consider creating user first")), 409
        else:
            messageId = str(uuid.uuid4())
            putItem = storeSentDm(messageId,to,from_,message,quickReplies)
            items = query_message(messageId)
            response = jsonify(get_response(status_code=201, message=items))
            response.status_code = 201
            response.autocorrect_location_header = False
            return response


# Replies to a direct message. The reply parameter may either be a text message or a quick-reply value.
@app.route("/reply", methods=['POST'])
def replyToDirectMessage():
    params = request.get_json()
    messageId = params.get('messageId')
    reply = params.get('reply')
    qrFlag = False
    if not reply:
        reply = params.get('quickReplies')
        qrFlag = True
    if not messageId or not reply:
        return jsonify(get_response(status_code=409, message="messageId / reply is not in request")), 409
    else:
        try:
            items = query_message(messageId)
            if not items:
                return jsonify(get_response(status_code=404, message="MessageId does not exist")), 409
        finally:
                table = dynamodb.Table('replyTable')
                replyId = str(uuid.uuid4())
                putItems = storeReplies(replyId,messageId,reply,qrFlag)
                items = query_reply(replyId)
                response = jsonify(get_response(status_code=201, message=items))
                response.status_code = 201
                response.autocorrect_location_header = False
                return response

# Lists a user's DMs.
@app.route("/list/messages", methods=['GET'])
def listDirectMessagesFor():
    params = request.get_json()
    username = params.get('username')
    messages = []
    if not username:
        return jsonify(get_response(status_code=409, message="username is not in request")), 409

    user = query_db('select * from users where username = ?', [username], one=True)
    if not user:
        return jsonify(get_response(status_code=409, message="Username/s does not exist. Consider creating user first")), 409
    
    table = dynamodb.Table('messageTable')
    print("Querying message table")
    response = table.scan(
        FilterExpression=Attr('to').eq(username)
        )
    items = response['Items']
    for item in items:
        messages.append(item['message'])
    response = jsonify(get_response(status_code=200, message=messages))
    response.status_code = 200
    response.autocorrect_location_header = False
    return response

# Lists the replies to a DM
@app.route("/list/replies", methods=['GET'])
def listRepliesTo():
    params = request.get_json()
    messageId = params.get('messageId')
    replies = []
    if not messageId:
        return jsonify(get_response(status_code=409, message="messageId is not in request")), 409
    
    table = dynamodb.Table('replyTable')
    print("Querying reply table")
    response = table.scan(
        FilterExpression=Attr('messageId').eq(messageId)
        )
    items = response['Items']
    for item in items:
        replies.append(item['message'])
    response = jsonify(get_response(status_code=200, message=replies))
    response.status_code = 200
    response.autocorrect_location_header = False
    return response

if __name__ == "__main__":
    app.run(debug = True)
    #app = create_app()