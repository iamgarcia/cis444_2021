import jwt
from functools import wraps
from flask import request, redirect, g
from flask_json import FlaskJSON, JsonError, json_response, as_json

from tools.logging import logger
from tools.get_secrets import get_secret


def token_required(f):
	@wraps(f)
	def _verify(*args, **kwargs):
		logger.debug("Token verification call.")
		secret = get_secret()

		invalid_message = {"message": "Invalid token. Registration or authentication required."}
		expired_message = {"message": "Token expired."}
		error_message = {"message": "An error has occured."}

		try:
			token = request.form["jwt"]
			logger.debug("Got token.")
			data = jwt.decode(token, secret, algorithms=["HS256"])
			print(data)
			g.jwt_data = data
			return f(*args, **kwargs)

		except jwt.ExpiredSignatureError:
			logger.debug("Expired JWT.")
			return json_response(message=expired_message, status=401)

		except jwt.InvalidTokenError:
			logger.debug("Invalid token.")
			return json_response(message=invalid_message, status=401)

		except Exception as e:
			logger.debug(e)
			return json_response(message=error_message, status=500)

	return _verify
