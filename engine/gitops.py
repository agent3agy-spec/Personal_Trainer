"""gitops.py · the only place the trainer touches git. Memory is committed to main, always (doctrine/07_WORKFLOW.md).

On Claude Code on the web (CLAUDE_CODE_REMOTE=true) a session works on its own branch. A new web
session starts from main, so the trainer also pushes its work to main, or the next session forgets.
"""
import json, os, subprocess, urllib.request
import core

DATA = ["me", "sessions"]


def git(*args, check=False):
    r = subprocess.run(["git"] + list(args), cwd=str(core.ROOT), capture_output=True, text=True)
    if check and r.returncode:
        raise RuntimeError(r.stderr.strip())
    return r


def is_repo():
    return git("rev-parse", "-" * 2 + "is-inside-work-tree").returncode == 0


def branch():
    return git("rev-parse", "-" * 2 + "abbrev-ref", "HEAD").stdout.strip()


def default_branch():
    r = git("symbolic-ref", "refs/remotes/origin/HEAD")
    if r.returncode == 0:
        return r.stdout.strip().rsplit("/", 1)[-1]
    return "main"


def has_remote():
    return bool(git("remote").stdout.strip())


def commit(message, push=True):
    """Checks first, then add only me/ and sessions/, commit, push. Returns a short status line."""
    import checks
    errs = checks.check_data()
    if errs:
        return {"ok": False, "status": "not committed: the memory files failed their check", "errors": errs}
    if not is_repo():
        return {"ok": True, "status": "saved (this folder is not a git repository, so nothing was committed)"}
    git("add", "-A", *DATA)
    if not git("diff", "-" * 2 + "cached", "-" * 2 + "quiet").returncode:
        return {"ok": True, "status": "nothing new to commit"}
    r = git("commit", "-m", message)
    if r.returncode:
        if "user.email" in r.stderr or "identity" in r.stderr:
            git("config", "user.email", "trainer@localhost")
            git("config", "user.name", "Personal trainer")
            r = git("commit", "-m", message)
        if r.returncode:
            return {"ok": False, "status": "commit failed: " + r.stderr.strip()[:200]}
    out = {"ok": True, "status": "committed: " + message}
    if push and has_remote():
        cur, main = branch(), default_branch()
        p = git("push", "origin", "HEAD")
        if os.environ.get("CLAUDE_CODE_REMOTE") == "true" and cur != main:
            p2 = git("push", "origin", "HEAD:" + main)
            out["pushed_main"] = p2.returncode == 0
            if p2.returncode:
                out["warning"] = ("saved on this session's branch but NOT on %s: the next web session would not see it. "
                                  "Merge this branch on GitHub, or train from a computer." % main)
        out["pushed"] = p.returncode == 0
        if p.returncode:
            out["status"] += " · not pushed yet (offline or not signed in), it will go next time"
    return out


def visibility():
    """public · private · unknown. One unauthenticated request to the GitHub API: an answer means public."""
    url = git("remote", "get-url", "origin").stdout.strip()
    if "github.com" not in url:
        return "unknown"
    slug = url.split("github.com")[-1].lstrip(":/").replace(".git", "")
    try:
        req = urllib.request.Request("https://api.github.com/repos/" + slug, headers={"User-Agent": "personal-trainer"})
        with urllib.request.urlopen(req, timeout=8) as r:
            return "public" if json.loads(r.read().decode()).get("private") is False else "private"
    except urllib.error.HTTPError as e:
        return "private" if e.code == 404 else "unknown"
    except Exception:
        return "unknown"


def file_url(rel, ref=None):
    """The GitHub page of a file in this copy, so the person can open the PDF on their phone. None if unknown."""
    import urllib.parse
    url = git("remote", "get-url", "origin").stdout.strip()
    if "github.com" not in url:
        return None
    slug = url.split("github.com")[-1].lstrip(":/").replace(".git", "")
    slug = "/".join(slug.split("/")[-2:])
    return "https://github.com/%s/blob/%s/%s" % (slug, ref or default_branch(), urllib.parse.quote(str(rel)))
