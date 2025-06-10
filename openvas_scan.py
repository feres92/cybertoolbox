import subprocess

def get_simulated_openvas_results():
    try:
        output = subprocess.check_output(["gvm-cli", "--gmp-username", "admin", "--gmp-password", "admin", "socket", "--xml", "<get_tasks/>"])
        return output.decode("utf-8")
    except Exception as e:
        return str(e)