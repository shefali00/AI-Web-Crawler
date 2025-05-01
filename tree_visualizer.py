#tree_visualizer.py
import graphviz

def render_tree(node):
    dot = graphviz.Digraph()
    def recurse(n):
        dot.node(n['url'], label=n['title'])
        for child in n.get('children', []):
            dot.edge(n['url'], child['url'])
            recurse(child)
    recurse(node)
    return dot
