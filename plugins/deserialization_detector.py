import re

def scan(content):
    findings = []
    patterns = [
        (r'pickle\.loads?\(', "insecure deserialization (Pickle)"),
        (r'yaml\.load\(.*Loader\s*=\s*yaml\.Loader', "unsafe YAML loading"),
        (r'yaml\.load\([^,)]*\)', "unsafe YAML loading (default loader)")
    ]

    for pattern, desc in patterns:
        if re.search(pattern, content):
            findings.append({
                "type": "insecure deserialization",
                "severity": "high",
                "details": desc
            })
    return findings
