from flask import request, g
from flask_json import FlaskJSON, JsonError, json_response, as_json
from tools.token_tools import create_token

import json

from tools.logging import logger


def handle_request():
	logger.debug("Get Wishlist Handle Request")
	cursor = g.db.cursor()

	try:
		user_id = g.jwt_data['user_id']

		# Thanks Professor Jardin for the suggestion. I figured out how to achieve something similar using
		# the joins method. Works like a charm!
		psql_str = "SELECT * FROM wishes ORDER BY timestamp ASC;"
		cursor.execute(psql_str)
		#print("Successfully retrieved wishes.")
	except:
		#print("Failed to retrieve wishes.")
		return json_response(data={"message": "Failed to retrieve wishes."}, status=500)

	message = "{\"wishes\":["
	wish_count = 0

	while True:
		psql_row = cursor.fetchone()

		if psql_row is None:
			#print("There are no more wishes to add.")
			break;
		else:
			#print("Adding a wish to the JSON structure...")

			if wish_count > 0: message += ","

			wish_count += 1

			# Here, I used a string with string formatting. It's also a variation
			# of Jardin's recommendation.
			message += "{\"wish\": \"%s\", \"timestamp\": \"%s\"}" % (psql_row[0], psql_row[2])

			#print("Added a wish to the JSON structure.")

	message += "]}"
	#print("The wish JSON payload has been created.")
	return json_response(data=json.loads(message))
