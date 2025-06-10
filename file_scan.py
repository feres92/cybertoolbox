import yara
import os

def scan_file_with_yara(filename):
    rules = yara.compile(filepath='yara_rules/index.yar')
    matches = rules.match(filepath=os.path.join('uploads', filename))
    return [match.rule for match in matches]

