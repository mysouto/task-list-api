import json
from flask import abort, Blueprint, jsonify, make_response, request
from app import db
from app.models.task import Task

# create instance of blueprint class
tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")


# error handling
def validate_task(task_id):
    # invalid task id
    try:
        task_id = int(task_id)
    except:
        abort(make_response({{"message": f"Invalid task id {task_id}."}}, 400))

    task = Task.query.get(task_id)

    # task not found
    if not task:
        abort(make_response({"message": f"Task {task_id} not found."}, 404))

    return task


# Wave 1 - Create a Task
@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()

    new_task = Task(
        title=request_body["title"],
        description=request_body["description"],
        completed_at=None
    )

    # add to dict
    db.session.add(new_task)
    # submit changes
    db.session.commit()

    # TODO create method to convert response to json
    # task_dict = Task.to_dict(new_task)
    response = {
        "task": new_task.to_dict()
    }

    return response, 201


@tasks_bp.route("", methods=["GET"])
def read_all_tasks():
    tasks_response = []
    tasks = Task.query.all()
    for task in tasks:
        task_dict = task.to_dict()

        tasks_response.append(task_dict)

    return jsonify(tasks_response)


# Create GET route for 1 task
@tasks_bp.route("/<task_id>", methods=["GET"])
def get_one_bike(task_id):
    chosen_task = validate_task(task_id)
    # chosen_task = Task.query.get(task_id)

    # returns jsonified object and response code as tuple
    response = {
        "task": chosen_task.to_dict()
    }

    return response, 200


# Update Task
@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_task(task_id)

    request_body = request.get_json()
    task.title = request_body["title"]
    task.description = request_body["description"]

    response = {
        "task": task.to_dict()
    }

    db.session.commit()

    return jsonify(response), 200
# REQUEST
# {
#   "title": "Updated Task Title",
#   "description": "Updated Test Description",
# }
# RESPONSE
# {
#   "task": {
#     "id": 1,
#     "title": "Updated Task Title",
#     "description": "Updated Test Description",
#     "is_complete": false
#   }
# }


@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_task(task_id)

    db.session.delete(task)
    db.session.commit()

    response = {
        "details": f"Task {task.title} successfully deleter"
    }

    return jsonify(response), 200

# RESPONSE
# {
#   "details": "Task 1 \"Go on my daily walk 🏞\" successfully deleted"
# }
