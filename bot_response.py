from flask import Flask, render_template, url_for, request, session, redirect
import pymongo
import bcrypt
import json
from flask import jsonify

app = Flask(__name__)

@app.route('/')
def index():
	return render_template('bot.html')


@app.route('/botresponse' , methods=['POST'])
def botresponse():
	user_input = request.get_data(as_text=True)
	print(user_input)
	if user_input is not None:
		answer = user_input
	else:
		answer = "no input"
	print(answer)
	if answer:
		return jsonify({'name' : answer})
	
	return jsonify({'error' : 'Missing data'})



    
    

if __name__ == '__main__':
    app.secret_key = 'mysecret'
    app.run(debug=True)