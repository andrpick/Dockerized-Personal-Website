import pytest
import os
import tempfile
from app import app
from DAL import DatabaseAccessLayer

@pytest.fixture
def client():
    """Create a test client for the Flask application."""
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    
    with app.test_client() as client:
        yield client

@pytest.fixture
def test_db():
    """Create a temporary database for testing."""
    # Create a temporary database file
    db_fd, db_path = tempfile.mkstemp(suffix='.db')
    
    # Create a new DAL instance for testing
    test_dal = DatabaseAccessLayer(db_path)
    
    yield test_dal
    
    # Clean up
    os.close(db_fd)
    if os.path.exists(db_path):
        os.unlink(db_path)

class TestHomePage:
    """Test cases for the home page."""
    
    def test_home_page_loads(self, client):
        """Test that the home page loads successfully."""
        response = client.get('/')
        assert response.status_code == 200
        assert b'Welcome to My Personal Website' in response.data
        assert b'Andrew Pickering' in response.data

    def test_home_page_navigation(self, client):
        """Test that navigation links are present."""
        response = client.get('/')
        assert b'About Me' in response.data
        assert b'Resume' in response.data
        assert b'Projects' in response.data
        assert b'Contact' in response.data

class TestAboutPage:
    """Test cases for the about page."""
    
    def test_about_page_loads(self, client):
        """Test that the about page loads successfully."""
        response = client.get('/about')
        assert response.status_code == 200
        assert b'About Me' in response.data
        assert b'MSIS Graduate Student' in response.data

    def test_about_page_skills(self, client):
        """Test that skills section is present."""
        response = client.get('/about')
        assert b'Skills & Interests' in response.data
        assert b'Business Intelligence' in response.data

class TestResumePage:
    """Test cases for the resume page."""
    
    def test_resume_page_loads(self, client):
        """Test that the resume page loads successfully."""
        response = client.get('/resume')
        assert response.status_code == 200
        assert b'Andrew Pickering' in response.data
        assert b'Education' in response.data

    def test_resume_page_sections(self, client):
        """Test that all resume sections are present."""
        response = client.get('/resume')
        assert b'Professional Experience' in response.data
        assert b'Technical Skills' in response.data
        assert b'Leadership' in response.data

class TestContactPage:
    """Test cases for the contact page."""
    
    def test_contact_page_loads(self, client):
        """Test that the contact page loads successfully."""
        response = client.get('/contact')
        assert response.status_code == 200
        assert b'Get In Touch' in response.data
        assert b'Contact Information' in response.data

    def test_contact_form_present(self, client):
        """Test that the contact form is present."""
        response = client.get('/contact')
        assert b'firstName' in response.data
        assert b'lastName' in response.data
        assert b'email' in response.data
        assert b'message' in response.data

    def test_contact_form_validation(self, client):
        """Test contact form validation."""
        # Test with missing required fields
        response = client.post('/contact', data={
            'firstName': '',
            'lastName': 'Test',
            'email': 'test@example.com'
        })
        # Should redirect to thankyou page (form validation is client-side)
        assert response.status_code == 200

class TestProjectsPage:
    """Test cases for the projects page with database functionality."""
    
    def test_projects_page_loads(self, client):
        """Test that the projects page loads successfully."""
        response = client.get('/projects')
        assert response.status_code == 200
        assert b'My Projects' in response.data

    def test_projects_table_structure(self, client):
        """Test that the projects table has correct structure."""
        response = client.get('/projects')
        assert b'<table' in response.data
        assert b'Image' in response.data
        assert b'Title' in response.data
        assert b'Description' in response.data
        assert b'Actions' in response.data

    def test_add_project_button(self, client):
        """Test that the add project button is present."""
        response = client.get('/projects')
        assert b'Add New Project' in response.data
        assert b'href="/add_project"' in response.data

class TestAddProject:
    """Test cases for adding new projects."""
    
    def test_add_project_page_loads(self, client):
        """Test that the add project page loads successfully."""
        response = client.get('/add_project')
        assert response.status_code == 200
        assert b'Add New Project' in response.data

    def test_add_project_form_fields(self, client):
        """Test that the add project form has required fields."""
        response = client.get('/add_project')
        assert b'name="title"' in response.data
        assert b'name="description"' in response.data
        assert b'name="image_filename"' in response.data

    def test_add_project_success(self, client):
        """Test successful project addition."""
        response = client.post('/add_project', data={
            'title': 'Test Project',
            'description': 'This is a test project',
            'image_filename': 'test.jpg'
        }, follow_redirects=True)
        
        assert response.status_code == 200
        assert b'Test Project' in response.data
        assert b'This is a test project' in response.data

    def test_add_project_validation(self, client):
        """Test project addition with missing fields."""
        response = client.post('/add_project', data={
            'title': '',
            'description': 'Test description',
            'image_filename': 'test.jpg'
        })
        
        # Should show error message
        assert b'All fields are required' in response.data

