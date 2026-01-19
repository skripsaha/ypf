import re

class AutoFixer:
    @staticmethod
    def get_fix(vuln_type, original_code):
        knowledge_base = {
            "SQL Injection": {
                "new_code": "# исправление: используйте параметризацию\n    cur.execute('SELECT * FROM users WHERE id = ?', (user_id,))",
                "explanation": "замена f-строки на безопасный плейсхолдер '?' предотвращает внедрение команд."
            },
            "RCE / Command Injection": {
                "new_code": "# исправление: Безопасный запуск без shell=True\n    subprocess.run(['echo', 'Running', cmd], shell=False)",
                "explanation": "отключение shell=True блокирует выполнение цепочек команд через ';' или '&&'."
            },
            "XSS / Injection": {
                "new_code": "# исправление: Авто-экранирование через шаблоны\n    return render_template('index.html', username=username)",
                "explanation": "render_template автоматически очищает ввод пользователя от скриптов."
            },
            "Hardcoded Secret": {
                "new_code": "import os\nAPI_KEY = os.getenv('API_KEY') # исправление: секрет в переменных окружения!",
                "explanation": "секреты нельзя хранить в коде. Используйте .env файлы."
            },
            "Insecure Deserialization": {
                "new_code": "# исправление: используйте json вместо pickle\n    data = json.loads(user_input)",
                "explanation": "json не позволяет выполнять произвольный код при чтении данных."
            }
        }
        return knowledge_base.get(vuln_type, {"new_code": "Review required", "explanation": "manual исправление:  needed"})