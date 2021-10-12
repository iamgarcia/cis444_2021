from flask import Flask,render_template,request

import datetime

app = Flask(__name__)


USER_PASSWORDS = { "cjardin": "strong password"}

IMGS_URL = {
            "DEV" : "/static",
            "INT" : "https://cis444-2021-iamgarcia.s3.us-west-1.amazonaws.com/images",
            "PRD" : "https://d8brksoxvr34y.cloudfront.net/images"
            }

CUR_ENV = "PRD"

@app.route('/') #endpoint
def index():
    return 'Web App with Python Caprice!' + USER_PASSWORDS['cjardin']

@app.route('/buy') #endpoint
def buy():
    return 'Buy'

@app.route('/hello') #endpoint
def hello():
    return render_template('hello.html',img_url=IMGS_URL[CUR_ENV] ) 

@app.route('/back',  methods=['GET']) #endpoint
def back():
    return render_template('backatu.html',input_from_browser=request.args.get('usay', default = "nothing", type = str) )

@app.route('/backp',  methods=['POST']) #endpoint
def backp():
    return render_template('backatu.html',input_from_browser= str(request.form) )


#Assigment 2
@app.route('/ss1') #endpoint
def ss1():
    return render_template('server_time.html', imgs_url=IMGS_URL[CUR_ENV])

app.run(host='0.0.0.0', port=80)

