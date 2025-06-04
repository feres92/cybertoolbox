from flask import Flask, render_template, request, redirect, url_for, session
from modules.nmap_scan import run_nmap

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
    return render_template("dashboard.html")

@app.route('/scan', methods=['POST'])
def scan():
    if 'user' not in session:
        return redirect(url_for('login'))
    ip = request.form['target']
    result = run_nmap(ip)
    return render_template("scan_result.html", ip=ip, result=result)

if __name__ == '__main__':
    app.run(debug=True)
