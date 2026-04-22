from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]   # /workspace
SRC_DIR = BASE_DIR / "src"
DATA_DIR = BASE_DIR / "sample_data"

RESULTS_DIR = SRC_DIR / "results"


RESULTS_DIR.mkdir(exist_ok=True)

def get_results_path(filename):
    return RESULTS_DIR / filename