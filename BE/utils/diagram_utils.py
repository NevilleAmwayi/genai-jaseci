# diagram_utils.py
import json


def generate_mermaid_diagram(ccg_json: str) -> str:
    """
    Generate a Mermaid diagram (graph TD) representation of the Code Context Graph (CCG).
    Each Python file is represented as a node that connects to its functions and classes.
    """
    try:
        ccg = json.loads(ccg_json)
    except Exception:
        return '```mermaid\n%% Invalid CCG data\ngraph TD\n```'

    lines = ['```mermaid', 'graph TD']

    # Limit the size for large repos to avoid clutter
    for path, content in list(ccg.items())[:50]:
        short = path.replace('/', '_').replace('.', '_')
        lines.append(f'    subgraph {short}')
        for func in content.get('functions', [])[:10]:
            node = f'{short}_{func}'
            lines.append(f'        {short} --> {node}["{func}()"]')
        for cls in content.get('classes', [])[:10]:
            cls_node = f'{short}_{cls}'
            lines.append(f'        {short} --> {cls_node}["class {cls}"]')
        lines.append('    end')

    lines.append('```')
    return '\n'.join(lines)
