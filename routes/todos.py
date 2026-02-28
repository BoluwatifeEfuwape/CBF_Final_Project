from flask import Blueprint, request, jsonify
from config import get_db_connection, token_required

todos_bp = Blueprint('todos', __name__)

#we are creating 6 endpoints

#1 Get all todos

@todos_bp.route('', methods=['GET'])
@token_required

def get_todos(user_id):
    # Connect to database
    # Query: SELECT * FROM todos
    # Return JSON list
    try:
        # Get query parameters for filtering
        completed = request.args.get('completed')  # ?completed=true
        priority = request.args.get('priority')    # ?priority=high
        
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Build query dynamically
        query = 'SELECT * FROM todos WHERE user_id = %s'
        params = [user_id]
        
        # if completed is not None:
        #     query += ' AND completed = %s'
        #     params.append(1 if completed.lower() == 'true' else 0)
        
        # if priority:
        #     query += ' AND priority = %s'
        #     params.append(priority)
        
        query += ' ORDER BY created_at DESC'
        
        
        cursor.execute(query, params)
        todos = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return jsonify(todos), 200
        
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': 'Database error'}), 500
    
#2 POST create todo

@todos_bp.route('', methods=['POST'])
@token_required

def create_todo(user_id):
    try:
        data = request.get_json()
        

        title = data.get('title')
        description = data.get('description', '')
        priority = data.get('priority', 'medium')
        due_date = data.get('due_date')
        
        # Validate
        if not user_id:
            return jsonify({'error': 'user_id is required'}), 400
        
        if not title:
            return jsonify({'error': 'Title is required'}), 400
        
        if priority not in ['low', 'medium', 'high']:
            return jsonify({'error': 'Priority must be low, medium, or high'}), 400
        
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Insert todo
        cursor.execute(
            '''INSERT INTO todos (user_id, title, description, priority, due_date) 
               VALUES (%s, %s, %s, %s, %s)''',
            (user_id, title, description, priority, due_date)
        )
        conn.commit()
        
        # Get created todo
        todo_id = cursor.lastrowid
        cursor.execute('SELECT * FROM todos WHERE id = %s', (todo_id,))
        new_todo = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        return jsonify(new_todo), 201
        
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': 'Database error'}), 500
    
#3 GET single todo

@todos_bp.route('/<int:id>', methods=['GET'])
@token_required

def get_todo(user_id, id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute(
            'SELECT * FROM todos WHERE id = %s AND user_id = %s',
            (id, user_id)
        )
        todo = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        if not todo:
            return jsonify({'error': 'Todo not found'}), 404
        
        return jsonify(todo), 200
        
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': 'Database error'}), 500
    
#4 PUT update todo

@todos_bp.route('/<int:id>', methods=['PUT'])
@token_required

def update_todo(user_id, id):
    try:
        data = request.get_json()
        
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Check if todo exists
        cursor.execute(
            'SELECT * FROM todos WHERE id = %s AND user_id = %s',
            (id, user_id)
        )
        existing = cursor.fetchone()
        
        if not existing:
            cursor.close()
            conn.close()
            return jsonify({'error': 'Todo not found'}), 404
        
        # Update todo
        cursor.execute(
            '''UPDATE todos 
               SET title = %s, description = %s, completed = %s, 
                   priority = %s, due_date = %s 
               WHERE id = %s''',
            (data.get('title', existing['title']),
             data.get('description', existing['description']),
             data.get('completed', existing['completed']),
             data.get('priority', existing['priority']),
             data.get('due_date', existing['due_date']),
             id)
        )
        conn.commit()
        
        # Get updated todo
        cursor.execute('SELECT * FROM todos WHERE id = %s', (id,))
        updated_todo = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        return jsonify(updated_todo), 200
        
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': 'Database error'}), 500

#5 PATCH toggle completed

@todos_bp.route('/<int:id>/toggle', methods=['PATCH'])
@token_required

def toggle_todo(user_id, id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Check if exists
        cursor.execute(
            'SELECT * FROM todos WHERE id = %s AND user_id = %s',
            (id, user_id)
        )
        existing = cursor.fetchone()
        
        if not existing:
            cursor.close()
            conn.close()
            return jsonify({'error': 'Todo not found'}), 404
        
        # Toggle completed
        new_status = 0 if existing['completed'] else 1
        cursor.execute(
            'UPDATE todos SET completed = %s WHERE id = %s',
            (new_status, id)
        )
        conn.commit()
        
        # Get updated todo
        cursor.execute('SELECT * FROM todos WHERE id = %s', (id,))
        updated_todo = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        return jsonify(updated_todo), 200
        
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': 'Database error'}), 500


#6 DELETE todo

@todos_bp.route('/<int:id>', methods=['DELETE'])
@token_required

def delete_todo(user_id,id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Check if exists
        cursor.execute(
            'SELECT * FROM todos WHERE id = %s AND user_id = %s',
            (id, user_id)
        )
        existing = cursor.fetchone()
        
        if not existing:
            cursor.close()
            conn.close()
            return jsonify({'error': 'Todo not found'}), 404
        
        # Delete
        cursor.execute('DELETE FROM todos WHERE id = %s', (id,))
        conn.commit()
        
        cursor.close()
        conn.close()
        
        return '', 204
        
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': 'Database error'}), 500