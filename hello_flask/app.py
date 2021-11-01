from flask import Flask,render_template,request, jsonify
from flask_json import FlaskJSON, JsonError, json_response, as_json

import jwt
import datetime
import bcrypt

from db_con import get_db_instance, get_db

app = Flask(__name__)
FlaskJSON(app)

JWT_SECRET = None
TOKEN = None

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
def isValidToken(token):
	if TOKEN is None:
		print("The server has no token.")
		return False
	else:
		server_token = jwt.decode(TOKEN, JWT_SECRET, algorithms=["HS256"])
		client_token = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])

		if server_token == client_token:
			print("The token is valid.")
			return True
		else:
			print("The token is invalid.")
			return False

def getUserId(token):
	return jwt.decode(TOKEN, JWT_SECRET, algorithms=["HS256"])

@app.route('/', methods=['GET']) #endpoint
def index():
	return render_template('books_app.html')

@app.route('/login', methods=['POST']) #endpoint
def login():
	form = request.form
	cur = global_db_con.cursor()
	cur.execute("SELECT * FROM users WHERE username='" + form['username'] + "';")
	row = cur.fetchone()

	if row is None:
		print("The username '" + form['username'] + "' does not exist.")
		return json_response(data={"message": "The username '" + form['username'] + "' does not exist."}, status=404)
	else:
		if form['password'] == row[2]:
			print(form['username'] + " is authorized.")
			global TOKEN
			TOKEN = jwt.encode({"user_id": row[0]}, JWT_SECRET, algorithm="HS256")
			return json_response(data={"jwt": TOKEN})
		else:
			print('The password for ' + form['username'] + ' is incorrect.')
			return json_response(data={"message": "The password for '" + form['username'] + "' is incorrect."}, status=404)

@app.route('/getBooks', methods=['POST'])
def getBooks():
	form = request.form

	if isValidToken(form['jwt']) == True:
		print("Token is valid. Retrieving books.")
		cur = global_db_con.cursor()

		try:
			jwt_str = getUserId(TOKEN)
			cur.execute("SELECT * FROM books WHERE NOT EXISTS " +
					"(SELECT FROM purchased_books WHERE " +
					"books.id = purchased_books.book_id AND " +
					jwt_str['user_id'] + " = purchased_books.user_id)")
			print("Retrieved books.")
		except:
			print("Unable to retrieve books.")
			return json_response(data={"message": "Unable to retrieve books."}, status=500)

		# Process cur.execute
	else:
		print()
		return json_response(data={"message": "Token is invalid."}, status=404)

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

