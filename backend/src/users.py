import re
import bcrypt
import sqlite3
from uuid import uuid4
from datetime import datetime


def is_exists(conn, tablename):
    q = f"SELECT name FROM sqlite_master WHERE type='table' AND name='{tablename}'"
    conn.cursor().execute(q)
    exists = conn.cursor().fetchone()
    if exists:
        return True
    else:
        return False


def hash_password(password):
    # Generate a salt and hash the password
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')


def check_password(hashed_password, password):
    # Check if the provided password matches the hashed password
    return bcrypt.checkpw(password.encode('utf-8'),
                          hashed_password.encode('utf-8'))


def is_valid_email(email):
    """
    Check if the given email is a valid email address.

    Args:
        email (str): The email address to be validated.

    Returns:
        bool: True if the email is valid, False otherwise.
    """
    # Regular expression pattern for validating email addresses
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

    # Use re.match() to check if the email matches the pattern
    if re.match(email_pattern, email):
        return True
    else:
        return False


class UserTable:
    def __init__(self):
        try:
            self.conn = sqlite3.connect('backend\\database\\database.db')
            self.cursor = self.conn.cursor()
            print("Connection to database successful.")
        except sqlite3.Error as e:
            print(f"Error connecting to database: {e}")

    def create_table(self):
        query = """
                CREATE TABLE Users (
                    UserID TEXT PRIMARY KEY,
                    Username TEXT NOT NULL UNIQUE,
                    Email TEXT NOT NULL UNIQUE,
                    PasswordHash TEXT NOT NULL,
                    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """

        if not is_exists(conn=self.conn, tablename='users'):
            print('Table exists in DB')
        else:
            self.conn.execute(query)

    def create_user(self, username: str, email: str, password: str):
        hashed_pwd = hash_password(password=password)
        user_id = str(uuid4())

        if is_valid_email(email=email):
            time = datetime.isoformat(datetime.now())
            q = f"INSERT INTO Users (UserID, Username, Email, PasswordHash, CreatedAt) VALUES ('{user_id}', '{username}', '{email}', '{hashed_pwd}', '{time}')"
            self.cursor.execute(q)
            self.conn.commit()
        else:
            print('Invalid Email Address')

    def update_password(self, username: str, new_password: str):
        hashed_pwd = hash_password(password=new_password)
        cursor = self.conn.cursor()
        query = "UPDATE Users SET PasswordHash = ? WHERE Username = ?"
        cursor.execute(query, (hashed_pwd, username))
        self.conn.commit()
        print("Password updated successfully.")

    def is_user(self, username: str = None, email: str = None, password: str= ''):
        if username is None:
            if email is None:
                print('Enater registered email ID or username')
            else:
                query = "SELECT * FROM Users WHERE Email = ?"
                self.cursor.execute(query, (email, ))
                user = self.cursor.fetchall()
        else:
            query = "SELECT * FROM Users WHERE Username = ?"
            self.cursor.execute(query, (username, ))
            user = self.cursor.fetchall()

        if user:
            stored_password_hash = user[0][3]  # Assuming PasswordHash is at index 3
            if check_password(hashed_password=stored_password_hash, password=password):
                print("Authentication successful.")
                return True
            else:
                print("Incorrect password.")
                return False
        else:
            print("User not found.")
            return False
