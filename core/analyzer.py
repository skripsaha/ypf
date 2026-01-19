import os
import yaml
import importlib.util
from pathlib import Path
from rich.console import Console
from rich.table import Table

console = Console()

class Analyzer:
    def __init__(self):
        self.config = self._load_config()
        self.plugins = self._load_plugins()
        self.results = []

    def _load_config(self):
        with open("config/settings.yaml", "r") as f:
            return yaml.safe_load(f)

    def _load_plugins(self):
        plugins = []
        plugin_dir = Path("plugins")
        for file in plugin_dir.glob("*_detector.py"):
            spec = importlib.util.spec_from_file_location(file.stem, file)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            if hasattr(module, "scan"):
                plugins.append(module)
        return plugins

    def scan_directory(self, target_path):
        target = Path(target_path)
        ignore = self.config['scanner']['ignore_dirs']
        exts = tuple(self.config['scanner']['target_extensions'])

        for root, dirs, files in os.walk(target):
            dirs[:] = [d for d in dirs if d not in ignore]
            for file in files:
                if file.endswith(exts):
                    full_path = Path(root) / file
                    self._scan_file(full_path)
        
        return self.results

    def _scan_file(self, filepath):
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
            
            for plugin in self.plugins:
                findings = plugin.scan(content)
                for finding in findings:
                    finding['file'] = str(filepath)
                    self.results.append(finding)
        except Exception as e:
            console.print(f"[red]Error reading {filepath}: {e}[/red]")

    def print_report(self):
        if not self.results:
            console.print("[green]No vulnerabilities found[/green]")
            return

        table = Table(title="ypf report")
        table.add_column("Type", style="cyan")
        table.add_column("Severity", style="red")
        table.add_column("File", style="white")
        table.add_column("Details", style="yellow")

        for res in self.results:
            table.add_row(
                res['type'], 
                res['severity'], 
                res['file'], 
                res['details']
            )
        console.print(table)