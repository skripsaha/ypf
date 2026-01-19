import re

def scan(content):
    findings = []
    regex = r'(api_key|secret|password|token)\s*=\s*[\'"][a-zA-Z0-9_\-!]{8,}[\'"]'
    
    if re.search(regex, content, re.IGNORECASE):
        findings.append({
            "type": "hardcoded secret",
            "severity": "medium",
            "details": "possible sensitive data in code"
        })
    return findings