import subprocess

def run_sqlmap_scan(url):
    try:
        output = subprocess.check_output(["sqlmap", "-u", url, "--batch", "--level=2", "--risk=1"])
        return output.decode("utf-8")
    except Exception as e:
        return str(e)
