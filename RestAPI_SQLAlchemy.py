from flask import Flask
from flask_restful import reqparse, abort, Api, Resource,fields,marshal_with
from flask_sqlalchemy import SQLAlchemy
from os.path import exists

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///project.db"
db = SQLAlchemy(app)
db_path = '.\instance\project.db'

class ToDoModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(200))
    summary = db.Column(db.String(500))

if not exists(db_path):
    with app.app_context():
        db.create_all()
        print('Created new Database')



# TODOS = {
#     1: {"Task": "Write Hello program","summary":"write hello"}
# }
parser = reqparse.RequestParser(bundle_errors=True)
parser.add_argument('task', type=str, required=True, help="The name of task is required")
parser.add_argument('summary', type=str, required=True,help = "The Summary is required")

parser_update = reqparse.RequestParser(bundle_errors=True)
parser_update.add_argument('task', type=str)
parser_update.add_argument('summary', type=str)


def abort_if_todo_doesnt_exist(todo_id):
    task = ToDoModel.query.filter_by(id=todo_id).first()
    if not task:
        abort(404, message="Todo {} doesn't exist".format(todo_id))
    if task:
        return task

def abort_if_todo_does_exist(todo_id):
    task = ToDoModel.query.filter_by(id=todo_id).first()
    if task:
        abort(409, message="Todo {} already exist".format(todo_id))

resourse_fields = {
    'id' : fields.Integer,
    'task': fields.String,
    'summary': fields.String
}

# Todo
# shows a single todo item and lets you delete a todo item
class Todo(Resource):
    @marshal_with(resourse_fields)
    def get(self, todo_id):
        task = abort_if_todo_doesnt_exist(todo_id)
        return task
    
    @marshal_with(resourse_fields)
    def delete(self, todo_id):
        task = abort_if_todo_doesnt_exist(todo_id)
        db.session.delete(task)
        db.session.commit()  # Commit the deletion to the database
        return task, 204
    
    @marshal_with(resourse_fields)
    def post(self, todo_id):
        args = parser.parse_args()
        abort_if_todo_does_exist(todo_id)
        todo = ToDoModel(id=todo_id, task=args['task'],summary=args['summary'])
        db.session.add(todo)
        db.session.commit()
        return todo, 200

    @marshal_with(resourse_fields)
    def put(self, todo_id):
        args = parser_update.parse_args()
        task = abort_if_todo_doesnt_exist(todo_id)
        if args['task']:
            task.task = args['task']
        if args['summary']:
            task.summary = args['summary']
        db.session.commit()
        return task, 201



# TodoList
# shows a list of all todos, and lets you POST to add new tasks
class TodoList(Resource):
    @marshal_with(resourse_fields)
    def get(self):
        tasks = ToDoModel.query.all()
        return tasks
    

##
## Actually setup the Api resource routing here
##
api.add_resource(TodoList, '/todos')
api.add_resource(Todo, '/todos/<int:todo_id>')


if __name__ == '__main__':
    app.run(host = '0.0.0.0',debug=True,port=8000)