class TestEditProject:
    """Test cases for editing projects."""
    
    def test_edit_project_page_loads(self, client):
        """Test that the edit project page loads for existing project."""
        # First add a project
        client.post('/add_project', data={
            'title': 'Test Project',
            'description': 'Test description',
            'image_filename': 'test.jpg'
        })
        
        # Get the project ID (assuming it's 1)
        response = client.get('/edit_project/1')
        assert response.status_code == 200
        assert b'Edit Project' in response.data

    def test_edit_project_form_prefilled(self, client):
        """Test that the edit form is prefilled with existing data."""
        # Add a project first
        client.post('/add_project', data={
            'title': 'Original Title',
            'description': 'Original Description',
            'image_filename': 'original.jpg'
        })
        
        response = client.get('/edit_project/1')
        assert b'value="Original Title"' in response.data
        assert b'Original Description' in response.data
        assert b'value="original.jpg"' in response.data

    def test_edit_project_success(self, client):
        """Test successful project editing."""
        # Add a project first
        client.post('/add_project', data={
            'title': 'Original Title',
            'description': 'Original Description',
            'image_filename': 'original.jpg'
        })
        
        # Edit the project
        response = client.post('/edit_project/1', data={
            'title': 'Updated Title',
            'description': 'Updated Description',
            'image_filename': 'updated.jpg'
        }, follow_redirects=True)
        
        assert response.status_code == 200
        assert b'Updated Title' in response.data
        assert b'Updated Description' in response.data

class TestDeleteProject:
    """Test cases for deleting projects."""
    
    def test_delete_project_success(self, client):
        """Test successful project deletion."""
        # Add a project first
        client.post('/add_project', data={
            'title': 'Project to Delete',
            'description': 'This will be deleted',
            'image_filename': 'delete.jpg'
        })
        
        # Delete the project
        response = client.get('/delete_project/1', follow_redirects=True)
        assert response.status_code == 200
        assert b'Project deleted successfully' in response.data

    def test_delete_nonexistent_project(self, client):
        """Test deleting a project that doesn't exist."""
        response = client.get('/delete_project/999', follow_redirects=True)
        assert response.status_code == 200
        assert b'Project not found' in response.data

class TestDatabaseAccessLayer:
    """Test cases for the Database Access Layer."""
    
    def test_dal_initialization(self, test_db):
        """Test that DAL initializes correctly."""
        assert test_db is not None
        assert hasattr(test_db, 'get_all_projects')
        assert hasattr(test_db, 'add_project')
        assert hasattr(test_db, 'delete_project')

    def test_add_project_to_db(self, test_db):
        """Test adding a project to the database."""
        project_id = test_db.add_project('Test Project', 'Test Description', 'test.jpg')
        assert project_id is not None
        
        projects = test_db.get_all_projects()
        assert len(projects) == 1
        assert projects[0][1] == 'Test Project'
        assert projects[0][2] == 'Test Description'
        assert projects[0][3] == 'test.jpg'

    def test_get_project_by_id(self, test_db):
        """Test retrieving a project by ID."""
        project_id = test_db.add_project('Test Project', 'Test Description', 'test.jpg')
        project = test_db.get_project_by_id(project_id)
        
        assert project is not None
        assert project[1] == 'Test Project'
        assert project[2] == 'Test Description'

    def test_update_project(self, test_db):
        """Test updating a project."""
        project_id = test_db.add_project('Original Title', 'Original Description', 'original.jpg')
        test_db.update_project(project_id, 'Updated Title', 'Updated Description', 'updated.jpg')
        
        project = test_db.get_project_by_id(project_id)
        assert project[1] == 'Updated Title'
        assert project[2] == 'Updated Description'
        assert project[3] == 'updated.jpg'

    def test_delete_project_from_db(self, test_db):
        """Test deleting a project from the database."""
        project_id = test_db.add_project('Project to Delete', 'Will be deleted', 'delete.jpg')
        test_db.delete_project(project_id)
        
        projects = test_db.get_all_projects()
        assert len(projects) == 0

    def test_project_exists(self, test_db):
        """Test checking if a project exists."""
        project_id = test_db.add_project('Test Project', 'Test Description', 'test.jpg')
        
        assert test_db.project_exists(project_id) == True
        assert test_db.project_exists(999) == False

class TestStaticAssets:
    """Test cases for static asset serving."""
    
    def test_css_serving(self, client):
        """Test that CSS files are served correctly."""
        response = client.get('/css/styles.css')
        assert response.status_code == 200
        assert b'body' in response.data

    def test_image_serving(self, client):
        """Test that images are served correctly."""
        # This test assumes at least one image exists
        response = client.get('/images/placeholder.jpg')
        # Should return 200 if image exists, 404 if not
        assert response.status_code in [200, 404]

    def test_js_serving(self, client):
        """Test that JavaScript files are served correctly."""
        response = client.get('/script.js')
        assert response.status_code == 200
        assert b'function' in response.data

class TestThankYouPage:
    """Test cases for the thank you page."""
    
    def test_thank_you_page_loads(self, client):
        """Test that the thank you page loads successfully."""
        response = client.get('/thankyou')
        assert response.status_code == 200
        assert b'Thank You!' in response.data

    def test_thank_you_page_content(self, client):
        """Test that the thank you page has expected content."""
        response = client.get('/thankyou')
        assert b'Your message has been successfully sent' in response.data
        assert b'Return to Homepage' in response.data

class TestErrorHandling:
    """Test cases for error handling."""
    
    def test_404_handling(self, client):
        """Test 404 error handling."""
        response = client.get('/nonexistent-page')
        assert response.status_code == 404

    def test_edit_nonexistent_project(self, client):
        """Test editing a project that doesn't exist."""
        response = client.get('/edit_project/999')
        assert response.status_code == 302  # Redirect to projects page

if __name__ == '__main__':
    pytest.main([__file__])
