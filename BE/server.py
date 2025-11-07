from flask import Flask, request, jsonify
import os
import tempfile
import shutil
import subprocess
from pathlib import Path
from utils.clone_repo import clone_repo

# -------------------------------------------
# Flask app setup
# -------------------------------------------
app = Flask(__name__)
PORT = 8000

# -------------------------------------------
# Health check endpoint
# -------------------------------------------
@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Codebase Genius backend running"}), 200

# -------------------------------------------
# 1. Clone repo + trigger Codebase Genius walker
# -------------------------------------------
@app.route("/walker/codebase_genius", methods=["POST"])
def run_codebase_genius():
    data = request.get_json() or {}
    repo_url = data.get("repo_url", "").strip()

    if not repo_url:
        return jsonify({"error": "Missing repository URL"}), 400

    # The temporary directory is created here, but the Jac walker handles cloning
    # and cleanup of the temporary clone inside its execution environment.
    # The cleanup for this higher-level tmp_dir is handled in the finally block.
    tmp_dir = tempfile.mkdtemp(prefix="codegenius_")
    print(f"[INFO] Temporary directory created at {tmp_dir}")

    # NOTE: The original code cloned the repo here, but based on main.jac, 
    # the walker is designed to clone the repo itself, so we skip the Flask clone
    # and let the Jac agent handle it inside run_pipeline.
    repo_name = repo_url.rstrip('/').split('/')[-1] # Simple deduction of repo name

    try:
        # Use absolute path to Jac file relative to server.py
        jac_path = Path(__file__).parent / "agents" / "main.jac"
        if not jac_path.exists():
            raise FileNotFoundError(f"Jac file not found: {jac_path}")

        # --- FIX APPLIED HERE: Added "--" separator ---
        # Correct Jac run syntax: jac run <file.jac> -- <walker_name> <arg=value>
        cmd = [
            "jac",
            "run",
            str(jac_path),
            "--",                       # Tells 'jac' to stop parsing options and pass the rest to the script/walker
            "codebase_entry",           # Walker name passed directly
            f"repo_url={repo_url}"      # Argument for the walker
        ]
        # ---------------------------------------------

        print(f"[INFO] Running Jac walker: {' '.join(cmd)}")
        
        # Capture output for debugging if needed, but 'check=True' ensures error handling
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(f"[DEBUG] Jac STDOUT:\n{result.stdout}")
        
        # Read generated docs (assuming the Jac script outputs to this fixed location)
        # Note: The Jac script uses os.getcwd() for its output path base, 
        # which might be different from Path(__file__).parent. This assumes the CWD 
        # when server.py runs is the project root (BE parent).
        docs_path = Path(__file__).parent / "outputs" / repo_name / "docs.md"
        docs_content = "No documentation generated."
        if docs_path.exists():
            with open(docs_path, "r", encoding="utf-8") as f:
                docs_content = f.read()

        return jsonify({"reports": [{"title": repo_name, "content": docs_content}]}), 200

    except subprocess.CalledProcessError as e:
        # Include stderr in the response for better debugging
        error_message = f"Jac execution failed with exit code {e.returncode}.\nSTDOUT: {e.stdout}\nSTDERR: {e.stderr}"
        return jsonify({"error": error_message}), 500
    except Exception as e:
        return jsonify({"error": f"Failed: {str(e)}"}), 500
    finally:
        # Clean up temporary clone
        shutil.rmtree(tmp_dir, ignore_errors=True)

# -------------------------------------------
# 2. Fetch all generated docs
# -------------------------------------------
@app.route("/walker/get_all_docs", methods=["POST"])
def get_all_docs():
    try:
        # Assuming 'outputs' is relative to the directory containing server.py
        outputs_dir = Path(__file__).parent / "outputs"
        if not outputs_dir.exists():
            return jsonify({"reports": []}), 200
            
        docs = []

        for repo_dir in outputs_dir.iterdir():
            if not repo_dir.is_dir():
                continue
            docs_file = repo_dir / "docs.md"
            if docs_file.exists():
                with open(docs_file, "r", encoding="utf-8") as f:
                    docs.append({"title": repo_dir.name, "content": f.read()})

        return jsonify({"reports": docs}), 200
    except Exception as e:
        return jsonify({"error": f"Failed to load docs: {e}"}), 500

# -------------------------------------------
# 3. Fetch all diagrams
# -------------------------------------------
@app.route("/walker/get_all_diagrams", methods=["POST"])
def get_all_diagrams():
    try:
        outputs_dir = Path(__file__).parent / "outputs"
        if not outputs_dir.exists():
            return jsonify({"reports": []}), 200
            
        diagrams = []

        for repo_dir in outputs_dir.iterdir():
            if not repo_dir.is_dir():
                continue
            # Note: The Jac script seems to output to the docs.md file, 
            # but this endpoint looks for a separate diagram.mmd file. 
            # We'll assume the naming convention holds for now.
            diagram_file = repo_dir / "diagram.mmd" 
            if diagram_file.exists():
                with open(diagram_file, "r", encoding="utf-8") as f:
                    diagrams.append({"title": repo_dir.name, "content": f.read()})

        return jsonify({"reports": diagrams}), 200
    except Exception as e:
        return jsonify({"error": f"Failed to load diagrams: {e}"}), 500

# -------------------------------------------
# Entry point
# -------------------------------------------
if __name__ == "__main__":
    print(f"Codebase Genius backend running on http://127.0.0.1:{PORT}")
    app.run(host="127.0.0.1", port=PORT)