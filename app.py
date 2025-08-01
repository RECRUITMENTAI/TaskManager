from flask import Flask, request, redirect, url_for, render_template_string
import sqlite3
import os

app = Flask(__name__)

# Database configuration
DATABASE = 'tasks.db'

def init_db():
    """Initialize the database with tasks table if it doesn't exist."""
    with sqlite3.connect(DATABASE) as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'incomplete'
            )
        ''')
        conn.commit()

def get_db_connection():
    """Get a database connection."""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def get_all_tasks():
    """Retrieve all tasks from the database."""
    conn = get_db_connection()
    tasks = conn.execute('SELECT * FROM tasks ORDER BY id DESC').fetchall()
    conn.close()
    return tasks

def add_task(title):
    """Add a new task to the database."""
    conn = get_db_connection()
    conn.execute('INSERT INTO tasks (title, status) VALUES (?, ?)', (title, 'incomplete'))
    conn.commit()
    conn.close()

def toggle_task_status(task_id):
    """Toggle task status between complete and incomplete."""
    conn = get_db_connection()
    task = conn.execute('SELECT status FROM tasks WHERE id = ?', (task_id,)).fetchone()
    if task:
        new_status = 'complete' if task['status'] == 'incomplete' else 'incomplete'
        conn.execute('UPDATE tasks SET status = ? WHERE id = ?', (new_status, task_id))
        conn.commit()
    conn.close()

def delete_task(task_id):
    """Delete a task from the database."""
    conn = get_db_connection()
    conn.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    conn.commit()
    conn.close()

# HTML template with inline CSS
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Task Manager</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', roboto, sans-serif;
            background-color: #f5f5f5;
            line-height: 1.6;
            color: #333;
        }
        
        .container {
            max-width: 600px;
            margin: 2rem auto;
            padding: 2rem;
            background: white;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        
        h1 {
            text-align: center;
            color: #2c3e50;
            margin-bottom: 2rem;
            font-size: 2.5rem;
        }
        
        .add-task-form {
            display: flex;
            gap: 10px;
            margin-bottom: 2rem;
            padding: 1rem;
            background: #f8f9fa;
            border-radius: 8px;
        }
        
        .add-task-form input[type="text"] {
            flex: 1;
            padding: 12px;
            border: 2px solid #e9ecef;
            border-radius: 6px;
            font-size: 16px;
            transition: border-color 0.3s;
        }
        
        .add-task-form input[type="text"]:focus {
            outline: none;
            border-color: #007bff;
        }
        
        .btn {
            padding: 12px 20px;
            border: none;
            border-radius: 6px;
            cursor: pointer;
            font-size: 14px;
            font-weight: 500;
            text-decoration: none;
            display: inline-block;
            text-align: center;
            transition: all 0.3s;
        }
        
        .btn-primary {
            background-color: #007bff;
            color: white;
        }
        
        .btn-primary:hover {
            background-color: #0056b3;
        }
        
        .btn-success {
            background-color: #28a745;
            color: white;
            font-size: 12px;
            padding: 8px 12px;
        }
        
        .btn-success:hover {
            background-color: #1e7e34;
        }
        
        .btn-warning {
            background-color: #ffc107;
            color: #212529;
            font-size: 12px;
            padding: 8px 12px;
        }
        
        .btn-warning:hover {
            background-color: #e0a800;
        }
        
        .btn-danger {
            background-color: #dc3545;
            color: white;
            font-size: 12px;
            padding: 8px 12px;
        }
        
        .btn-danger:hover {
            background-color: #c82333;
        }
        
        .task-list {
            list-style: none;
        }
        
        .task-item {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 1rem;
            margin-bottom: 10px;
            background: #f8f9fa;
            border-radius: 8px;
            border-left: 4px solid #007bff;
            transition: all 0.3s;
        }
        
        .task-item.completed {
            background: #d4edda;
            border-left-color: #28a745;
        }
        
        .task-content {
            flex: 1;
            margin-right: 1rem;
        }
        
        .task-title {
            font-size: 16px;
            font-weight: 500;
        }
        
        .task-title.completed {
            text-decoration: line-through;
            color: #6c757d;
        }
        
        .task-status {
            font-size: 12px;
            padding: 4px 8px;
            border-radius: 12px;
            font-weight: 500;
            margin-top: 4px;
            display: inline-block;
        }
        
        .task-status.incomplete {
            background-color: #fff3cd;
            color: #856404;
        }
        
        .task-status.complete {
            background-color: #d1ecf1;
            color: #0c5460;
        }
        
        .task-actions {
            display: flex;
            gap: 8px;
        }
        
        .empty-state {
            text-align: center;
            padding: 3rem;
            color: #6c757d;
        }
        
        .empty-state h3 {
            margin-bottom: 1rem;
            color: #495057;
        }
        
        @media (max-width: 480px) {
            .container {
                margin: 1rem;
                padding: 1rem;
            }
            
            .add-task-form {
                flex-direction: column;
            }
            
            .task-actions {
                flex-direction: column;
                gap: 4px;
            }
            
            .btn {
                font-size: 12px;
                padding: 8px 12px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Task Manager</h1>
        
        <!-- Add Task Form -->
        <form method="POST" action="/add" class="add-task-form">
            <input type="text" name="title" placeholder="Enter a new task..." required>
            <button type="submit" class="btn btn-primary">Add Task</button>
        </form>
        
        <!-- Task List -->
        {% if tasks %}
            <ul class="task-list">
                {% for task in tasks %}
                <li class="task-item {{ 'completed' if task.status == 'complete' else '' }}">
                    <div class="task-content">
                        <div class="task-title {{ 'completed' if task.status == 'complete' else '' }}">
                            {{ task.title }}
                        </div>
                        <span class="task-status {{ task.status }}">{{ task.status }}</span>
                    </div>
                    <div class="task-actions">
                        <form method="POST" action="/toggle/{{ task.id }}" style="display: inline;">
                            <button type="submit" class="btn {{ 'btn-warning' if task.status == 'complete' else 'btn-success' }}">
                                {{ 'Mark Incomplete' if task.status == 'complete' else 'Mark Complete' }}
                            </button>
                        </form>
                        <form method="POST" action="/delete/{{ task.id }}" style="display: inline;">
                            <button type="submit" class="btn btn-danger" onclick="return confirm('Are you sure you want to delete this task?')">
                                Delete
                            </button>
                        </form>
                    </div>
                </li>
                {% endfor %}
            </ul>
        {% else %}
            <div class="empty-state">
                <h3>No tasks yet!</h3>
                <p>Add your first task above to get started.</p>
            </div>
        {% endif %}
    </div>
</body>
</html>
'''

@app.route('/')
def index():
    """Display all tasks."""
    tasks = get_all_tasks()
    return render_template_string(HTML_TEMPLATE, tasks=tasks)

@app.route('/add', methods=['POST'])
def add():
    """Add a new task."""
    title = request.form.get('title', '').strip()
    if title:
        add_task(title)
    return redirect(url_for('index'))

@app.route('/toggle/<int:task_id>', methods=['POST'])
def toggle(task_id):
    """Toggle task completion status."""
    toggle_task_status(task_id)
    return redirect(url_for('index'))

@app.route('/delete/<int:task_id>', methods=['POST'])
def delete(task_id):
    """Delete a task."""
    delete_task(task_id)
    return redirect(url_for('index'))

@app.route('/health')
def health():
    """Health check endpoint for deployment verification."""
    return {'status': 'healthy', 'app': 'Flask Task Manager'}


if __name__ == '__main__':
    # Initialize database on startup
    init_db()

    # Run the application
    app.run(host='0.0.0.0', port=5000, debug=False)
