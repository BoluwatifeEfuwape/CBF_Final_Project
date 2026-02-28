from flask import Flask
from routes.todos import todos_bp
from routes.users import users_bp

app = Flask(__name__)

# Register routes
app.register_blueprint(todos_bp, url_prefix='/api/todos')
app.register_blueprint(users_bp, url_prefix= '/api/users')


@app.route('/')
def home():
    return {
        'message': 'Todo API is running with authentication!',
        'endpoints': {
            'POST /api/users/register': 'Register new user',
            'POST /api/users/login': 'Login user',
            'GET /api/todos': 'Get all todos',
            'POST /api/todos': 'Create todo',
            'GET /api/todos/:id': 'Get single todo',
            'PUT /api/todos/:id': 'Update todo',
            'PATCH /api/todos/:id/toggle': 'Toggle completed',
            'DELETE /api/todos/:id': 'Delete todo'
        }
    }

if __name__ == '__main__':
    app.run(debug=True, port=5000)