# parse_code.py
import os
import ast
import json


IGNORE_DIRS = {'.git', '__pycache__', 'node_modules', '.venv', '.env'}

def generate_file_tree(repo_path: str) -> str:
    tree = {}
    for root, dirs, files in os.walk(repo_path):
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
        rel = os.path.relpath(root, repo_path)
        node = tree
        if rel != '.':
            for part in rel.split(os.sep):
                node = node.setdefault(part, {})
        node.setdefault('files', [])
        node['files'].extend(files)
    return json.dumps(tree, indent=2)

def summarize_readme(repo_path: str) -> str:
    candidates = ['README.md', 'README.rst', 'readme.md']
    for c in candidates:
        p = os.path.join(repo_path, c)
        if os.path.exists(p):
            with open(p, 'r', encoding='utf-8') as f:
                text = f.read()
            # naive summary: first 5 paragraphs or first 300 words
            words = text.split()
            return ' '.join(words[:300])
    return 'No README found.'    

def build_ccg(repo_path: str) -> str:
    ccg = {}
    for root, _, files in os.walk(repo_path):
        for file in files:
            if file.endswith('.py'):
                path = os.path.join(root, file)
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        src = f.read()
                    tree = ast.parse(src)
                except Exception:
                    continue


                funcs = [n.name for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)]
                classes = [n.name for n in ast.walk(tree) if isinstance(n, ast.ClassDef)]
                ccg[path] = {'functions': funcs, 'classes': classes}
    return json.dumps(ccg, indent=2)

def query_ccg(query: str) -> str:
    # Placeholder: a minimal query helper - this can be improved
    # For now, simply return a message explaining that query support is limited
    return json.dumps({'query': query, 'result': 'Querying CCG not yet implemented.'})