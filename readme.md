# Todo List API

A RESTful API built with Flask and MySQL for managing personal todo lists with user authentication.

## Features

- 🔐 **User Authentication** - Secure registration and login with JWT tokens
- ✅ **CRUD Operations** - Create, read, update, and delete todos
- 🔒 **Protected Routes** - User-specific data access
- 🏷️ **Priority Levels** - Organize todos by low, medium, or high priority
- 📅 **Due Dates** - Set deadlines for tasks
- 🔍 **Filtering** - Filter todos by completion status and priority
- 🔄 **Toggle Complete** - Quick endpoint to mark todos as done/undone

## Tech Stack

- **Backend:** Flask (Python)
- **Database:** MySQL
- **Authentication:** JWT (JSON Web Tokens)
- **Password Hashing:** bcrypt
- **API Testing:** Postman/curl

## Project Structure
```
todo-api/
├── app.py                 # Main application file
├── config.py              # Database connection and helper functions
├── todo_database_setup.py            # Database setup script
├── requirements.txt       # Python dependencies
└── routes/
│   ├── __init__.py
│   ├── todos.py           # Todo endpoints
│   └── users.py           # Authentication endpoints
└── services/
│   ├── db_config_service.py           # Base service class used by other services
│    ├── todo_service.py   # Handles all business logic related to Todos
│    └── user_service.py   #Handles all business logic related to Users        
```

## Database Schema

### Users Table
```sql
- id (INT, PRIMARY KEY, AUTO_INCREMENT)
- username (VARCHAR, UNIQUE)
- email (VARCHAR, UNIQUE)
- password_hash (VARCHAR)
- created_at (TIMESTAMP)
```

### Todos Table
```sql
- id (INT, PRIMARY KEY, AUTO_INCREMENT)
- user_id (INT, FOREIGN KEY)
- title (VARCHAR)
- description (TEXT)
- completed (BOOLEAN)
- priority (ENUM: 'low', 'medium', 'high')
- due_date (DATE)
- created_at (TIMESTAMP)
- updated_at (TIMESTAMP)
```

## Installation

### Prerequisites
- Python 3.8+
- MySQL 8.0+
- pip

### Setup

1. **Create virtual environment**
```bash
python -m venv venv

# Activate virtual environment
# On Mac/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Configure MySQL**

Update `config.py` with your MySQL credentials:
```python
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="your_password",  # Change this
        database="todo_api_db"
    )
```

4. **Set up database**
```bash
python todo_database_setup.py
```

5. **Run the application**
```bash
flask --app your_app_name run --debug
```

The API will be available at `http://127.0.0.1:5000`

## API Endpoints

### Authentication

#### Register User
```http
POST /api/users/register
Content-Type: application/json

{
  "username": "johndoe",
  "email": "john@example.com",
  "password": "securepassword123"
}
```

**Response:**
```json
{
  "message": "User registered successfully",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com"
  }
}
```

#### Login User
```http
POST /api/users/login
Content-Type: application/json

{
  "email": "john@example.com",
  "password": "securepassword123"
}
```

### Todos (All require authentication)

#### Get All Todos
```http
GET /api/todos
Authorization: Bearer <token>
```

**Query Parameters:**
- `?completed=true` - Filter by completion status
- `?priority=high` - Filter by priority

#### Get Single Todo
```http
GET /api/todos/:id
Authorization: Bearer <token>
```

#### Create Todo
```http
POST /api/todos
Authorization: Bearer <token>
Content-Type: application/json

{
  "title": "Finish project",
  "description": "Complete Todo API",
  "priority": "high",
  "due_date": "2025-03-15"
}
```

#### Update Todo
```http
PUT /api/todos/:id
Authorization: Bearer <token>
Content-Type: application/json

{
  "title": "Updated title",
  "completed": true,
  "priority": "medium"
}
```

#### Toggle Todo Completion
```http
PATCH /api/todos/:id/toggle
Authorization: Bearer <token>
```

#### Delete Todo
```http
DELETE /api/todos/:id
Authorization: Bearer <token>
```

## Usage Examples

### Using curl

**Register:**
```bash
curl -X POST http://127.0.0.1:5000/api/users/register \
  -H "Content-Type: application/json" \
  -d '{"username":"johndoe","email":"john@example.com","password":"password123"}'
```

**Create Todo:**
```bash
curl -X POST http://127.0.0.1:5000/api/todos \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -d '{"title":"Buy groceries","priority":"high","due_date":"2025-03-01"}'
```

**Get All Todos:**
```bash
curl http://127.0.0.1:5000/api/todos \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

## Security Features

- ✅ Passwords are hashed using bcrypt
- ✅ JWT tokens for authentication
- ✅ Tokens expire after 7 days
- ✅ User-specific data access
- ✅ SQL injection prevention
- ✅ Protected routes

## Error Handling

HTTP Status Codes:
- `200 OK` - Successful GET/PUT/PATCH
- `201 Created` - Successful POST
- `204 No Content` - Successful DELETE
- `400 Bad Request` - Invalid input
- `401 Unauthorized` - Missing/invalid token
- `404 Not Found` - Resource not found
- `500 Internal Server Error` - Server error

## Future Enhancements

- [ ] Add categories/tags for todos
- [ ] Implement search functionality
- [ ] Add pagination
- [ ] Todo sharing between users
- [ ] Email notifications for due dates
- [ ] Recurring todos
- [ ] Statistics/analytics endpoint

## Author

**Boluwatife Efuwape**
- GitHub: [BoluwatifeEfuwape](https://github.com/BoluwatifeEfuwape)
- Email: boluefu@gmail.com

## Acknowledgments

- Built as a bootcamp final project
- Flask and Python communities

---

⭐ If you found this project helpful, please give it a star!
