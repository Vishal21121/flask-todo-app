from bson import ObjectId
from flask import jsonify, request
import time

def addTodo(userid,collection,todoCollection):
    # storing the value send as request body to data
    data = request.json
    if len(data["title"]) == 0:
        return jsonify({"status":"failure","message":"passed empty value"}), 400
    # checking whether title and description are there in the data
    if "title" not in data:
        return jsonify({"status":"failure","message":"enter complete information"}), 400
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

def getTodos(userid,todoCollection):
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

def deleteTodo(todoId,todoCollection):
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

def updateTodo(todoId,todoCollection):
    data = request.json
    todo = todoCollection.find_one({"_id":ObjectId(todoId)})
    if todo is not None:
        new_values = {"$set": {"title": data["title"]}}
        todoCollection.update_one({"_id":ObjectId(todoId)},new_values)
        return jsonify({"status":"success","message":f"updated todo with todo id {todoId}"})
    else:
        return jsonify({"status":"failure","message":"not updated any document"})