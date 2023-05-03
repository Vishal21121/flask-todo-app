from flask import Flask, jsonify, request
from jsonschema import Draft7Validator
from bson import ObjectId
import db
import json
import bcrypt

# getting the collection from db
db = db.connect()
collection = db['User']
todoCollection = db['Todo']

# creating a new instance of flask 
app = Flask(__name__)

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
        val = data["password"]
        # encoding the password for converting it into hash
        password = val.encode("utf-8")
        # got the hashed password but we need to decode it to get it in string format
        hashedPassword = bcrypt.hashpw(password,bcrypt.gensalt()).decode("utf-8")
        print(hashedPassword)
        # insert the user into the collection
        collection.insert_one({"name":data["name"],"email":data["email"], "password":hashedPassword})
        return jsonify({"message":"success"}), 201
    except Exception as err:
        print(err)
        return jsonify({"message":"Internal server error"}), 500
    
# login user endpoint
@app.route('/login', methods=['POST'])
def login():
    # storing the data passed 
    data = request.json
    if 'email' not in data or 'password' not in data:
        return jsonify({"message":"enter complete information"}), 404
    try:
        # finding the user with the passed email id
        user = collection.find_one({"email":data["email"]})
        print(user)
        # if user is not found then return credentials error
        if(user == None):
            return jsonify({"message":"Please enter correct credentials"}), 401
        # else check whether the password is correct
        if bcrypt.checkpw(data["password"].encode("utf-8"),user["password"].encode("utf-8")):
            # print("same")
            # if password is correct then send success message
            return jsonify({"message":"success"}), 200
        else:
            # else return incorrect credentials message
            return jsonify({"message":"Please enter correct credentials"}), 401
    except Exception as err:
        print(err)
        # catch exception and return
        return jsonify({"message":"error"}), 500
    
# add Todo
@app.route("/addTodo", methods=["POST"])
def addTodo():
    # storing the value send as request body to data
    data = request.json
    # validating the request body content
    validator = Draft7Validator(todoSchema)
    # storing errors 
    errors = list(validator.iter_errors(data))
    print(errors)
    # if errors are found
    if len(errors) != 0:
        return jsonify({"message":"enter complete information"}), 404
    try:
        # taking the userid from the request body
        userid = data["userid"]
        # getting the user with the userid
        user = collection.find_one({"_id":ObjectId(userid)})
        # if user is found then add the todo with the given userid
        if user is not None:
            todoCollection.insert_one(data)
            return jsonify({"message":"success"}), 201
        else:
            # return bad request
            return jsonify({"message":"failure no user exists"}), 404
    except Exception as e:
        print(e)
        return jsonify({"message":"internal server error"}), 500
    


if __name__ == "__main__":
    app.run(debug=True,port=8081)
