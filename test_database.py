"""
Comprehensive database testing for the Flask personal website.
Tests the Database Access Layer (DAL) functionality.
"""
import pytest
import os
import tempfile
from DAL import DatabaseAccessLayer

class TestDatabaseInitialization:
    """Test database initialization and setup."""
    
    def test_database_creation(self, test_db):
        """Test that database is created successfully."""
        assert test_db is not None
        assert hasattr(test_db, 'db_name')
        assert os.path.exists(test_db.db_name)
    
    def test_table_creation(self, test_db):
        """Test that projects table is created."""
        # Try to get all projects (should return empty list, not error)
        projects = test_db.get_all_projects()
        assert isinstance(projects, list)
        assert len(projects) == 0

class TestProjectCRUD:
    """Test Create, Read, Update, Delete operations for projects."""
    
    def test_add_single_project(self, test_db, sample_project_data):
        """Test adding a single project."""
        project_id = test_db.add_project(
            sample_project_data['title'],
            sample_project_data['description'],
            sample_project_data['image_filename']
        )
        
        assert project_id is not None
        assert isinstance(project_id, int)
        assert project_id > 0
    
    def test_get_all_projects_empty(self, test_db):
        """Test getting all projects when database is empty."""
        projects = test_db.get_all_projects()
        assert isinstance(projects, list)
        assert len(projects) == 0
    
    def test_get_all_projects_with_data(self, test_db, multiple_projects_data):
        """Test getting all projects when database has data."""
        # Add multiple projects
        for project_data in multiple_projects_data:
            test_db.add_project(
                project_data['title'],
                project_data['description'],
                project_data['image_filename']
            )
        
        projects = test_db.get_all_projects()
        assert len(projects) == len(multiple_projects_data)
        
        # Check that projects are ordered by created_date DESC
        for i, project in enumerate(projects):
            assert len(project) == 5  # id, title, description, image_filename, created_date
            assert project[1] in [p['title'] for p in multiple_projects_data]
    
    def test_get_project_by_id(self, test_db, sample_project_data):
        """Test retrieving a project by ID."""
        project_id = test_db.add_project(
            sample_project_data['title'],
            sample_project_data['description'],
            sample_project_data['image_filename']
        )
        
        project = test_db.get_project_by_id(project_id)
        assert project is not None
        assert project[0] == project_id
        assert project[1] == sample_project_data['title']
        assert project[2] == sample_project_data['description']
        assert project[3] == sample_project_data['image_filename']
    
    def test_get_nonexistent_project(self, test_db):
        """Test retrieving a project that doesn't exist."""
        project = test_db.get_project_by_id(999)
        assert project is None
    
    def test_update_project(self, test_db, sample_project_data):
        """Test updating a project."""
        project_id = test_db.add_project(
            sample_project_data['title'],
            sample_project_data['description'],
            sample_project_data['image_filename']
        )
        
        # Update the project
        new_title = "Updated Title"
        new_description = "Updated Description"
        new_image = "updated.jpg"
        
        test_db.update_project(project_id, new_title, new_description, new_image)
        
        # Verify the update
        project = test_db.get_project_by_id(project_id)
        assert project[1] == new_title
        assert project[2] == new_description
        assert project[3] == new_image
    
    def test_delete_project(self, test_db, sample_project_data):
        """Test deleting a project."""
        project_id = test_db.add_project(
            sample_project_data['title'],
            sample_project_data['description'],
            sample_project_data['image_filename']
        )
        
        # Verify project exists
        assert test_db.project_exists(project_id) == True
        
        # Delete the project
        test_db.delete_project(project_id)
        
        # Verify project is deleted
        assert test_db.project_exists(project_id) == False
        project = test_db.get_project_by_id(project_id)
        assert project is None
    
    def test_delete_nonexistent_project(self, test_db):
        """Test deleting a project that doesn't exist."""
        # Should not raise an error
        test_db.delete_project(999)

class TestProjectExists:
    """Test project existence checking."""
    
    def test_project_exists_true(self, test_db, sample_project_data):
        """Test project_exists returns True for existing project."""
        project_id = test_db.add_project(
            sample_project_data['title'],
            sample_project_data['description'],
            sample_project_data['image_filename']
        )
        
        assert test_db.project_exists(project_id) == True
    
    def test_project_exists_false(self, test_db):
        """Test project_exists returns False for non-existing project."""
        assert test_db.project_exists(999) == False
    
    def test_project_exists_after_deletion(self, test_db, sample_project_data):
        """Test project_exists returns False after deletion."""
        project_id = test_db.add_project(
            sample_project_data['title'],
            sample_project_data['description'],
            sample_project_data['image_filename']
        )
        
        assert test_db.project_exists(project_id) == True
        
        test_db.delete_project(project_id)
        assert test_db.project_exists(project_id) == False

