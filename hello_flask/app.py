from flask import Flask, render_template, request
from flask_json import FlaskJSON, JsonError, json_response, as_json

import json
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

	# The server does not have a token saved.
	if TOKEN is None:
		print("There is no token saved on the server.")
		return False
	else:
		# Decoding server side and client side tokens.
		server_token = expose_jwt_token(TOKEN)
		client_token = expose_jwt_token(token)

		# Comparing the server side and client side tokens
		# to see if they're a match.
		# If the tokens are equivalent, return True.
		# Else, the token is invalid, return False.
		return True if server_token == client_token else False

def expose_jwt_token(token):
	return jwt.decode(token, JWT_SECRET, algorithms=["HS256"])

@app.route('/', methods=['GET']) # Endpoint
def index():
	return render_template('books_app.html')

@app.route('/login', methods=['POST']) # Endpoint
def login():
	cursor = global_db_con.cursor()
	cursor.execute("SELECT * FROM users WHERE username = '%s';" % (request.form['username']))
	psql_row = cursor.fetchone()

	if psql_row is None:
		print("The username '" + request.form['username'] + "' does not exist.")
		return json_response(data={"message": "The username '" + request.form['username'] + "' does not exist."}, status=404)
	else:
		if request.form['password'] == psql_row[2]:
			print(request.form['username'] + " is authorized.")
			global TOKEN
			TOKEN = jwt.encode({"user_id": psql_row[0]}, JWT_SECRET, algorithm="HS256")
			return json_response(data={"jwt": TOKEN})
		else:
			print('The password for ' + request.form['username'] + ' is incorrect.')
			return json_response(data={"message": "The password for '" + request.form['username'] + "' is incorrect."}, status=404)

@app.route('/getBooks', methods=['POST']) # Endpoint
def getBooks():
	if isValidToken(request.form['jwt']) == True:
		print("The token is valid. Processing the retrieval of books...")
		cursor = global_db_con.cursor()

		try:
			exposed_jwt_token = expose_jwt_token(TOKEN)

			# Thanks Professor Jardin for the suggestion. I figured out how to achieve something similar
			# using the joins method. Works like a charm!
			psql_str = " ".join((
				"SELECT * FROM books WHERE NOT EXISTS",
				"(SELECT FROM purchased_books WHERE books.id = purchased_books.book_id AND",
				str(exposed_jwt_token['user_id']),
				"= purchased_books.user_id);"
			))

			cursor.execute(psql_str)
			print("Successfully retrieved books.")
		except:
			print("Failed to retrieve books.")
			return json_response(data={"message": "Failed to retrieve books."}, status=500)

		message = "{\"books\":["
		book_items = 0

		while True:
			psql_row = cursor.fetchone()

			if psql_row is None:
				print("There are no more books to add.")
				break;
			else:
				print("Adding a book to the JSON structure...")

				if book_items > 0: message += ","

				book_items += 1

				# Here, I used a string with string formatting. It's also a variation
				# of Jardin's recommendation.
				message += "{\"book_id\": %s, \"author\": \"%s\", \"title\": \"%s\", \"price\": %s}" % (str(psql_row[0]), psql_row[1], psql_row[2], str(psql_row[3]))

				print("Added a book to the JSON structure.")

		message += "]}"
		print("The books JSON payload has been created.")
		return json_response(data=json.loads(message))
	else:
		print("The token is invalid.")
		return json_response(data={"message": "The token is invalid."}, status=404)

@app.route('/purchaseBook', methods=["POST"]) # Endpoint
def purchaseBook():
	cursor = global_db_con.cursor()

	try:
		exposed_jwt_token = expose_jwt_token(TOKEN)
		cursor.execute("INSERT INTO purchased_books (user_id, book_id) VALUES (%s, %s);" % (str(exposed_jwt_token['user_id']), str(request.form['book_id'])))
		global_db_con.commit()
		print("Book purchase was successful.")
		return json_response(data={"message": "Book purchase was successful."})

	except:
		print("Failed to write to the \"purchased_books\" table.")
		return json_response(data={"message": "Failed to write to the \"purchased_books\" table."}, status=500)

@app.route('/exposejwt') # Endpoint
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

