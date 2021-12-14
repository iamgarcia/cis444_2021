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
		psql_str = " ".join((
			"SELECT * FROM books WHERE NOT EXISTS",
			"(SELECT FROM purchased_books WHERE books.id = purchased_books.book_id AND",
			str(user_id),
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
			message += "{\"author\": \"%s\", \"title\": \"%s\", \"price\": %s, \"book_id\": %s}" % (psql_row[1], psql_row[2], str(psql_row[3]), str(psql_row[0]))

			print("Added a book to the JSON structure.")

	message += "]}"
	print("The books JSON payload has been created.")
	return json_response(data=json.loads(message))
