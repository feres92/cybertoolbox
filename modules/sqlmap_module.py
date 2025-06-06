
def run_sqlmap_scan(url):
    return {
        "url": url,
        "status": "Vulnérable",
        "vulnerabilities": [
            {"type": "SQL Injection", "payload": "' OR '1'='1", "param": "username"},
            {"type": "Login Bypass", "payload": "' OR 1=1--", "param": "password"}
        ]
    }
