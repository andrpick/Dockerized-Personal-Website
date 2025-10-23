"""
Pytest configuration and fixtures for the Flask personal website tests.
"""
import pytest
import os
import tempfile
import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from app import app
from DAL import DatabaseAccessLayer

@pytest.fixture(scope='session')
def app_config():
    """Application configuration for testing."""
    return {
        'TESTING': True,
        'WTF_CSRF_ENABLED': False,
        'SECRET_KEY': 'test-secret-key'
    }

@pytest.fixture
def test_app(app_config):
    """Create a test Flask application."""
    app.config.update(app_config)
    return app

@pytest.fixture
def client(test_app):
    """Create a test client for the Flask application."""
    with test_app.test_client() as client:
        yield client

@pytest.fixture
def test_db():
    """Create a temporary database for testing."""
    # Create a temporary database file
    db_fd, db_path = tempfile.mkstemp(suffix='.db')
    
    try:
        # Create a new DAL instance for testing
        test_dal = DatabaseAccessLayer(db_path)
        yield test_dal
    finally:
        # Clean up
        os.close(db_fd)
        if os.path.exists(db_path):
            os.unlink(db_path)

@pytest.fixture
def sample_project_data():
    """Sample project data for testing."""
    return {
        'title': 'Test Project',
        'description': 'This is a test project for unit testing',
        'image_filename': 'test-project.jpg'
    }

@pytest.fixture
def multiple_projects_data():
    """Multiple sample projects for testing."""
    return [
        {
            'title': 'Project 1',
            'description': 'First test project',
            'image_filename': 'project1.jpg'
        },
        {
            'title': 'Project 2',
            'description': 'Second test project',
            'image_filename': 'project2.jpg'
        },
        {
            'title': 'Project 3',
            'description': 'Third test project',
            'image_filename': 'project3.jpg'
        }
    ]

@pytest.fixture
def populated_test_db(test_db, multiple_projects_data):
    """Create a test database with sample projects."""
    for project_data in multiple_projects_data:
        test_db.add_project(
            project_data['title'],
            project_data['description'],
            project_data['image_filename']
        )
    return test_db

# Pytest configuration
def pytest_configure(config):
    """Configure pytest with custom settings."""
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests"
    )
    config.addinivalue_line(
        "markers", "unit: marks tests as unit tests"
    )

def pytest_collection_modifyitems(config, items):
    """Modify test collection to add markers automatically."""
    for item in items:
        # Add unit marker to all tests by default
        if not any(marker.name in ['integration', 'slow'] for marker in item.iter_markers()):
            item.add_marker(pytest.mark.unit)
        
        # Mark database tests as integration tests
        if 'test_db' in item.fixturenames or 'DatabaseAccessLayer' in item.name:
            item.add_marker(pytest.mark.integration)
