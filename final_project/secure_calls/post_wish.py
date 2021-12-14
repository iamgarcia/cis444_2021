from flask import request, g
from flask_json import FlaskJSON, JsonError, json_response, as_json
from tools.token_tools import create_token

import json

from tools.logging import logger


def handle_request():
    logger.debug("Post Wish Handle Request")

    wish = request.form['wish']
    user_id = g.jwt_data['user_id']
    timestamp = request.form['timestamp']

    cursor = g.db.cursor()

    try:
        cursor.execute(f"INSERT INTO wishes (wish, user_id, timestamp) VALUES ('{wish}', '{user_id}', '{timestamp}');")
        g.db.commit()
        print("Wish was posted successfully.")
        return json_response(data={"message": "Wish was posted successfully."})
    except:
        print("Failed to write to the \"wishes\" table.")
        return json_response(data={"message": "Failed to write to the \"wishes\" table."}, status=500)
