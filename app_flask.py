from flask import Flask, jsonify, render_template_string, redirect, send_from_directory
import datetime
import os
import markdown2
import json
import re  
from flask import request

from flask_cors import CORS

app = Flask(__name__, static_url_path='/static')
CORS(app)
CONFIG_PATH = 'static/config/config.json'
TODO_PATH = 'static/data/todo/todo.md'
DATEIEN_PATH = 'static/dateien'
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


@app.route('/v1/config', methods=['POST'])
def create_config():
    """Create a new JSON config."""
    try:
        data = request.json
        with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)
        return jsonify({"message": "Config created successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/v1/config', methods=['GET'])
def read_config():
    """Read the JSON config."""
    try:
        if not os.path.exists(CONFIG_PATH):
            return jsonify({"message": "Config file not found"}), 404
        with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


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
    """Return the contents of todo.md file or a fallback message."""
    todo_datei='todo.md'
    #todo_file_path = f"C:\\Users\\itbc000133\\AppData\\Local\\LOCALHOME\\repos\\py_upstream\\zisch\\projects\\web_localhost\\automatisierung\\static\\data\\todo\\{todo_datei}"
    todo_file_path = f"/static/data/todo/{todo_datei}"
    FALLBACK ="""
# Heute 
## Essen

- [ ] Frühstück
- [ ] Mittag
## Sport

- [ ] Joggen
- [ ] radeln
- !!!_todo_file_path_!!!
"""
    todo_contents="nix nada niente"
    html_content="<p>nix nada niente</p>"
    try:
        if os.path.exists(todo_file_path):
            FALLBACK = FALLBACK.replace('!!!_todo_file_path_!!!', f"Loaded from {todo_file_path}")
            with open(todo_file_path, 'r', encoding='utf-8') as file:
                todo_contents = file.read()
        else:
            FALLBACK = FALLBACK.replace('!!!_todo_file_path_!!!', f"Not found: {todo_file_path}")
            todo_contents=FALLBACK
        html_content = markdown_to_html_with_checkboxes(todo_contents)
    except Exception as e:
        return jsonify({
            "Fehlerchen": "!",
            "error": f"{e}"
        }, 500)
    return html_content

@app.route('/v1/get_automation')
def get_automation():
    """Return automation projects."""
    return jsonify({"automation_projects": AUTOMATION_PROJECTS})

@app.route('/')
def root():
    """Redirect from root URL to /static/index.html."""
    return redirect('/static/index.html')

@app.route('/static/<path:path>')
def send_static(path):
    """Serve files from the static directory."""
    return send_from_directory('static', path)

@app.route('/api')
def landingpage():
    """Return all routes with the 'v' version as HTML."""
    routes = [
        "/v1/get_date",
        "/v1/say_hello",
        "/v1/get_py_projects",
        "/v1/get_todolist",
        "/v1/get_automation"
    ]
    html_content = "<h1>Available Routes</h1><ul>"
    for route in routes:
        html_content += f"<li><a href='{route}'>{route}</a></li>"
    html_content += "</ul>"
    return render_template_string(html_content)


def markdown_to_html_with_checkboxes(markdown_text):
    # Convert markdown to HTML
    html_content = markdown2.markdown(markdown_text)
    
    # Define regex replacements for checkboxes
    replacements = {
        r'\[ \]': r'<input type="checkbox">',
        r'\[x\]': r'<input type="checkbox" checked>',
    }

    # Apply replacements for task list checkboxes
    for pattern, replacement in replacements.items():
        html_content = re.sub(pattern, replacement, html_content, flags=re.IGNORECASE)

    return html_content

# Ensure the base directory exists
os.makedirs(DATEIEN_PATH, exist_ok=True)

# Generate CRUD routes
def generate_crud_routes():
    @app.route('/v1/dateien/<path:path_param>', methods=['POST'])
    def create_file(path_param):
        """Create a new text or JSON file."""
        try:
            file_path = f"{DATEIEN_PATH}/{path_param}"
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            content_type = request.headers.get('Content-Type', '')
            
            if 'application/json' in content_type:
                data = request.json
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=4)
            else:
                data = request.data.decode('utf-8')
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(data)
            return jsonify({"message": "File created successfully"}), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route('/v1/dateien/<path:path_param>', methods=['GET'])
    def read_file(path_param):
        """Read a text or JSON file."""
        try:
            file_path = f"{DATEIEN_PATH}/{path_param}"
            if not os.path.exists(file_path):
                return jsonify({"message": "File not found"}), 404

            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if path_param.endswith('.json'):
                data = json.loads(content)
                return jsonify(data), 200
            return content, 200, {'Content-Type': 'text/plain'}
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route('/v1/dateien/<path:path_param>', methods=['PUT'])
    def update_file(path_param):
        """Update a text or JSON file."""
        try:
            file_path = f"{DATEIEN_PATH}/{path_param}"
            if not os.path.exists(file_path):
                return jsonify({"message": "File not found"}), 404

            content_type = request.headers.get('Content-Type', '')
            if 'application/json' in content_type:
                data = request.json
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=4)
            else:
                data = request.data.decode('utf-8')
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(data)
            return jsonify({"message": "File updated successfully"}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

@app.route('/test')
def test():
    try:
       test_dateien_endpoints()
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    return jsonify({"und": "ok"}), 200
# Internal test function
def test_dateien_endpoints():
    import requests
    base_url = "http://localhost:6462/v1/dateien"
    test_file = "test.txt"

    try:
        # Test POST
        print("Testing Create (POST)...")
        response = requests.post(f"{base_url}/{test_file}", data="Sample text")
        print(response.json())
        # Test GET
        print("Testing Read (GET)...")
        response = requests.get(f"{base_url}/{test_file}")
        print(response.text)

        # Test PUT
        print("Testing Update (PUT)...")
        response = requests.put(f"{base_url}/{test_file}", data="Updated text")
        print(response.json())
    except Exception as e:
        return jsonify({"tut nicht": "{e}"}), 500   

generate_crud_routes()

if __name__ == '__main__':
    app.run(host='localhost', port=6462, debug=True)
