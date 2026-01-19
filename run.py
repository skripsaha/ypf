#!/usr/bin/env python3
import sys
import os
import json
from pathlib import Path
from core.analyzer import Analyzer
from visualizer.graph_builder import GraphBuilder
from rich.panel import Panel
from rich.console import Console

console = Console()

def main():
    os.system('clear' if os.name == 'posix' else 'cls')
    Path("reports").mkdir(exist_ok=True)

    #demo тест
    target = "demo_app"
    if len(sys.argv) > 1:
        target = sys.argv[1]
    
    console.print(f"analyzing [bold]{target}[/bold]...")
    analyzer = Analyzer()
    results = analyzer.scan_directory(target)
    
    analyzer.print_report()
    if results:
        builder = GraphBuilder(results)
        builder.build()
        builder.draw()
        with open('reports/latest_report.json', 'w') as f:
            json.dump(results, f, indent=4)


if __name__ == "__main__":
    main()