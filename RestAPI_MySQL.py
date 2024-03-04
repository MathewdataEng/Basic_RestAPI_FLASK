from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_mysqldb import MySQL

app = Flask(__name__)
api = Api(app)

# MySQL configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'RestAPI'

# Initialize MySQL extension
mysql = MySQL(app)


def create_table_if_not_exists():
    with app.app_context():
        cursor = mysql.connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS to_do_list (
                id INT AUTO_INCREMENT PRIMARY KEY,
                task VARCHAR(255) NOT NULL,
                summary VARCHAR(255) NOT NULL
            )
        """)
        mysql.connection.commit()


create_table_if_not_exists()  # Call the function to create the table

# Define request parsers
parser = reqparse.RequestParser(bundle_errors=True)
parser.add_argument('task', type=str, required=True, help="The name of task is required")
parser.add_argument('summary', type=str, required=True, help="The Summary is required")

parser_update = reqparse.RequestParser(bundle_errors=True)
parser_update.add_argument('task', type=str)
parser_update.add_argument('summary', type=str)

# Helper functions for handling todo existence
def abort_if_todo_doesnt_exist(todo_id):
    with app.app_context():
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM to_do_list WHERE id=%s", (todo_id,))
        todo = cursor.fetchone()
        if not todo:
            abort(404, message="Todo {} doesn't exist".format(todo_id))
        return todo


# Resource fields for marshalling
resource_fields = {
    'id': fields.Integer,
    'task': fields.String,
    'summary': fields.String
}


# Helper function for formatting todo
def format_todo(todo):
    return {'id': todo[0], 'task': todo[1], 'summary': todo[2]}


# TodoList resource
class TodoList(Resource):
    @marshal_with(resource_fields)
    def get(self):
        with app.app_context():
            cursor = mysql.connection.cursor()
            cursor.execute("SELECT * FROM to_do_list")
            tasks = cursor.fetchall()
            return [format_todo(task) for task in tasks], 200

    @marshal_with(resource_fields)
    def post(self):
        args = parser.parse_args()
        with app.app_context():
            cursor = mysql.connection.cursor()
            cursor.execute("INSERT INTO to_do_list (task, summary) VALUES (%s, %s)", (args['task'], args['summary']))
            mysql.connection.commit()
            cursor.execute("SELECT * FROM to_do_list WHERE id=(SELECT LAST_INSERT_ID())")
            new_todo = cursor.fetchone()
            return format_todo(new_todo), 201

# Todo resource
class Todo(Resource):
    @marshal_with(resource_fields)
    def get(self, todo_id):
        todo = abort_if_todo_doesnt_exist(todo_id)
        return format_todo(todo),200

    @marshal_with(resource_fields)
    def delete(self, todo_id):
        todo = abort_if_todo_doesnt_exist(todo_id)
        if todo:
            with app.app_context():
                cursor = mysql.connection.cursor()
                cursor.execute("DELETE FROM to_do_list WHERE id=%s", (todo_id,))
                mysql.connection.commit()
                return None, 204
        
    @marshal_with(resource_fields)
    def put(self, todo_id):
        args = parser_update.parse_args()
        with app.app_context():
            cursor = mysql.connection.cursor()
            # Update task if provided
            if args['task']:
                cursor.execute("UPDATE to_do_list SET task=%s WHERE id=%s", (args['task'], todo_id))
                mysql.connection.commit()
            # Update summary if provided (separate statement for clarity)
            if args['summary']:
                cursor.execute("UPDATE to_do_list SET summary=%s WHERE id=%s", (args['summary'], todo_id))
                mysql.connection.commit()
            # No need to fetch and return the updated todo here (optional)
            todo = abort_if_todo_doesnt_exist(todo_id)
            return format_todo(todo),202 # HTTP 202 Accepted indicates successful processing

## Actually setup the Api resource routing here
##
api.add_resource(TodoList, '/todos')
api.add_resource(Todo, '/todos/<int:todo_id>')


if __name__ == '__main__':
    app.run(host = '0.0.0.0',debug=True,port=8000)

