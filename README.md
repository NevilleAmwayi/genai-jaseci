🧠 Codebase Genius — Backend (Jac + Python)

Codebase Genius is an AI-powered code understanding and documentation tool.
This backend service automatically clones a public GitHub repository, analyzes its code structure, builds a Code Context Graph (CCG), and generates a well-formatted Markdown documentation complete with a Mermaid diagram showing relationships between files, functions, and classes.

🚀 Features

🧩 Repository Cloning — Automatically clones any public GitHub repo.

🧠 Static Code Analysis — Extracts classes, functions, and relationships using Python’s AST module.

🌲 File Tree Visualization — Produces a JSON-style map of all files and folders.

🗂️ Code Context Graph (CCG) — Represents structural relationships between code entities.

🪄 Auto-Documentation — Generates a Markdown file (docs.md) summarizing the project.

🖼️ Mermaid Diagram Generation — Visualizes CCG as an interactive diagram.

⚙️ Flask API Bridge — Trigger the Jac pipeline via a REST API endpoint.

🧩 Project Structure
assignment2/
│
├── .env                     # Environment variables (e.g., API keys)
├── .gitignore               # Git ignore rules
├── README.md                # Full documentation
├── requirements.txt         # Dependencies
│
├── BE/                      # Backend
│   │
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── main.jac
│   │   ├── repo_mapper.jac
│   │   ├── code_analyzer.jac
│   │   └── docgenie.jac
│   │
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── clone_repo.py
│   │   ├── parse_code.py
│   │   ├── diagram_utils.py
│   │   ├── io_utils.py
│   │   └── log_utils.py
│   │
│   ├── outputs/             # Auto-generated repo docs
│   └── server.py            # Flask API bridge
│
└── FE/                      # Frontend (Streamlit)
    └── app.py

⚙️ Installation
1. Clone this project
git clone https://github.com/<your-username>/codebase-genius-backend.git
cd codebase-genius-backend

2. Create a virtual environment
python -m venv .env
source .env/bin/activate    # (Linux/Mac)
.env\Scripts\activate       # (Windows)

3. Install dependencies
pip install -r requirements.txt

▶️ Usage
Run the Flask API
python BE/server.py


Flask will start on port 8000.

Trigger Documentation Generation

Send a POST request to /generate:

curl -X POST http://localhost:8000/generate \
     -H "Content-Type: application/json" \
     -d '{"repo_url": "https://github.com/<user>/<repo>"}'


✅ The backend will:

Clone the target repository

Build its file tree and summary

Analyze all Python files

Generate a Markdown documentation file

Save it to:

BE/outputs/<repo_name>/docs.md


🧪 Example End-to-End Run
# 1. Start the backend
python backend/server.py

# 2. Trigger analysis
curl -X POST http://localhost:5000/generate \
     -H "Content-Type: application/json" \
     -d '{"repo_url":"https://github.com/NevilleAmwayi/control_flows_and_functions_py"}'

# 3. View results
cat backend/outputs/control_flows_and_functions_py/docs.md

🧑‍💻 Contributing

Contributions are welcome!
To add new analyzers or extend documentation features:

Fork this repo

Create a feature branch (feature/add-new-parser)

Commit and push your changes

Open a Pull Request


👨‍💻 Author

Neville Shem Amwayi