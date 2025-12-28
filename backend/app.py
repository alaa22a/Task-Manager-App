import os
from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv

from models import db, User, Task

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default-dev-secret-key')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///taskmanager.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'default-jwt-secret-key')

CORS(app)
db.init_app(app)
jwt = JWTManager(app)

with app.app_context():
    db.create_all()

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'ok'})

# --- Auth Routes ---

@app.route('/api/auth/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data or not data.get('email') or not data.get('password') or not data.get('name'):
        return jsonify({'message': 'Missing required fields'}), 400
    
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'message': 'User already exists'}), 400

    hashed_pw = generate_password_hash(data['password'])
    new_user = User(name=data['name'], email=data['email'], password_hash=hashed_pw)
    
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({'message': 'User created successfully'}), 201

@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'message': 'Missing email or password'}), 400

    user = User.query.filter_by(email=data['email']).first()
    
    if user and check_password_hash(user.password_hash, data['password']):
        access_token = create_access_token(identity=str(user.id))
        return jsonify({
            'access_token': access_token,
            'user': {
                'id': user.id,
                'name': user.name,
                'email': user.email
            }
        }), 200

    return jsonify({'message': 'Invalid credentials'}), 401

# --- Task Routes ---

@app.route('/api/tasks', methods=['GET'])
@jwt_required()
def get_tasks():
    current_user_id = int(get_jwt_identity())
    tasks = Task.query.filter_by(user_id=current_user_id).order_by(Task.created_at.desc()).all()
    return jsonify([task.to_dict() for task in tasks]), 200

@app.route('/api/tasks', methods=['POST'])
@jwt_required()
def create_task():
    current_user_id = int(get_jwt_identity())
    data = request.get_json()
    
    if not data or not data.get('title'):
        return jsonify({'message': 'Title is required'}), 400

    new_task = Task(
        title=data['title'],
        description=data.get('description', ''),
        status=data.get('status', 'pending'),
        user_id=current_user_id
    )
    
    db.session.add(new_task)
    db.session.commit()
    
    return jsonify(new_task.to_dict()), 201

@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
@jwt_required()
def update_task(task_id):
    current_user_id = int(get_jwt_identity())
    task = Task.query.filter_by(id=task_id, user_id=current_user_id).first()
    
    if not task:
        return jsonify({'message': 'Task not found'}), 404
        
    data = request.get_json()
    
    if 'title' in data:
        task.title = data['title']
    if 'description' in data:
        task.description = data['description']
    if 'status' in data:
        task.status = data['status']
        
    db.session.commit()
    return jsonify(task.to_dict()), 200

@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
@jwt_required()
def delete_task(task_id):
    current_user_id = int(get_jwt_identity())
    task = Task.query.filter_by(id=task_id, user_id=current_user_id).first()
    
    if not task:
        return jsonify({'message': 'Task not found'}), 404
        
    db.session.delete(task)
    db.session.commit()
    return jsonify({'message': 'Task deleted'}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)
