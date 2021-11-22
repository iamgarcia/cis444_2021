from flask import request, g
from flask_json import FlaskJSON, JsonError, json_response, as_json
from tools.token_tools import create_token

import jwt

from tools.logging import logger

def handle_request():
	logger.debug("Login Handle Request")

	username_from_form = request.form["username"]
	password_from_form = request.form["password"]

	cursor = g.db.cursor()
	cursor.execute("SELECT * FROM users WHERE username = '%s';" % (username_from_form))
	psql_row = cursor.fetchone()

	if psql_row is None:
		return json_response(data={"message": "The username '" + username_from_form + "' does not exist."}, status=404)

	else:
		if password_from_form == psql_row[2]:
			user = {"user_id": psql_row[0]}
			return json_response(data={"jwt": create_token(user)})
		else:
			return json_response(data={"message": "The password for '" + username_from_form + "' is incorrect."}, status=404)
