import subprocess

def run_zap_scan(url):
    try:
        output = subprocess.check_output(["zap-cli", "quick-scan", url])
        return output.decode("utf-8")
    except Exception as e:
        return str(e)
