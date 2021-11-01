from flask import Flask,render_template,request, jsonify
from flask_json import FlaskJSON, JsonError, json_response, as_json

import jwt
import datetime
import bcrypt

from db_con import get_db_instance, get_db

app = Flask(__name__)
FlaskJSON(app)

JWT_SECRET = None

global_db_con = get_db()

with open("secret", "r") as f:
	JWT_SECRET = f.read()

@app.route('/backp',  methods=['POST']) #endpoint
def backp():
	print(request.form)
	salted = bcrypt.hashpw(bytes(request.form['fname'], 'utf-8') , bcrypt.gensalt(10))
	print(salted)
	print(bcrypt.checkpw(bytes(request.form['fname'], 'utf-8'), salted))
	return render_template('backatu.html',input_from_browser= str(request.form) )

@app.route('/auth',  methods=['POST']) #endpoint
def auth():
        print(request.form)
        return json_response(data=request.form)

#Assigment 2
@app.route('/ss1') #endpoint
def ss1():
	return render_template('server_time.html', imgs_url=IMGS_URL[CUR_ENV])

@app.route('/getTime') #endpoint
def get_time():
	return json_response(data={"password": request.args.get('password'), "class": "cis44", "serverTime": str(datetime.datetime.now())})

#Assignment 3
@app.route('/', methods=['GET']) #endpoint
def index():
	return render_template('books_app.html')

@app.route('/login', methods=['POST']) #endpoint
def login():
	cur = global_db_con.cursor()
	cur.execute("SELECT * FROM users WHERE username='" + request.form['username'] + "';")
	row = cur.fetchone()

	if row is None:
		print("The username '" + request.form['username'] + "' does not exist.")
		return jsonify({"message1": "The username '" + request.form['username'] + "' does not exist."})
	else:
		if request.form['password'] == row[2]:
			print(request.form['username'] + " is authorized.")

			jwt_str = jwt.encode({"username": request.form['username'], "password": request.form['password']}, JWT_SECRET, algorithm="HS256")
			print(jwt_str)
			#return json_response(jwt=jwt_str)
			return jsonify({"message2": "Authentication successful."})
		else:
			print('The password for ' + request.form['username'] + ' is incorrect.')
			return jsonify({"message3": "The password for '" + request.form['username'] + "' is incorrect."})

@app.route('/exposejwt') #endpoint
def exposejwt():
    jwt_token = request.args.get('jwt')
    print(jwt_token)
    return json_response(output=jwt.decode(jwt_token, JWT_SECRET, algorithms=["HS256"]))

@app.route('/hellodb') #endpoint
def hellodb():
    cur = global_db_con.cursor()
    cur.execute("insert into music values( 'dsjfkjdkf', 1);")
    global_db_con.commit()
    return json_response(status="good")

app.run(host='0.0.0.0', port=80)

