from flask import Flask, render_template, request, redirect, url_for, session
from modules.nmap_scan import run_nmap
from openvas_scan import get_simulated_openvas_results
from file_scan import scan_file_with_yara
from werkzeug.utils import secure_filename
import json, os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Change ce mot de passe !
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def login():
    return render_template("login.html")

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    if username == "admin" and password == "cyber":
        session['user'] = username
        return redirect(url_for('dashboard'))
    return "Identifiants invalides"

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))

    scan_history = []
    if os.path.exists("scan_history.json"):
        with open("scan_history.json") as f:
            scan_history = json.load(f)

    return render_template("dashboard.html", history=scan_history)

@app.route('/scan', methods=['POST'])
def scan():
    if 'user' not in session:
        return redirect(url_for('login'))

    ip = request.form['target']
    result = run_nmap(ip)

    scan_entry = {
        "ip": ip,
        "ports": ", ".join(result['open_ports']),
        "status": "Vulnérable" if result['open_ports'] else "Sain",
        "date": datetime.now().strftime("%d/%m/%Y")
    }

    history_file = "scan_history.json"
    history = []
    if os.path.exists(history_file):
        with open(history_file) as f:
            history = json.load(f)

    history.insert(0, scan_entry)
    with open(history_file, "w") as f:
        json.dump(history, f, indent=2)

    return render_template("scan_result.html", ip=ip, result=result)

@app.route("/openvas")
def openvas():
    if 'user' not in session:
        return redirect(url_for('login'))
    results = get_simulated_openvas_results()
    return render_template("openvas_results.html", results=results)

@app.route('/file', methods=['GET', 'POST'])
def file_scan():
    if 'user' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        uploaded_file = request.files['file']
        if uploaded_file:
            filename = secure_filename(uploaded_file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            uploaded_file.save(filepath)
            result = scan_file_with_yara(filename)
            return render_template("file_result.html", result=result, filename=filename)

    return render_template("file_upload.html")

if __name__ == '__main__':
    app.run(debug=True)
