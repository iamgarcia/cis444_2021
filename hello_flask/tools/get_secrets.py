JWT_SECRET = ""

def get_jwt_value():
	return JWT_SECRET

def get_secret():
	if not get_jwt_value():
		with open("secret.txt", "r") as f:
			global JWT_SECRET
			JWT_SECRET = f.read()
			JWT_SECRET = JWT_SECRET.rstrip('\n\r')

	return JWT_SECRET
