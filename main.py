from flask import Flask
from flask_cors import CORS
import db
import json
from routes.User import addUser, login
from routes.Todo import addTodo,getTodos,deleteTodo,updateTodo

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
def regiterUser():
    return addUser(schema, collection)
    
# login user endpoint
@app.route('/login', methods=['POST'])
def loginUser():
    return login(collection)
    
# add Todo
@app.route("/addTodo/<userid>", methods=["POST"])
def registerTodo(userid):
    return addTodo(userid,collection,todoCollection)

# get the todos based on userid
@app.route('/getTodo/<userid>', methods=['GET'])
def fetchTodo(userid):
    return getTodos(userid,todoCollection)


@app.route("/deleteTodo/<todoId>",methods=["DELETE"])
def removeTodo(todoId):
    return deleteTodo(todoId,todoCollection)

@app.route("/updateTodo/<todoId>",methods = ["PATCH"])
def modifyTodo(todoId):
   return updateTodo(todoId,todoCollection)

if __name__ == "__main__":
    app.run(debug=True,port=8081)
