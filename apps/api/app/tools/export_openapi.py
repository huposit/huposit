import json
import sys
from pathlib import Path

from app.main import app

ROOT_DIR = Path(__file__).resolve().parents[4]
DEFAULT_OUTPUT_PATH = ROOT_DIR / "generated" / "openapi.json"


def export_openapi(output_path: Path = DEFAULT_OUTPUT_PATH) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(app.openapi(), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def main() -> None:
    output_path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_OUTPUT_PATH
    export_openapi(output_path)


if __name__ == "__main__":
    main()