class TestDatabaseConstraints:
    """Test database constraints and edge cases."""
    
    def test_empty_string_values(self, test_db):
        """Test handling of empty string values."""
        project_id = test_db.add_project("", "", "")
        assert project_id is not None
        
        project = test_db.get_project_by_id(project_id)
        assert project[1] == ""
        assert project[2] == ""
        assert project[3] == ""
    
    def test_long_string_values(self, test_db):
        """Test handling of long string values."""
        long_title = "A" * 1000
        long_description = "B" * 5000
        long_filename = "C" * 500
        
        project_id = test_db.add_project(long_title, long_description, long_filename)
        assert project_id is not None
        
        project = test_db.get_project_by_id(project_id)
        assert project[1] == long_title
        assert project[2] == long_description
        assert project[3] == long_filename
    
    def test_special_characters(self, test_db):
        """Test handling of special characters."""
        special_title = "Project with Special Chars: !@#$%^&*()_+-=[]{}|;':\",./<>?"
        special_description = "Description with\nnewlines\tand\ttabs"
        special_filename = "file with spaces & symbols.jpg"
        
        project_id = test_db.add_project(special_title, special_description, special_filename)
        assert project_id is not None
        
        project = test_db.get_project_by_id(project_id)
        assert project[1] == special_title
        assert project[2] == special_description
        assert project[3] == special_filename

class TestDatabaseTransactions:
    """Test database transaction handling."""
    
    def test_multiple_operations(self, test_db, multiple_projects_data):
        """Test multiple database operations in sequence."""
        # Add multiple projects
        project_ids = []
        for project_data in multiple_projects_data:
            project_id = test_db.add_project(
                project_data['title'],
                project_data['description'],
                project_data['image_filename']
            )
            project_ids.append(project_id)
        
        # Verify all projects exist
        for project_id in project_ids:
            assert test_db.project_exists(project_id) == True
        
        # Update all projects
        for i, project_id in enumerate(project_ids):
            test_db.update_project(
                project_id,
                f"Updated {multiple_projects_data[i]['title']}",
                f"Updated {multiple_projects_data[i]['description']}",
                f"updated_{multiple_projects_data[i]['image_filename']}"
            )
        
        # Verify updates
        for i, project_id in enumerate(project_ids):
            project = test_db.get_project_by_id(project_id)
            assert project[1] == f"Updated {multiple_projects_data[i]['title']}"
            assert project[2] == f"Updated {multiple_projects_data[i]['description']}"
        
        # Delete all projects
        for project_id in project_ids:
            test_db.delete_project(project_id)
            assert test_db.project_exists(project_id) == False
        
        # Verify database is empty
        projects = test_db.get_all_projects()
        assert len(projects) == 0

class TestDatabaseConnection:
    """Test database connection handling."""
    
    def test_connection_creation(self, test_db):
        """Test that database connections are created properly."""
        connection = test_db.get_connection()
        assert connection is not None
        
        # Test that connection can execute queries
        cursor = connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM projects")
        count = cursor.fetchone()[0]
        assert isinstance(count, int)
        
        connection.close()
    
    def test_multiple_connections(self, test_db):
        """Test multiple database connections."""
        conn1 = test_db.get_connection()
        conn2 = test_db.get_connection()
        
        assert conn1 is not None
        assert conn2 is not None
        assert conn1 != conn2
        
        conn1.close()
        conn2.close()

@pytest.mark.integration
class TestDatabaseIntegration:
    """Integration tests for database functionality."""
    
    def test_full_workflow(self, test_db):
        """Test complete workflow: create, read, update, delete."""
        # Create
        project_id = test_db.add_project("Workflow Test", "Testing full workflow", "workflow.jpg")
        assert project_id is not None
        
        # Read
        project = test_db.get_project_by_id(project_id)
        assert project[1] == "Workflow Test"
        
        # Update
        test_db.update_project(project_id, "Updated Workflow", "Updated description", "updated.jpg")
        updated_project = test_db.get_project_by_id(project_id)
        assert updated_project[1] == "Updated Workflow"
        
        # Delete
        test_db.delete_project(project_id)
        assert test_db.project_exists(project_id) == False
    
    def test_concurrent_operations(self, test_db):
        """Test concurrent database operations."""
        # Add multiple projects concurrently (simulated)
        project_ids = []
        for i in range(5):
            project_id = test_db.add_project(f"Concurrent Project {i}", f"Description {i}", f"image{i}.jpg")
            project_ids.append(project_id)
        
        # Verify all projects were created
        projects = test_db.get_all_projects()
        assert len(projects) == 5
        
        # Clean up
        for project_id in project_ids:
            test_db.delete_project(project_id)
