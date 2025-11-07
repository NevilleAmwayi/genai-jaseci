# docgenie.jac
import from byllm.llm { Model }
import os;
glob llm = Model(model_name="gemini/gemini-2.0-flash", verbose=False);


node DocGenie {
    def create_markdown(repo_path: str) -> str;
}

sem DocGenie.create_markdown = "Using repo metadata, file-tree and CCG, synthesize a human-friendly Markdown document including installation, usage, API reference and diagrams.";


impl DocGenie.create_markdown {
    # In our design the heavy lifting is already in CodeGenius.generate_docs, so this can act as a thin wrapper
    cg = CodeGenius();
    cg.map_repository(repo_path);
    cg.analyze_code(repo_path);
    return cg.generate_docs(repo_path);
}