import requests
from requests.auth import HTTPBasicAuth

def run_openvas_scan(target_ip):
    """
    Lance un scan OpenVAS via GVM REST API (GSA) sur un hôte cible
    (nécessite que OpenVAS/GVM soit déjà installé et configuré)
    """
    # Configuration GVM (modifie ces valeurs selon ton instance)
    gvm_url = "https://127.0.0.1:9392"
    username = "admin"
    password = "admin"  # change ce mot de passe selon ta conf

    session = requests.Session()
    session.auth = HTTPBasicAuth(username, password)
    session.verify = False  # désactive le certificat SSL auto-signé (à sécuriser en prod)

    try:
        # Exemple d'appel vers l'API (à adapter selon ta version de GVM)
        response = session.get(f"{gvm_url}/gmp?cmd=get_targets")
        if response.status_code == 200:
            return {
                "status": "OK",
                "details": response.text[:500]  # tronqué pour l'exemple
            }
        else:
            return {
                "status": "Erreur",
                "code": response.status_code,
                "message": response.text
            }
    except Exception as e:
        return {
            "status": "Erreur",
            "message": str(e)
        }
