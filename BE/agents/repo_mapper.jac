# repo_mapper.jac
import from byllm.llm { Model }
glob llm = Model(model_name="gemini/gemini-2.0-flash", verbose=False);


node RepoMapper {
    def generate_file_tree(repo_path: str) -> str;
    def summarize_readme(repo_path: str) -> str;
}

sem RepoMapper.generate_file_tree = "Produce a JSON map of files and folders in the repo. Ignore .git, node_modules, __pycache__, .venv, .env.";
sem RepoMapper.summarize_readme = "Read README.md and produce a concise 5-8 sentence summary suitable for a project overview.";


impl RepoMapper.generate_file_tree {
    py_mod = import_py_module("BE.utils.parse_code");
    return py_mod.generate_file_tree(repo_path);
}

impl RepoMapper.summarize_readme {
    # Use the simple summariser in parse_code; later this could call an LLM
    py_mod = import_py_module("BE.utils.parse_code");
    return py_mod.summarize_readme(repo_path);
}