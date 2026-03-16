from database.db import get_db_connection
from database.auth_utils import get_password_hash, verify_password
from typing import Optional


def get_user_by_username(username: str):
    """Get user by username"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
    
    conn.close()
    return dict(user) if user else None


def get_user_by_email(email: str):
    """Get user by email"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    user = cursor.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
    
    conn.close()
    return dict(user) if user else None


def create_user(username: str, email: str, password: str, full_name: Optional[str] = None):
    """Create a new user"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    hashed_password = get_password_hash(password)
    
    try:
        cursor.execute(
            "INSERT INTO users (username, email, hashed_password, full_name) VALUES (?, ?, ?, ?)",
            (username, email, hashed_password, full_name)
        )
        conn.commit()
        user_id = cursor.lastrowid
        
        # Get the created user
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        user = cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
        
        conn.close()
        return dict(user) if user else None
    except Exception as e:
        conn.close()
        raise e


def authenticate_user(username: str, password: str):
    """Authenticate a user"""
    user = get_user_by_username(username)
    
    if not user:
        return False
    
    if not verify_password(password, user["hashed_password"]):
        return False
    
    return user
