
def run_zap_scan(url):
    return {
        "url": url,
        "alerts": [
            {"name": "Reflected XSS", "risk": "High", "param": "search"},
            {"name": "CSRF", "risk": "Medium", "param": "token"},
            {"name": "Information Disclosure", "risk": "Low", "param": "server"}
        ]
    }
