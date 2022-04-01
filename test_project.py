import flask
from flask import request
import requests
import json
from bson import json_util
import pymongo
from pymongo import MongoClient


app = flask.Flask(__name__)
app.config["DEBUG"] = False

class User:
    def __init__(self, id, name, email, gender, status):
        self.id = id
        self.name = name
        self.email = email
        self.gender = gender
        self.status = status

active_users = []

@app.route('/', methods=['POST'])
def post():
    responseFromDataSource = requests.get("https://gorest.co.in/public/v2/users")
    for u in responseFromDataSource.json():
        if u['status'] == "active":
            active_users.append(User(u['id'], u['name'], u['email'], u['gender'], u['status']))
            print(u)

    try:
        conn = MongoClient()
        print("Connected successfully!!!")
    except:
        print("Could not connect to MongoDB")

    db = conn.users

    collection = db.active_users

    for user in active_users:
        collection.insert_one(user.__dict__)

    cursor = collection.find()
    for record in cursor:
        print(record)

    return "POSTAPI completed!"

@app.route('/', methods=['GET'])
def get():
    myuser = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myuser["users"]
    mycol = mydb["active_users"]
    mydoc = mycol.find({"gender":"female"})
    print(mydoc)
    json_docs = [json.dumps(doc, default=json_util.default) for doc in mydoc]
    return str(json_docs)

@app.route('/user', methods=['GET'])
def getUser():
    myuser = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myuser["users"]
    mycol = mydb["active_users"]
    mydoc = mycol.find(request.args)
    json_docs = [json.dumps(doc, default=json_util.default) for doc in mydoc]
    return str(json_docs)


app.run()
