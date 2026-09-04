#!/usr/bin/env python3
# /// script
# dependencies = ["pyyaml"]
# ///
"""Smoke-test a copied standards-advisor package in a temporary project."""

import argparse
import csv
import json
import subprocess
import tempfile
from pathlib import Path

import yaml


def run(command: list[str]) -> None:
    subprocess.run(command, check=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--skill-root",
        default=str(Path(__file__).resolve().parents[1]),
        help="Path to the copied standards-advisor skill",
    )
    args = parser.parse_args()

    skill_root = Path(args.skill_root).resolve()
    required_files = [
        skill_root / "SKILL.md",
        skill_root / "assets/module.yaml",
        skill_root / "assets/module-help.csv",
        skill_root / "scripts/merge-config.py",
        skill_root / "scripts/merge-help-csv.py",
        skill_root / "standards/index.yaml",
    ]
    missing = [str(path) for path in required_files if not path.is_file()]
    if missing:
        raise SystemExit("Missing install files:\n" + "\n".join(missing))

    catalog = yaml.safe_load((skill_root / "standards/index.yaml").read_text(encoding="utf-8"))
    for standard in catalog.get("standards", []):
        for field in ("path", "checklist"):
            referenced_file = skill_root / "standards" / standard[field]
            if not referenced_file.is_file():
                raise SystemExit(f"Catalog reference is missing: {referenced_file}")

    with tempfile.TemporaryDirectory() as directory:
        project_root = Path(directory) / "project"
        bmad_root = project_root / "_bmad"
        answers_path = Path(directory) / "answers.json"
        bmad_root.mkdir(parents=True)
        answers_path.write_text(
            json.dumps(
                {
                    "core": {
                        "user_name": "BMad",
                        "communication_language": "English",
                        "document_output_language": "English",
                        "output_folder": "{project-root}/_bmad-output",
                    },
                    "module": {},
                }
            ),
            encoding="utf-8",
        )

        run(
            [
                "uv",
                "run",
                str(skill_root / "scripts/merge-config.py"),
                "--config-path",
                str(bmad_root / "config.yaml"),
                "--user-config-path",
                str(bmad_root / "config.user.yaml"),
                "--module-yaml",
                str(skill_root / "assets/module.yaml"),
                "--answers",
                str(answers_path),
            ]
        )
        run(
            [
                "uv",
                "run",
                str(skill_root / "scripts/merge-help-csv.py"),
                "--target",
                str(bmad_root / "module-help.csv"),
                "--source",
                str(skill_root / "assets/module-help.csv"),
                "--module-code",
                "stds",
            ]
        )

        for path in (
            bmad_root / "config.yaml",
            bmad_root / "config.user.yaml",
            bmad_root / "module-help.csv",
        ):
            if not path.is_file():
                raise SystemExit(f"Registration did not create {path}")

        with (bmad_root / "module-help.csv").open(newline="", encoding="utf-8") as file:
            rows = list(csv.DictReader(file))
        if not any(row.get("module") == "stds" for row in rows):
            raise SystemExit("Registration did not add the stds help entry")

    print("standards-advisor install smoke test passed")


if __name__ == "__main__":
    main()