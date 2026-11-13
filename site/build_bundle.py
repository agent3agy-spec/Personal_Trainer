"""build_bundle.py · packs the engine and the doctrine into site/bundle.json for the web trainer.

    python3 site/build_bundle.py

The page writes every entry into its own Python filesystem, so the engine runs unchanged.
engine/gitops.py is swapped for site/py/gitops_web.py in the bundle only, never on disk.
"""
import json, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
TEXT = {".py", ".md", ".css", ".csv", ".json", ""}


def pack():
    files = {}
    for top in ("engine", "doctrine"):
        for p in sorted((ROOT / top).rglob("*")):
            if p.is_file() and p.suffix in TEXT and "__pycache__" not in p.parts and "_out_of_scope" not in p.parts:
                files[p.relative_to(ROOT).as_posix()] = p.read_text(encoding="utf-8")
    files["engine/gitops.py"] = (ROOT / "site" / "py" / "gitops_web.py").read_text(encoding="utf-8")
    version = (ROOT / "VERSION").read_text(encoding="utf-8").strip() if (ROOT / "VERSION").exists() else "dev"
    return {"version": version, "files": files}


if __name__ == "__main__":
    b = pack()
    out = ROOT / "site" / "bundle.json"
    out.write_text(json.dumps(b, ensure_ascii=False), encoding="utf-8")
    print("%d files, %d KB -> %s" % (len(b["files"]), out.stat().st_size // 1024, out.relative_to(ROOT)))
    sys.exit(0)
