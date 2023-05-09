from flask import Flask, jsonify, request
from jsonschema import Draft7Validator
from bson import ObjectId
from flask_cors import CORS
import db
import json
import bcrypt
import time

# getting the collection from db
db = db.connect()
collection = db['User']
todoCollection = db['Todo']

# creating a new instance of flask 
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": ["http://localhost:5173"]}})
# reading the content of the userSchema
with open ('./models/userSchema.json') as f:
    schema = json.load(f)
    # print(schema)

# reading the content of the todoSchema
with open ('./models/todoSchema.json') as f:
    todoSchema = json.load(f)
    # print(schema)

# adding user 
@app.route('/addUser',methods=['POST'])
def addUser():
    data = request.json
    # creating the validator instance
    validator = Draft7Validator(schema)
    # storing errors 
    errors = list(validator.iter_errors(data))
    print(errors)
    if len(errors) != 0:
        return jsonify({"message":"enter complete information"}), 404
    try:
        user = collection.find_one({"email":data["email"]})
        if user is None:
            val = data["password"]
            # encoding the password for converting it into hash
            password = val.encode("utf-8")
            # got the hashed password but we need to decode it to get it in string format
            hashedPassword = bcrypt.hashpw(password,bcrypt.gensalt()).decode("utf-8")
            print(hashedPassword)
            # insert the user into the collection
            userInsertedVal =  collection.insert_one({"name":data["name"],"email":data["email"], "password":hashedPassword})
            return jsonify({"status":"success","data":str(userInsertedVal.inserted_id)}), 201
        else:
            return jsonify({"status":"failure","message":"A user with this email already exists"}), 404
    except Exception as err:
        print(err)
        return jsonify({"message":"Internal server error"}), 500
    
# login user endpoint
@app.route('/login', methods=['POST'])
def login():
    # storing the data passed 
    data = request.json
    if 'email' not in data or 'password' not in data:
        return jsonify({"status":"failure","message":"enter complete information"}), 404
    try:
        # finding the user with the passed email id
        user = collection.find_one({"email":data["email"]})
        print(user)
        # if user is not found then return credentials error
        if(user == None):
            return jsonify({"status":"failure","message":"Please enter correct credentials"}), 401
        # else check whether the password is correct
        if bcrypt.checkpw(data["password"].encode("utf-8"),user["password"].encode("utf-8")):
            # print("same")
            # if password is correct then send success message
            print(user["_id"])
            return jsonify({"status":"success","data":str(user["_id"])}), 200
        else:
            # else return incorrect credentials message
            return jsonify({"status":"failure","message":"Please enter correct credentials"}), 401
    except Exception as err:
        print(err)
        # catch exception and return
        return jsonify({"message":"error"}), 500
    
# add Todo
@app.route("/addTodo/<userid>", methods=["POST"])
def addTodo(userid):
    # storing the value send as request body to data
    data = request.json
    # checking whether title and description are there in the data
    if "title" not in data:
        return jsonify({"status":"failure","message":"enter complete information"}), 404
    try:
        # getting the user with the userid
        user = collection.find_one({"_id":ObjectId(userid)})
        # if user is found then add the todo with the given userid
        if user is not None:
            local_time = time.localtime(time.time())
            finalTime = time.strftime("%d-%m-%Y %H:%M:%S", local_time)
            insertVal = todoCollection.insert_one({"title":data["title"],"userid":userid,"createdAt":finalTime})
            return jsonify({"status":"success","data":str(insertVal.inserted_id)}), 201
        else:
            # return bad request
            return jsonify({"status":"failure","message":"failure no user exists"}), 404
    except Exception as e:
        print(e)
        return jsonify({"status":"failure","message":"internal server error"}), 500

# get the todos based on userid
@app.route('/getTodo/<userid>', methods=['GET'])
def getTodos(userid):
    print("hello")
    # getting all the todos with the userid provided
    todos = todoCollection.find({"userid":userid})
    print(todos)
    todoList = []
    if todos is not None:
        print("entered inside ")
        for todo in todos:
            print(todo)
            # appending todo one by one to the todoList
            todoList.append({"title":todo["title"], "todoId":str(todo["_id"])})
        # returning all the todos
        return jsonify({"status":"success","data":todoList})
    else:
        # returning nothing to display
        return jsonify({"message":"nothing to display"})


@app.route("/deleteTodo/<todoId>")
def deleteTodo(todoId):
    # finding the todo
    todo = todoCollection.find_one({"_id":ObjectId(todoId)})
    # if todo with given id is present
    if(todo is not None):
        # getting the response on delete
        response = todoCollection.delete_one({"_id":ObjectId(todoId)})
        if response.acknowledged:
            return jsonify({"status":"success","message":"deleted the todo with id:"+todoId})
    else:
        return jsonify({"status":"false","message":"no todo found with id:"+todoId}), 404

if __name__ == "__main__":
    app.run(debug=True,port=8081)
