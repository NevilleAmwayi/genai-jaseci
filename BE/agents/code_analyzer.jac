# code_analyzer.jac
import from byllm.llm { Model }
glob llm = Model(model_name="gemini/gemini-2.0-flash", verbose=False);


node CodeAnalyzer {
    def build_ccg(repo_path: str) -> str;
    def query_ccg(query: str) -> str;
}

sem CodeAnalyzer.build_ccg = "Parse Python files and return JSON listing functions, classes and simple relationships (calls/inherits).";
sem CodeAnalyzer.query_ccg = "Answer queries about relationships in the CCG, e.g. 'Which functions call train_model?'.";


impl CodeAnalyzer.build_ccg {
    py_mod = import_py_module("BE.utils.parse_code");
    return py_mod.build_ccg(repo_path);
}

impl CodeAnalyzer.query_ccg {
    # A lightweight query via Python helper for now
    py_mod = import_py_module("BE.utils.parse_code");
    return py_mod.query_ccg(query);
}