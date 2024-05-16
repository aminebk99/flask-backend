from flask import Flask, jsonify, request, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager, create_access_token
from flask_bcrypt import Bcrypt, generate_password_hash, check_password_hash


app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://myuser:secret@postgres:5432/mydatabase'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)
CORS(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(50), nullable=False)
    lastname = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    __tablename__ = "users"

    def __init__(self, username, password, firstname, lastname):
        self.username = username
        self.firstname = firstname
        self.lastname = lastname
        self.set_password(password)

    def set_password(self, password):
        self.password = generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return check_password_hash(self.password, password)


@app.route('/')
def hello_world():
    return "Hello world!"


@app.route('/users', methods=['GET'])
def get_all_users():
    users = User.query.all()
    user_list = [{'id': user.id, 'firstname': user.firstname, 'lastname': user.lastname, 'username': user.username, 'password': user.password} for user in users]
    return jsonify({'users': user_list})


@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    firstname = data.get('firstname')
    lastname = data.get('lastname')
    username = data.get('username')
    password = data.get('password')

    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({'message': 'Username already exists'}), 400

    new_user = User(firstname=firstname, lastname=lastname, username=username, password=password)
    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'User created successfully'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Failed to create user'}), 500
    
@app.route('/login', methods=['POST'])
def secure():
    data = request.get_json()
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({'error': 'Missing username or password'}), 400

    username = data['username']
    password = data['password']

    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password, password):
        token = create_access_token(identity=username)  
        return jsonify({'access_token': token}), 200
    else:
        return jsonify({'error': 'Invalid username or password'}), 401
    
    
@app.route('/login', methods=['POST'])
def secured_login():
    return jsonify({'login user'})
    # data = request.get_json()
    # username = data.get('username')
    # password = data.get('password')
    
    # user = User.query.filter_by(username=username, password = password).first()

    
    # access_token = create_access_token(identity=user, fresh=True)
    # return jsonify({'token': access_token}), 200
    



if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
