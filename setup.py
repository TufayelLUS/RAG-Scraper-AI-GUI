import sys
from cx_Freeze import setup, Executable

base = None

if sys.platform == "win32":
    base = "Win32GUI"  # Use this option to create a GUI executable on Windows
# set the name of the python script below
executables = [Executable("RAG Scraper.py", base=base)]
# if you want to show the console, use the line below instead and comment out the line above
# executables = [Executable("python_file_name.py", base="Console")]

options = {
    "build_exe": {
        "optimize": 2, # set level of optimization 0-2
        "packages": ["chromadb", "chromadb.api.segment", "chromadb.execution.executor.local", "pydantic", "pydantic.deprecated.decorator", "chromadb.utils.embedding_functions.onnx_mini_lm_l6_v2", "onnxruntime", "opentelemetry", "opentelemetry.context.contextvars_context", "chromadb.telemetry.product.posthog", "chromadb.segment.impl.metadata.sqlite"],  # List of packages to include
        "includes": ["chromadb.quota.simple_quota_enforcer", "chromadb.telemetry.opentelemetry"],
        "include_files": [],  # List of additional files to include
    },
}

setup(
    name="RAG Scraper AI by Tufayel", # name of the process
    version="1.0",
    description="RAG Scraper AI that reads a PDF/URL and answers questions", # description of the process
    options=options,
    executables=executables
)