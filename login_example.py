from flask import Flask, render_template, url_for, request, session, redirect
import pymongo
import bcrypt
import json
from flask import jsonify
import random
from pprint import pprint
import certifi

app = Flask(__name__)


client = pymongo.MongoClient("mongodb+srv://aakarshachug:password@cluster0-qtf6n.mongodb.net/test?retryWrites=true&w=majority",tlsCAFile=certifi.where())
db = client.chatbot

@app.route('/')
def index():
    if 'username' in session:
        s = session['username']
        return render_template('bot.html' , name = s)

    return render_template('index.html')

@app.route('/login', methods=['POST','GET'])  
def login():
    users = db.login_details
    login_user = users.find_one({'name' : request.form['username']})

    if login_user:
        #if bcrypt.hashpw(request.form['pass'].encode('utf-8'), login_user['password'].encode('utf-8')) == login_user['password'].encode('utf-8'):
         user_pass = login_user['password']
         if bcrypt.checkpw(request.form['pass'].encode('utf-8'), user_pass):
            session['username'] = request.form['username']
            return redirect(url_for('index'))

    return 'Invalid username/password combination'


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        users = db.login_details
        existing_user = users.find_one({'name' : request.form['username']})

        if existing_user is None:
            #hashpass = bcrypt.hashpw(request.form['pass'].encode('utf-8'), bcrypt.gensalt())
            hashpass = bcrypt.hashpw(request.form['pass'].encode('utf8'), bcrypt.gensalt())
            users.insert_one({'name' : request.form['username'], 'password' : hashpass})
            session['username'] = request.form['username']
            return redirect(url_for('index'))
        
        return 'That username already exists!'

    return render_template('register.html')

@app.route('/botresponse' , methods=['POST' , 'GET'])
def botresponse():
    bot_reply = db.responses
    
    history = db.chat_history
    s = session['username']
    user_input = request.json['text']
    bot_reply.create_index([('user', pymongo.TEXT)], name='search_index', default_language='english')
    print("User", user_input)
    cursor = bot_reply.find(
            {'$text': {'$search': user_input }},
            {'score': {'$meta': 'textScore'}})

        
    query_response =  cursor.sort([('score', {'$meta': 'textScore'})])
    #myquery = { "user": user_input }
    #query_response = bot_reply.find_one(myquery)
    x = query_response[0]['bot']

    
    if query_response is not None:
        r = random.choice(x)

    else:
        r = "I don't know about this :("
        print(r)
    if user_input is not None:
        answer = user_input
    
    if answer:
        if history.find_one({'username' : s}) :
            history.update_one({'username' : s} , { "$push": {"user" : answer , "bot" : r}})
            
        else:
            history.insert_one({"username" : s ,"user" : [answer] , "bot" : [r]})

        

        return jsonify({'user' : answer , 'bot' : r})
    
    return jsonify({'error' : 'Missing data'})


@app.route('/gethistory' , methods=['POST'])
def gethistory():
    history = db.chat_history
    s = session['username']
    cursor =  history.find_one({"username" : s})
    user_messages = cursor['user']
    bot_messages = cursor['bot']
    print(user_messages)
    print(bot_messages)
 
    return jsonify({'user' : user_messages , 'bot' : bot_messages})



if __name__ == '__main__':
    app.secret_key = 'mysecret'
    app.run(debug=True)