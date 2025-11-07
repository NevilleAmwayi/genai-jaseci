# main.jac
import from byllm.llm { Model }
import os;
import from dotenv { load_dotenv }
include ../utils/clone_repo;
include ../utils/parse_code;
include repo_mapper.jac;
include code_analyzer.jac;
include docgenie.jac;


load_dotenv();

glob llm = Model(model_name="gemini/gemini-2.0-flash", verbose=False);


# -------------------------------------------
# Node definitions
# -------------------------------------------

node Repo {
    has url: str = "";
    has local_path: str = "";
}

node CodeGenius {
    has repo_url: str = "";
    has repo_path: str = "";
    has file_tree: str = "";
    has readme_summary: str = "";
    has ccg: str = "";
    has docs_path: str = "";


    def clone_repository(repo_url: str) -> str;
    def map_repository(repo_path: str) -> str;
    def analyze_code(repo_path: str) -> str;
    def generate_docs(repo_path: str) -> str;


    def run_pipeline(repo_url: str) -> str;


    can execute with codebase_entry(visitor) {
        print("CodeGenius: received request to process -> " + visitor.repo_url);
        self.repo_url = visitor.repo_url;
        result = self.run_pipeline(self.repo_url);
        report { "status": result };
    }
}

# -------------------------------------------
# Semantics (instructions for LLM-driven methods)
# -------------------------------------------


sem CodeGenius.clone_repository = "Clone the given public GitHub repository URL into a local directory under backend/outputs and return the absolute path. Handle errors gracefully.";
sem CodeGenius.map_repository = "Produce a JSON-style file tree and a README summary for planning analysis."
sem CodeGenius.analyze_code = "Construct a Code Context Graph (CCG) capturing functions, classes and basic call/relationship info for Python files."
sem CodeGenius.generate_docs = "Produce a well-structured markdown document (docs.md) under backend/outputs/<repo>/docs.md including README summary, file map, API reference, and a Mermaid diagram generated from the CCG."
sem CodeGenius.run_pipeline = "Run tasks in order: clone -> map -> analyze -> docs. Report progress and errors."


# -------------------------------------------
# Implementations (impl blocks)
# -------------------------------------------

impl CodeGenius.clone_repository {
    # Use Python helper to clone
    py_mod = import_py_module("BE.utils.clone_repo");
    try {
        path = py_mod.clone_repo(repo_url);
    } else {
        path = "";
    }
    self.repo_path = path;
    return path;
}

impl CodeGenius.map_repository {
    py_mod = import_py_module("BE.utils.parse_code");
    file_tree = py_mod.generate_file_tree(repo_path);
    readme_summary = py_mod.summarize_readme(repo_path);
    self.file_tree = file_tree;
    self.readme_summary = readme_summary;
    return file_tree;
}

impl CodeGenius.analyze_code {
    py_mod = import_py_module("BE.utils.parse_code");
    ccg = py_mod.build_ccg(repo_path);
    self.ccg = ccg;
    return ccg;
}



impl CodeGenius.generate_docs {
    py_diag = import_py_module("BE.utils.diagram_utils");
    py_io = import_py_module("BE.utils.io_utils");


    # Prepare output path
    repo_name = repo_path.rstrip('/').split('/')[-1];
    out_dir = os.path.join(os.getcwd(), "BE", "outputs", repo_name);
    py_io.ensure_dir(out_dir);


    mermaid = py_diag.generate_mermaid_diagram(self.ccg);


    markdown = [];
    markdown.append(f"# {repo_name} — Documentation (generated)");
    markdown.append("\n## Overview\n");
    markdown.append(self.readme_summary or "No README available.");
    markdown.append("\n## File Tree\n");
    markdown.append("```json\n" + self.file_tree + "\n```");
    markdown.append("\n## Code Context Graph (CCG)\n");
    markdown.append("```json\n" + self.ccg + "\n```");
    markdown.append("\n## Diagram\n");
    markdown.append(mermaid);


    docs_text = "\n\n".join(markdown);
    docs_path = os.path.join(out_dir, "docs.md");
    py_io.write_text_file(docs_path, docs_text);
    self.docs_path = docs_path;
    return docs_path;
}

impl CodeGenius.run_pipeline {
    # Step 1: clone
    print("Step 1: Cloning repository...");
    path = self.clone_repository(repo_url);
    if path == "" {
    return "error: clone failed";
    }


    # Step 2: map
    print("Step 2: Mapping repository...");
    self.map_repository(path);


    # Step 3: analyze
    print("Step 3: Analyzing code (building CCG)...");
    self.analyze_code(path);


    # Step 4: generate docs
    print("Step 4: Generating documentation...");
    docs = self.generate_docs(path);


    return "done: docs saved at " + docs;
}