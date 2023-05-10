from flask import Flask, jsonify, request
from jsonschema import Draft7Validator
import bcrypt

# adding user 
def addUser(schema,collection):
    data = request.json
    # creating the validator instance
    validator = Draft7Validator(schema)
    # storing errors 
    errors = list(validator.iter_errors(data))
    print(errors)
    if len(errors) != 0:
        return jsonify({"message":"enter complete information"}), 400
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
            return jsonify({"status":"failure","message":"A user with this email already exists"}), 401
    except Exception as err:
        print(err)
        return jsonify({"message":"Internal server error"}), 500


def login(collection):
    # storing the data passed 
    data = request.json
    if 'email' not in data or 'password' not in data:
        return jsonify({"status":"failure","message":"enter complete information"}), 400
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