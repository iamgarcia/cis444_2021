import psycopg2


def get_db():
    return psycopg2.connect(host="localhost", dbname="dearsanta" , user="santa", password="rudolph")

def get_db_instance():
	db  = get_db()
	cursor  = db.cursor( )
	return db, cursor
