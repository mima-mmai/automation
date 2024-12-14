from flask import Flask, jsonify
import datetime
import os

app = Flask(__name__)

# Sample data for other endpoints
AUTOMATION_PROJECTS = [
    {
        "id": 1, 
        "name": "Email Automation", 
        "description": "Automated email sending script",
        "status": "In Progress"
    },
    {
        "id": 2,
        "name": "File Organizer",
        "description": "Script to organize files by type and date",
        "status": "Planned"
    }
]

@app.route('/v1/get_date')
def get_date():
    """Return the current date and time."""
    current_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return jsonify({"date": current_date})

@app.route('/v1/say_hello')
def say_hello():
    """Return a friendly greeting."""
    return jsonify({"message": "Hello, World!"})

@app.route('/v1/get_py_projects')
def get_py_projects():
    """Return a list of Python projects in the current directory."""
    try:
        # List Python projects (directories or .py files) in the current directory
        py_projects = [
            item for item in os.listdir('.')
            if (os.path.isdir(item) or item.endswith('.py')) and not item.startswith('.')
        ]
        return jsonify({"projects": py_projects})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/v1/get_todolist')
def get_todolist():
    """Return the contents of todo.md file or an error message."""
    todo_file_path = r'C:\ai\mmai\todo.md'
    
    try:
        # Check if the file exists
        if not os.path.exists(todo_file_path):
            return jsonify({
                "error": "Todo file not found", 
                "path": todo_file_path
            }), 404
        
        # Read and return file contents
        with open(todo_file_path, 'r', encoding='utf-8') as file:
            todo_contents = file.read()
        
        return jsonify({
            "todo_file_path": todo_file_path,
            "contents": todo_contents
        })
    
    except Exception as e:
        return jsonify({
            "error": f"Error reading todo file: {str(e)}",
            "path": todo_file_path
        }), 500

@app.route('/v1/get_automation')
def get_automation():
    """Return automation projects."""
    return jsonify({"automation_projects": AUTOMATION_PROJECTS})

if __name__ == '__main__':
    app.run(host='localhost', port=6462, debug=True)