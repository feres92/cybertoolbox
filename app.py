from flask import Flask, render_template, request, redirect, url_for, session, send_file
from modules.nmap_scan import run_nmap
from modules.sqlmap_module import run_sqlmap_scan
from modules.zap_module import run_zap_scan
from modules.openvas_module import run_openvas_scan
from modules.file_scan import scan_file_with_yara
from modules.metasploit_module import run_metasploit
from modules.john_module import run_john
from modules.report_generator import generate_report
from werkzeug.utils import secure_filename
import json, os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'supersecretkey'
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
    result["ip"] = ip
    scan_entry = {
        "ip": ip,
        "ports": ", ".join(result['open_ports']),
        "statut": "Vulnérable" if result['open_ports'] else "Sain",
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

@app.route("/openvas", methods=['GET', 'POST'])
def openvas():
    if 'user' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        ip = request.form['target']
        results = run_openvas_scan(ip)
        return render_template("openvas_results.html", results=results)
    return render_template("scan_form.html")

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
            result = scan_file_with_yara(filepath)
            return render_template("file_result.html", result=result, filename=filename)
    return render_template("file_upload.html")

@app.route("/sqlmap", methods=['GET', 'POST'])
def sqlmap():
    if 'user' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        url = request.form['url']
        result = run_sqlmap_scan(url)
        return render_template("sqlmap_result.html", result=result)
    return render_template("scan_form.html")

@app.route("/zap", methods=['GET', 'POST'])
def zap():
    if 'user' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        url = request.form['url']
        result = run_zap_scan(url)
        return render_template("zap_result.html", result=result)
    return render_template("scan_form.html")

@app.route("/metasploit", methods=['GET', 'POST'])
def metasploit():
    if 'user' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        ip = request.form['target']
        result = run_metasploit(ip)
        return render_template("metasploit_result.html", result=result)
    return render_template("scan_form.html")

@app.route("/john", methods=['GET', 'POST'])
def john():
    if 'user' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        uploaded_file = request.files['file']
        if uploaded_file:
            filename = secure_filename(uploaded_file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            uploaded_file.save(filepath)
            result = run_john(filepath)
            return render_template("john_result.html", result=result)
    return render_template("file_upload.html")

@app.route('/report')
def report():
    if 'user' not in session:
        return redirect(url_for('login'))
    if not os.path.exists("scan_history.json"):
        return "Aucun scan trouvé"
    with open("scan_history.json") as f:
        history = json.load(f)
    filepath = generate_report(history)
    filename = os.path.basename(filepath)
    return render_template("report.html", filename=filename)

@app.route('/report/download/<filename>')
def download_report(filename):
    filepath = os.path.join("reports", filename)
    return send_file(filepath, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
