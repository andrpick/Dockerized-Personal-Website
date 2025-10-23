import sqlite3
import os

class DatabaseAccessLayer:
    def __init__(self, db_name='projects.db'):
        self.db_name = db_name
        self.init_database()
    
    def init_database(self):
        """Initialize the database and create the projects table if it doesn't exist"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        # Create projects table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS projects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT NOT NULL,
                image_filename TEXT NOT NULL,
                created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def get_connection(self):
        """Get a database connection"""
        return sqlite3.connect(self.db_name)
    
    def get_all_projects(self):
        """Retrieve all projects from the database"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM projects ORDER BY created_date DESC')
        projects = cursor.fetchall()
        
        conn.close()
        return projects
    
    def get_project_by_id(self, project_id):
        """Retrieve a specific project by ID"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM projects WHERE id = ?', (project_id,))
        project = cursor.fetchone()
        
        conn.close()
        return project
    
    def add_project(self, title, description, image_filename):
        """Add a new project to the database"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO projects (title, description, image_filename)
            VALUES (?, ?, ?)
        ''', (title, description, image_filename))
        
        project_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return project_id
    
    def update_project(self, project_id, title, description, image_filename):
        """Update an existing project"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE projects 
            SET title = ?, description = ?, image_filename = ?
            WHERE id = ?
        ''', (title, description, image_filename, project_id))
        
        conn.commit()
        conn.close()
    
    def delete_project(self, project_id):
        """Delete a project from the database"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM projects WHERE id = ?', (project_id,))
        
        conn.commit()
        conn.close()
    
    def project_exists(self, project_id):
        """Check if a project exists by ID"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) FROM projects WHERE id = ?', (project_id,))
        count = cursor.fetchone()[0]
        
        conn.close()
        return count > 0
