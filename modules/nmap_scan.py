import subprocess

def run_nmap(ip):
    try:
        result = subprocess.run(['nmap', '-F', ip], capture_output=True, text=True, timeout=5)
        return result.stdout
    except subprocess.TimeoutExpired:
        return "Scan trop long ou bloqué (timeout)"
    except Exception as e:
        return f"Erreur : {str(e)}"
