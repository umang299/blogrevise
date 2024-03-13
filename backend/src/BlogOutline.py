import os
import sys
import yaml
import openai
import sqlite3
from uuid import uuid4
from datetime import datetime


api_key = os.environ['OPENAI_API_KEY']
openai.api_key = api_key

cwd = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(cwd)

from .utils import (load_yaml_file, read_text_file)


class BlogOutline:
    def __init__(self) -> None:
        self.db_path = os.path.join(cwd, 'database', 'database.db')
        self.config = load_yaml_file(
                    file_path=os.path.join(
                                cwd, 'config.yaml'
                                )
                    )
        self.outline_db_name = self.config['database']['outline']['tablename']
        self.outline_category_db_name = self.config['database']['outline']['categoryname']

    def create_outline_table(self):
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        print("Connection to database successful.")

        cur.execute(f"""
                SELECT name FROM sqlite_master WHERE type='table'
                AND name='{self.outline_db_name}'""")

        table_exists = cur.fetchone()

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

        conn.close()

    def create_category_table(self):
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        print("Connection to database successful.")

        cur.execute(f"""
                SELECT name FROM sqlite_master WHERE type='table'
                AND name='{self.outline_category_db_name}'""")
        table_exists = cur.fetchone()

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

        conn.close()

    def upload_blog_data(self, blog_data):
        try:
            conn = sqlite3.connect(self.db_path)
            cur = conn.cursor()
            print("Connection to database successful.")

            cur.execute("""
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

            conn.commit()
            conn.close()
            print("Blog data uploaded successfully!")
        except sqlite3.Error as e:
            print("Error uploading blog data:", e)

    def get_outline_filenames_by_user_id(self, user_id):
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        # print("Connection to database successful.")
        cur.execute("""
                SELECT Filename FROM BlogOutlines WHERE UserID = ?
                """, (user_id,))
        rows = cur.fetchall()
        filenames = [row[0] for row in rows]

        conn.close()
        return filenames

    def generate_outline(self, topic, instructions):
        prompt_template = read_text_file(
                            file_path=os.path.join(
                                        cwd, 'prompts', 'blog_outline.txt'))
        prompt = prompt_template.replace('<<TOPIC>>', topic)
        prompt = prompt_template.replace('<<INSTRUCTIONS>>', instructions)
        response = openai.chat.completions.create(
                            messages=[{'role' : 'user', 'content' : prompt}],
                            model='gpt-4',
                            temperature=2)

        return response.choices[0].message.content
