import subprocess

def run_metasploit():
    try:
        return subprocess.check_output(["msfconsole", "-q", "-x", "help; exit"], stderr=subprocess.STDOUT).decode("utf-8")
    except Exception as e:
        return str(e)
