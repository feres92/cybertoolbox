def scan_file_with_yara(filename):
    # Simulation simple
    if filename.lower().endswith(('.exe', '.bat', '.vbs')):
        return {
            "verdict": "Malveillant",
            "details": [
                "Pattern YARA : Suspicious Executable",
                "VirusTotal : 31/70 antivirus détectent",
                "ClamAV : Trojan.Generic"
            ]
        }
    else:
        return {
            "verdict": "Sain",
            "details": [
                "Pattern YARA : Aucun",
                "VirusTotal : 0/70",
                "ClamAV : Aucun virus détecté"
            ]
        }
