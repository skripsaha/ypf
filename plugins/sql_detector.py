import re

def scan(content):
    findings = []
    patterns = [
        (r'f["\'].*SELECT.*FROM', "SQL-injection via f-string construction"),
        (r'\.execute\(.*query', "Dangerous execution of variable 'query'"),
        (r'["\'].*\+.*SELECT.*FROM', "SQL-injection via string concatenation")
    ]

    for pattern, desc in patterns:
        if re.search(pattern, content, re.IGNORECASE):
            findings.append({
                "type": "SQL Injection",
                "severity": "critical",
                "details": desc
            })
    return findings