import os
import json
import subprocess
from flask import Flask, render_template, jsonify, request, send_from_directory

app = Flask(__name__)

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
REPORTS_DIR = os.path.join(BASE_DIR, "reports")
TARGET_DIR = "demo_app"

if not os.path.exists(REPORTS_DIR):
    os.makedirs(REPORTS_DIR)

AI_FIX_DB = {
    "SQL Injection": {
        "code": "cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))",
        "desc": "Используйте параметризацию. Это предотвращает внедрение вредоносного SQL-кода."
    },
    "RCE / Command Injection": {
        "code": "subprocess.run(['ls', folder], shell=False)",
        "desc": "Отключите shell=True. Передавайте команды списком аргументов."
    },
    "XSS / Injection": {
        "code": "render_template('page.html', content=user_input)",
        "desc": "Jinja2 автоматически экранирует HTML, блокируя выполнение скриптов."
    },
    "Hardcoded Secret": {
        "code": "import os\nAPI_KEY = os.getenv('API_KEY')",
        "desc": "Никогда не храните пароли в коде. Используйте переменные окружения."
    },
    "Insecure Deserialization": {
        "code": "import json\ndata = json.loads(user_input)",
        "desc": "Замените Pickle на JSON. JSON не позволяет исполнять произвольный код."
    }
}

@app.route('/reports/<path:filename>')
def serve_reports(filename):
    return send_from_directory(REPORTS_DIR, filename)

@app.route('/')
def index():
    return render_template('dashboard.html')

@app.route('/api/scan')
def scan():
    try:
        subprocess.run(['python', 'run.py', TARGET_DIR], check=True)
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/get_vulns')
def get_vulns():
    report_path = os.path.join(REPORTS_DIR, "latest_report.json")
    if not os.path.exists(report_path):
        return jsonify([])
    
    try:
        with open(report_path, 'r') as f:
            data = json.load(f)
            return jsonify(data)
    except Exception:
        return jsonify([])

@app.route('/api/fix', methods=['POST'])
def fix():
    v_type = request.json.get('type')
    suggestion = AI_FIX_DB.get(v_type, {
        "code": "# Требуется ручное исправление",
        "desc": "Для данного типа уязвимости нет готового шаблона."
    })
    return jsonify(suggestion)


@app.route('/images/<path:filename>')
def serve_images(filename):
    images_dir = os.path.join(app.root_path, 'templates', 'images')
    return send_from_directory(images_dir, filename)

if __name__ == '__main__':
    print("http://localhost:5050")
    app.run(port=5050, debug=True)