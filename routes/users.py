from flask import Blueprint, request, jsonify
from config import get_db_connection, hash_password, check_password, create_token

users_bp = Blueprint('users', __name__)

# Register new user
@users_bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        
        # Validate input
        if not username or not email or not password:
            return jsonify({'error': 'Username, email, and password are required'}), 400
        
        if len(password) < 6:
            return jsonify({'error': 'Password must be at least 6 characters'}), 400
        
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Check if user already exists
        cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
        if cursor.fetchone():
            cursor.close()
            conn.close()
            return jsonify({'error': 'Email already registered'}), 400
        
        cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
        if cursor.fetchone():
            cursor.close()
            conn.close()
            return jsonify({'error': 'Username already taken'}), 400
        
        # Hash password
        password_hash = hash_password(password)
        
        # Insert user
        cursor.execute(
            'INSERT INTO users (username, email, password_hash) VALUES (%s, %s, %s)',
            (username, email, password_hash)
        )
        conn.commit()
        
        # Get created user
        user_id = cursor.lastrowid
        cursor.execute('SELECT id, username, email, created_at FROM users WHERE id = %s', (user_id,))
        new_user = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        # Create token
        token = create_token(user_id)
        
        return jsonify({
            'message': 'User registered successfully',
            'token': token,
            'user': new_user
        }), 201
        
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': 'Database error'}), 500


# Login user
@users_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        
        email = data.get('email')
        password = data.get('password')
        
        # Validate input
        if not email or not password:
            return jsonify({'error': 'Email and password are required'}), 400
        
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Get user by email
        cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
        user = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        if not user:
            return jsonify({'error': 'Invalid email or password'}), 401
        
        # Check password
        if not check_password(user['password_hash'], password):
            return jsonify({'error': 'Invalid email or password'}), 401
        
        # Create token
        token = create_token(user['id'])
        
        return jsonify({
            'message': 'Login successful',
            'token': token,
            'user': {
                'id': user['id'],
                'username': user['username'],
                'email': user['email']
            }
        }), 200
        
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': 'Database error'}), 500