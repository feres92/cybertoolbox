import subprocess

def run_john(filepath):
    try:
        subprocess.run(["zip2john", filepath, ">", "hash.txt"], shell=True)
        output = subprocess.check_output(["john", "hash.txt"])
        return output.decode("utf-8")
    except Exception as e:
        return str(e)
