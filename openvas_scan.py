import json

def get_simulated_openvas_results():
    return [
    {
        "id": "CVE-2021-34527",
        "title": "Windows Print Spooler Remote Code Execution",
        "severity": "Critique",
        "description": "Une vuln\u00e9rabilit\u00e9 dans le service Print Spooler de Windows permet l'ex\u00e9cution de code \u00e0 distance.",
        "solution": "D\u00e9sactiver le service Print Spooler ou appliquer le correctif Microsoft."
    },
    {
        "id": "CVE-2020-1472",
        "title": "Zerologon Privilege Escalation",
        "severity": "\u00c9lev\u00e9e",
        "description": "Vuln\u00e9rabilit\u00e9 dans Netlogon permettant d'\u00e9lever les privil\u00e8ges vers administrateur de domaine.",
        "solution": "Installer les correctifs de s\u00e9curit\u00e9 d'ao\u00fbt 2020."
    },
    {
        "id": "CVE-2019-0708",
        "title": "Remote Desktop Services Remote Code Execution",
        "severity": "Critique",
        "description": "Aussi appel\u00e9e BlueKeep, cette faille permet une ex\u00e9cution de code via RDP sans authentification.",
        "solution": "Appliquer le patch de s\u00e9curit\u00e9 Microsoft imm\u00e9diatement."
    }
]

if __name__ == "__main__":
    results = get_simulated_openvas_results()
    for vuln in results:
        print(f"- {vuln['id']} ({vuln['severity']}) : {vuln['title']}")
        print(f"  ➜ Description : {vuln['description']}")
        print(f"  ➜ Solution    : {vuln['solution']}\n")
