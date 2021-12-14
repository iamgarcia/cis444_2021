from flask import request, g
from flask_json import FlaskJSON, JsonError, json_response, as_json
from tools.token_tools import create_token

import jwt

from tools.logging import logger


def handle_request():
    logger.debug("Signup Handle Request")

    username_from_form = request.form["username"]
    password_from_form = request.form["password"]

    cursor = g.db.cursor()
    cursor.execute(f"SELECT * FROM users "
                   f"WHERE username = '{username_from_form}';")
    psql_row = cursor.fetchone()

    # If there are no users under that name, create a user
    if psql_row is None:
        cursor.execute(f"INSERT INTO users (username, password) VALUES "
                       f"('{username_from_form}', '{password_from_form}');")
        g.db.commit()
        cursor.execute(f"SELECT * FROM users "
                       f"WHERE username = '{username_from_form}';")
        psql_row = cursor.fetchone()
        user = {"user_id": psql_row[0]}
        return json_response(data={"jwt": create_token(user)})
    # Otherwise, if there is a user under that name, inform
    # the user of the taken name and tell them to
    # try a different name
    else:
        return json_response(data={"message": "The username '" + username_from_form + "' is already taken."}, status=404)
