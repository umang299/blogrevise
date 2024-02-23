import yaml
import sqlite3
from uuid import uuid4
from datetime import datetime


def load_yaml_file(file_path):
    """
    Load data from a YAML file.

    Parameters:
        file_path (str): The path to the YAML file.

    Returns:
        dict: The data loaded from the YAML file.
    """
    try:
        with open(file_path, 'r') as file:
            data = yaml.safe_load(file)
        return data
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
        return None
    except Exception as e:
        print(f"Error occurred while loading YAML file: {e}")
        return None


class BlogOutline:
    def __init__(self) -> None:
        try:
            self.conn = sqlite3.connect('backend\\database\\database.db')
            self.cursor = self.conn.cursor()
            print("Connection to database successful.")

            self.config = load_yaml_file(file_path='backend\\config.yaml')
            self.outline_db_name = self.config['database']['outline']['tablename']
            self.outline_category_db_name = self.config['database']['outline']['categoryname']

        except sqlite3.Error as e:
            print(f"Error connecting to database: {e}")

    def create_outline_table(self):
        self.cursor.execute(f"""
                SELECT name FROM sqlite_master WHERE type='table'
                AND name='{self.outline_db_name}'""")

        table_exists = self.cursor.fetchone()

        if table_exists:
            print(f"Table '{self.outline_db_name}' already exists.")
        else:
            self.cursor.execute(f"""
                CREATE TABLE {self.outline_db_name} (
                    OutlineID INTEGER PRIMARY KEY AUTOINCREMENT,
                    UserID INTEGER,
                    Title TEXT,
                    Topic TEXT,
                    Instructions TEXT,
                    Filename TEXT,
                    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    IsUploaded BOOLEAN,
                    Version INTEGER,
                    CategoryID INTEGER,
                    FOREIGN KEY (UserID) REFERENCES Users(UserID),
                    FOREIGN KEY (CategoryID) REFERENCES Categories(CategoryID)
                )
            """)
            print(f"Table '{self.outline_db_name}' created successfully.")

    def create_category_table(self):
        self.cursor.execute(f"""
                SELECT name FROM sqlite_master WHERE type='table'
                AND name='{self.outline_category_db_name}'""")
        table_exists = self.cursor.fetchone()

        if table_exists:
            print(f"Table '{self.outline_category_db_name}' already exists.")
        else:
            self.cursor.execute(f"""
                CREATE TABLE {self.outline_category_db_name} (
                    CategoryID INTEGER PRIMARY KEY AUTOINCREMENT,
                    Name TEXT
                );
            """)
            print(f"Table '{self.outline_category_db_name}' \
                  created successfully.")

    def upload_blog_data(self, blog_data):
        try:
            self.cursor.execute("""
                INSERT INTO BlogOutlines
                (UserID, Title, Topic, Instructions,
                Filename, IsUploaded, Version, CategoryID)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                blog_data['UserID'], blog_data['Title'], blog_data['Topic'],
                blog_data['Instructions'], blog_data['Filename'],
                blog_data['IsUploaded'], blog_data['Version'],
                blog_data['CategoryID'])
                )

            self.conn.commit()
            print("Blog data uploaded successfully!")
        except sqlite3.Error as e:
            print("Error uploading blog data:", e)

    def get_outline_filenames_by_user_id(self, user_id):
        self.cursor.execute("""
                SELECT Filename FROM BlogOutlines WHERE UserID = ?
                """, (user_id,))
        rows = self.cursor.fetchall()
        filenames = [row[0] for row in rows]
        return filenames
