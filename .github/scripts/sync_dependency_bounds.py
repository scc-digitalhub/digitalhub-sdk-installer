import re
import sys
import tomllib
from pathlib import Path


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("Usage: sync_dependency_bounds.py VERSION")

    version_match = re.fullmatch(r"(\d+)\.(\d+)\.\d+(?:[a-zA-Z]+\d*)?", sys.argv[1])
    if version_match is None:
        raise SystemExit(f"Unsupported release version: {sys.argv[1]}")

    major, minor = (int(part) for part in version_match.groups())
    lower_bound = f"{major}.{minor}.0"
    upper_bound = f"{major}.{minor + 1}"

    pyproject_path = Path("pyproject.toml")
    pyproject_text = pyproject_path.read_text(encoding="utf-8")
    project_data = tomllib.loads(pyproject_text)
    dependencies = project_data["project"]["dependencies"]
    for extra_dependencies in project_data["project"].get("optional-dependencies", {}).values():
        dependencies.extend(extra_dependencies)

    digitalhub_dependencies = [
        dependency for dependency in dependencies if dependency.startswith("digitalhub")
    ]
    constraint_pattern = re.compile(r">=\d+\.\d+\.\d+,\s*<\d+\.\d+")
    updated_text, count = constraint_pattern.subn(
        f">={lower_bound}, <{upper_bound}",
        pyproject_text,
    )
    if count != len(digitalhub_dependencies):
        raise SystemExit(
            "Expected one version constraint for each Digitalhub dependency "
            f"({len(digitalhub_dependencies)}), found {count}"
        )

    pyproject_path.write_text(updated_text, encoding="utf-8")
    print(f"Updated {count} Digitalhub dependency constraints for release line {major}.{minor}.")


if __name__ == "__main__":
    main()
