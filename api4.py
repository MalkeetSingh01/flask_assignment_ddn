from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users_info.db'
db = SQLAlchemy(app)


# from flask_jwt_extended import create_access_token
# from flask_jwt_extended import get_jwt_identity
# from flask_jwt_extended import jwt_required
# from flask_jwt_extended import JWTManager

# access_token = create_access_token(identity=data.get('username'))
#     return jsonify(access_token=access_token)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))

    def __init__(self, username, password):
        self.username = username
        self.password = password

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(30), db.ForeignKey("user.username"))
    status= db.Column(db.String(50))
    due_date = db.Column(db.String(50))
    task = db.Column(db.String(255))

    def __init__(self,data):
        return {
            'task':data.task,
            'user':data.user,
            "status":data.status,
            "due_date":data.due_date
        }


@app.route('/alltasks', methods=['GET'])
def get_all_tasks():
    tasks = Task.query.all()
    task_list = []
    for task in tasks:
        task_data = {
            'id': task.id,
            'task': task.task,
            'due_date': task.due_date.isoformat(),
            "status":task.status,
        }
        task_list.append(task_data)
    return jsonify({'tasks': task_list}), 200


@app.route('/home')
def home():
    return jsonify({"message":"home address"}),200


@app.route('/add',methods=['POST'])
def add_user():
    data=request.json
    username=data.get("username")
    password=data.get("password")
    # id=data.get('id')
    if not username or not password:
        return jsonify({'message': 'Username and password are required.'}), 400
    user =User.query.filter_by(username=username).first()
    if user:
        return jsonify({'message': 'Username Exists.'}), 401
    user = User(username=username, password=password)
    db.session.add(user)
    db.session.commit()

    return jsonify({'message': 'User added successfully.'}), 200
    


@app.route('/login',methods=['POST'])
def login_user():
    data=request.json
    username=data.get("username")
    password=data.get("password")

    if not username or not password:
        return jsonify({'message': 'Username and password are required.'}), 400
    
    user =User.query.filter_by(username=username, password=password).first()
    if not user:
        return jsonify({'message': 'Invalid credentials.'}), 401
    
    return jsonify({'message': 'Authentication successful.'}), 200
    

@app.route('/users', methods=['GET'])
def get_all_users():
    users = User.query.all()
    user_list = []
    for user in users:
        user_data = {
            'id': user.id,
            'username': user.username,
            'password': user.password
        }
        user_list.append(user_data)
    return jsonify({'users': user_list}), 200

@app.route("/tasks",methods=['GET'])
# @jwt_required()
def get_task():
    # users = Task.query.all()
    # current_user = get_jwt_identity()
    tasks = Task.query.filter_by(user = 'Malkeet')
    tasks = [t.to_dict() for t in tasks]
    return jsonify(tasks)

@app.route("/tasks",methods=['POST'])
# @jwt_required()
def add_task():
    # current_user = get_jwt_identity()
    data = request.get_json()
    if data.get('task') == None:
        return jsonify({'message': 'Addition task failed Add task.'}), 400
    task = Task(data)
    db.session.add(task)
    db.session.commit()
    return jsonify({'message': 'Addition of Task successfull.'}), 200


if __name__=="__main__":
    
    with app.app_context():
        db.create_all()
        app.debug=True
        app.run()