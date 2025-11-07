# io_utils.py
import os


def ensure_dir(path: str):
    """Ensure that a directory exists."""
    os.makedirs(path, exist_ok=True)


def write_text_file(path: str, content: str):
    """Write text content to a file."""
    ensure_dir(os.path.dirname(path))
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)


def read_text_file(path: str) -> str:
    """Read and return text content from a file."""
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()
