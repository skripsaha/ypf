import networkx as nx
import matplotlib.pyplot as plt
from rich.console import Console

console = Console()

class GraphBuilder:
    def __init__(self, results):
        self.results = results
        self.G = nx.Graph()
        self.severity_colors = {
            'critical': '#ff3333',
            'high': '#ff6600',
            'medium': '#ffcc00',
            'low': '#ffff00',
            'info': '#00ff00'
        }

    def build(self):
        for item in self.results:
            file_node = item['file']
            sev = item['severity'].lower()
            
            vuln_color = self.severity_colors.get(sev, '#808080')
            vuln_node = f"{item['type']}\n({item['severity']})"
            self.G.add_node(file_node, color='#a0c4ff', node_type='file')
            self.G.add_node(vuln_node, color=vuln_color, node_type='vuln')
            self.G.add_edge(file_node, vuln_node)

    def draw(self, output_file="reports/attack_graph.png"):
        if not self.results:
            return

        plt.figure(figsize=(12, 8))
        pos = nx.spring_layout(self.G, k=0.8, seed=42) 
        
        node_colors = [self.G.nodes[n].get('color', 'gray') for n in self.G.nodes]
        
        nx.draw(self.G, pos, 
                with_labels=True, 
                node_color=node_colors,
                node_size=3000, 
                font_size=11,
                font_weight="normal",
                edge_color="#dddddd",
                width=2)
        
        plt.savefig(output_file, bbox_inches='tight')
        plt.close()
        console.print(f"saved to {output_file}")