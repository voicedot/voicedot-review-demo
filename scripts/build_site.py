"""Copy the bounded static site and stamp the exact revision being deployed."""
import argparse
import datetime
import hashlib
import json
from pathlib import Path
import re
import shutil

ROOT = Path(__file__).resolve().parents[1]
ALLOWED = {"index.html", "needs-fix.html", "styles.css", "deployment.js", ".nojekyll"}


def build(commit, branch, destination):
    if not re.fullmatch(r"[a-f0-9]{40}", commit):
        raise ValueError("commit must be a complete Git commit SHA")
    if branch != "review":
        raise ValueError("Only the review branch is deployable")
    destination = Path(destination).resolve()
    if destination != ROOT / "dist":
        raise ValueError("Output must be this repository's dist directory")
    source = ROOT / "site"
    entries = list(source.iterdir())
    if {p.name for p in entries} != ALLOWED:
        raise ValueError("Unexpected file in site; update the explicit publisher allowlist first")
    for path in entries:
        if path.is_symlink() or not path.is_file() or path.stat().st_size > 500_000:
            raise ValueError(f"Not a bounded static file: {path.name}")
    destination.mkdir(exist_ok=True)
    for path in destination.iterdir():
        if path.is_dir() or path.is_symlink():
            raise ValueError("Unexpected directory/link in output; inspect it manually")
        path.unlink()
    assets = {}
    for name in ("styles.css", "deployment.js"):
        digest = hashlib.sha256((source / name).read_bytes()).hexdigest()[:16]
        assets[name] = f"{Path(name).stem}.{digest}{Path(name).suffix}"
    manifest_name = f"deployment.{commit}.json"
    for path in entries:
        if path.suffix == ".html":
            html = path.read_text()
            for name, versioned in assets.items():
                html = html.replace(f'./{name}"', f'./{versioned}"')
            html = html.replace('id="deployment-commit"',
                                f'id="deployment-commit" data-manifest="./{manifest_name}"')
            (destination / path.name).write_text(html)
        else:
            shutil.copyfile(path, destination / assets.get(path.name, path.name))
    manifest = json.dumps({
        "commit": commit,
        "branch": branch,
        "builtAt": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    }, indent=2) + "\n"
    (destination / "deployment.json").write_text(manifest)
    (destination / manifest_name).write_text(manifest)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--commit", required=True)
    parser.add_argument("--branch", required=True)
    args = parser.parse_args()
    build(args.commit, args.branch, ROOT / "dist")
