from flask import Flask, jsonify, request
from jsonschema import Draft7Validator
import db
import json
import bcrypt

# getting the collection from db
collection = db.connect()

# creating a new instance of flask 
app = Flask(__name__)

# reading the content of the userSchema
with open ('./models/userSchema.json') as f:
    schema = json.load(f)
    print(schema)

# adding user 
@app.route('/addUser',methods=['POST'])
def addUser():
    data = request.json
    # creating the validator instance
    validator = Draft7Validator(schema)
    # storing errors 
    errors = list(validator.iter_errors(request.json))
    print(errors)
    if len(errors) != 0:
        return jsonify({"message":"some error occurred"})
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

if __name__ == "__main__":
    app.run(debug=True,port=8081)