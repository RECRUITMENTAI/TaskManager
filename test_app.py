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
