import mysql.connector

def get_connection():
    # ⚠️ IMPORTANT: Replace 'password' with YOUR MySQL password
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="password123"  # ← CHANGE THIS!
    )

def setup_todo_db(cursor):
    print("📱 Creating 'todo_api' database...")
    cursor.execute("CREATE DATABASE IF NOT EXISTS todo_api_db")
    cursor.execute("USE todo_api_db")


    # Create Users Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INT PRIMARY KEY AUTO_INCREMENT,
        username VARCHAR(50) UNIQUE NOT NULL,
        email VARCHAR(100) UNIQUE NOT NULL,
        password_hash VARCHAR(255) NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP         
    )""")

    # Insert test user(s)
    Users = [
        ('boluefuwape', 'boluefu@gmail.com', 'temppassword'),
    ]

    cursor.executemany(
        "INSERT IGNORE INTO users (username, email, password_hash) VALUES (%s, %s, %s)",
        Users
    )

    user_id = cursor.lastrowid
    print(user_id)


    # Create todos table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS todos (
        id INTEGER PRIMARY KEY AUTO_INCREMENT,
        user_id INT NOT NULL,
        title VARCHAR(200) NOT NULL,
        description TEXT,
        completed BOOLEAN DEFAULT 0,
        priority ENUM('low', 'medium', 'high') DEFAULT 'medium',
        due_date DATE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    )''')


    # insert test todos

    cursor.execute("""
    INSERT IGNORE INTO todos (id, user_id, title, description, priority, due_date) 
    VALUES 
    (1, %s, 'Buy groceries', 'Milk, eggs, bread', 'medium', '2025-02-28'),
    (2, %s, 'Finish bootcamp project', 'Build todo API', 'high', '2026-02-28'),
    (3, %s, 'Job Applications', 'Apply for 50 jobs', 'high', '2026-03-31')
    """, (user_id,user_id, user_id))


def main():
    print("\n" + "="*60)
    print("  PYTHON & MySQL COURSE - DATABASE SETUP")
    print("="*60 + "\n")
    
    try:
        print("🔌 Connecting to MySQL...")
        conn = get_connection()
        cursor = conn.cursor()
        print("   ✅ Connected successfully!\n")
        
        setup_todo_db(cursor)
    
        conn.commit()
        
        print("\n" + "="*60)
        print("  ✅ SUCCESS! Databases created successfully!")
        print("="*60)
        
        
    except mysql.connector.Error as err:
        print(f"\n❌ ERROR: {err}")
        print("\n🔧 TROUBLESHOOTING:")
        print("   1. Is MySQL Server running?")
        print("   2. Did you change 'password' to your actual MySQL password?")
        print("   3. Try running: mysql -u root -p")
        
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()
            print("🔌 Connection closed.\n")

if __name__ == "__main__":
    main()