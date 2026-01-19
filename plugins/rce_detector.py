import re

def scan(content):
    findings = []
    patterns = [
        (r'subprocess\.(call|run|Popen)\(.*\bshell\s*=\s*True', "Critical: Shell execution enabled"),
        (r'os\.system\(', "Critical: Unsafe system command execution"),
        (r'eval\(', "Critical: Dynamic code execution (eval)"),
        (r'exec\(', "Critical: Dynamic code execution (exec)"),
        (r'import\s+os\s*;\s*os\.system', "High: Inline system command")
    ]

    for pattern, desc in patterns:
        if re.search(pattern, content):
            findings.append({
                "type": "RCE / Command Injection",
                "severity": "critical",
                "details": desc
            })
    return findings