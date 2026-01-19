import re

def scan(content):
    findings = []
    patterns = [
        (r'render_template_string\(', "SSTI / XSS Vulnerability"),
        (r'\|safe', "Unsafe Jinja2 filter usage"),
        (r'\.html\(', "Potential DOM XSS")
    ]

    for pattern, desc in patterns:
        if re.search(pattern, content):
            findings.append({
                "type": "XSS / Injection",
                "severity": "high",
                "details": desc
            })
    return findings
    