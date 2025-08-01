import pytest
import os
import tempfile
from app import app, init_db


@pytest.fixture
def client():
    # Create a temporary database for testing
    db_fd, temp_db_path = tempfile.mkstemp()
    app.config['DATABASE'] = temp_db_path
    app.config['TESTING'] = True

    with app.test_client() as client:
        with app.app_context():
            init_db()
        yield client

    os.close(db_fd)
    os.unlink(temp_db_path)


def test_index_page(client):
    """Test that the main page loads."""
    rv = client.get('/')
    assert rv.status_code == 200
    assert b'Task Manager' in rv.data


def test_add_task(client):
    """Test adding a new task."""
    rv = client.post('/add', data={'title': 'Test Task'})
    assert rv.status_code == 302  # Redirect after POST

    # Check task appears on main page
    rv = client.get('/')
    assert b'Test Task' in rv.data


def test_empty_task_not_added(client):
    """Test that empty tasks are not added."""
    rv = client.post('/add', data={'title': ''})
    assert rv.status_code == 302

    rv = client.get('/')
    assert b'No tasks yet!' in rv.data


def test_api_stats_empty(client):
    """Test API stats endpoint with no tasks."""
    rv = client.get('/api/stats')
    assert rv.status_code == 200
    data = rv.get_json()
    assert data['total_tasks'] == 0
    assert data['completed_tasks'] == 0
    assert data['incomplete_tasks'] == 0
    assert data['completion_rate'] == 0


def test_api_stats_with_tasks(client):
    """Test API stats endpoint with tasks."""
    # Add some tasks
    client.post('/add', data={'title': 'Task 1'})
    client.post('/add', data={'title': 'Task 2'})
    
    # Complete one task (get the task ID first)
    rv = client.get('/')
    # For this test, we'll assume the first task has ID 1
    client.post('/toggle/1')
    
    # Check stats
    rv = client.get('/api/stats')
    assert rv.status_code == 200
    data = rv.get_json()
    assert data['total_tasks'] == 2
    assert data['completed_tasks'] == 1
    assert data['incomplete_tasks'] == 1
    assert data['completion_rate'] == 50.0
