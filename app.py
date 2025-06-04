from flask import Flask, render_template, request, redirect, url_for, session
from modules.nmap_scan import run_nmap
from openvas_scan import get_simulated_openvas_results
from datetime import datetime
import json
import os

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Change ce mot de passe !

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
    try:
        with open("scan_history.json", "r") as f:
            history = json.load(f)
    except:
        history = []
    return render_template("dashboard.html", history=history)

@app.route('/scan', methods=['POST'])
def scan():
    if 'user' not in session:
        return redirect(url_for('login'))
    ip = request.form['target']
    result = run_nmap(ip)
    enregistrer_scan(ip, result)
    return render_template("scan_result.html", ip=ip, result=result)

def enregistrer_scan(ip, result):
    lignes = result.splitlines()
    ports = [line.split('/')[0] for line in lignes if '/tcp' in line and 'open' in line]
    statut = "Sain" if len(ports) <= 2 else "Vulnérable"
    date = datetime.now().strftime("%d/%m/%Y")

    new_entry = {
        "ip": ip,
        "ports": ', '.join(ports),
        "statut": statut,
        "date": date
    }

    if not os.path.exists("scan_history.json"):
        with open("scan_history.json", "w") as f:
            json.dump([], f)

    with open("scan_history.json", "r") as f:
        data = json.load(f)
    data.insert(0, new_entry)
    with open("scan_history.json", "w") as f:
        json.dump(data, f, indent=2)

@app.route("/openvas")
def openvas():
    if 'user' not in session:
        return redirect(url_for('login'))
    results = get_simulated_openvas_results()
    return render_template("openvas_results.html", results=results)

if __name__ == '__main__':
    app.run(debug=True)
