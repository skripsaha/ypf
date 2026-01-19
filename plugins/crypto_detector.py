import re

def scan(content):
    findings = []
    patterns = [
        (r'hashlib\.md5\(', "weak hashing algorithm (md5)"),
        (r'hashlib\.sha1\(', "weak hashing algorithm (sha1)"),
        (r'random\.random\(', "weak PRNG"),
        (r'base64\.b64encode\(.*password', "encoding isnt encryption")
    ]

    for pattern, desc in patterns:
        if re.search(pattern, content, re.IGNORECASE):
            findings.append({
                "type": "weak cryptography",
                "severity": "medium",
                "details": desc
            })
    return findings