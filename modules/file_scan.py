import yara
import os

RULES_DIR = "yara_rules"
if not os.path.exists(RULES_DIR):
    os.makedirs(RULES_DIR)

# Exemple de règle YARA simple
rule_content = '''
rule ExampleRule
{
    strings:
        $a = "malicious"
    condition:
        $a
}
'''

with open(os.path.join(RULES_DIR, "example.yar"), "w") as f:
    f.write(rule_content)

rules = yara.compile(filepath=os.path.join(RULES_DIR, "example.yar"))

def scan_file_with_yara(filename):
    filepath = os.path.join("uploads", filename)
    matches = rules.match(filepath)
    if matches:
        return f"Infections détectées : {[match.rule for match in matches]}"
    else:
        return "Aucune infection détectée"
