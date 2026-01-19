from flask import Flask, request, render_template_string
import sqlite3
import os
import subprocess
import pickle
import hashlib
import yaml

app = Flask(__name__)
API_KEY = "super_secret_admin_key_12345" # пример хардкод-секрета

@app.route('/')
def home():
    username = request.args.get('username', 'Guest')
    #xss
    template = f"<h1>Hello, {username}!</h1>"
    return render_template_string(template)

@app.route('/admin')
def admin():
    cmd = request.args.get('cmd')
    #rce иньекция команд
    os.system(f"echo Running command: {cmd}") 
    return "Command executed"

@app.route('/restore')
def restore():
    data = request.args.get('data')
    #небезопасная десериализация
    obj = pickle.loads(data)
    return "Data restored"

@app.route('/login')
def login():
    password = request.args.get('password')
    #слабая криптография
    hashed = hashlib.md5(password.encode()).hexdigest()
    
    user_id = request.args.get('id')
    conn = sqlite3.connect('db.sqlite')
    cur = conn.cursor()
    #SQL-иньекция!
    query = f"SELECT * FROM users WHERE id = {user_id}" 
    cur.execute(query)
    
    return f"User {hashed} checked"

if __name__ == '__main__':
    app.run(debug=True)