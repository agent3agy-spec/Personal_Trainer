"""gitops_web.py · stands in for engine/gitops.py when the trainer runs inside a web page.

The page has no git and no GitHub. Memory is the browser's: after every command the page copies
me/ and sessions/ into the device's storage. So "commit" only runs the same data check the real
one runs, and says saved. engine/gitops.py stays the one used by the terminal path.
"""
import core

DATA = ["me", "sessions"]


class _Done:
    returncode = 1
    stdout = ""
    stderr = "no git in the web trainer"


def git(*args, check=False):
    if check:
        raise RuntimeError(_Done.stderr)
    return _Done()


def is_repo():
    return False


def branch():
    return "main"


def default_branch():
    return "main"


def has_remote():
    return False


def commit(message, push=True):
    import checks
    errs = checks.check_data()
    if errs:
        return {"ok": False, "status": "not saved: the memory files failed their check", "errors": errs}
    return {"ok": True, "status": "saved on this device"}


def visibility():
    return "private"


def file_url(rel, ref=None):
    return None
