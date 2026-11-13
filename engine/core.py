"""core.py · paths, file io, the exercise bank, the program files, the profile.

Standard library only. Every other engine file imports from here.
The machine part of every markdown file (profile, plan, program, module) is the FIRST
fenced block marked json. Everything outside that block is for people.
"""
import csv, datetime, json, pathlib, re

ROOT = pathlib.Path(__file__).resolve().parent.parent
ME = ROOT / "me"
SESSIONS = ROOT / "sessions"
DOCTRINE = ROOT / "doctrine"
PROGRAMS = DOCTRINE / "programs"
MODULES = DOCTRINE / "modules"
BANK = DOCTRINE / "exercises" / "bank.csv"

PROFILE = ME / "PROFILE.md"
PLAN = ME / "PLAN.md"
STATE = ME / "state.json"
LOG = ME / "log.jsonl"
LOGMD = ME / "LOG.md"

GOALS = ["muscle", "strength", "powerlifting", "weightlifting", "functional", "hyrox",
         "run", "skills", "fat_loss", "health", "independent"]
EXPERIENCE = ["none", "novice", "intermediate", "advanced"]
LEVEL_TARGET = {"none": 1, "novice": 2, "intermediate": 3, "advanced": 4}
LEVEL_CAP = {"none": 2, "novice": 3, "intermediate": 4, "advanced": 5}
AGE_BANDS = ["under_18", "18_39", "40_59", "60_74", "75_plus"]

# Equipment presets a person ticks at onboarding, expanded to tags the bank uses.
MACHINES = ["cable", "lat_pulldown", "leg_press", "leg_curl", "leg_extension",
            "chest_press_machine", "row_machine", "pec_deck", "smith"]
CARDIO = ["rower", "bike", "treadmill"]
PRESETS = {
    "full_gym": ["bodyweight", "pullup_bar", "dip_bars", "bench", "box", "band", "dumbbell",
                 "kettlebell", "barbell", "rack", "plates", "ez_bar", "trap_bar", "med_ball",
                 "outdoors"] + MACHINES + CARDIO,
    "basic_gym": ["bodyweight", "pullup_bar", "bench", "dumbbell", "barbell", "rack", "plates",
                  "cable", "lat_pulldown", "leg_press", "treadmill", "bike", "outdoors"],
    "home_dumbbells": ["bodyweight", "dumbbell", "band", "outdoors"],
    "home_bodyweight": ["bodyweight", "outdoors"],
    "park": ["bodyweight", "pullup_bar", "dip_bars", "outdoors"],
    "crossfit_box": ["bodyweight", "pullup_bar", "rings", "box", "bench", "band", "dumbbell", "kettlebell",
                     "barbell", "rack", "plates", "med_ball", "rower", "bike", "skierg",
                     "jump_rope", "sandbag", "outdoors"],
}
ALL_TAGS = sorted(set(sum(PRESETS.values(), [])) | {"rings", "skierg", "sled", "sandbag",
                                                   "jump_rope", "mini_band", "suspension"})


def today():
    return datetime.date.today().isoformat()


def read_json_block(path):
    """The first ```json block of a markdown file, parsed. None if the file or block is missing."""
    p = pathlib.Path(path)
    if not p.exists():
        return None
    m = re.search(r"```json\s*\n(.*?)\n```", p.read_text(encoding="utf-8"), re.S)
    if not m:
        return None
    return json.loads(m.group(1))


def write_json_block(path, data, prose):
    """Write a markdown file: the prose for people, then the json block for the engine."""
    body = prose.rstrip() + "\n\n## The data (the engine reads this block)\n\n```json\n" + \
        json.dumps(data, indent=2, ensure_ascii=False) + "\n```\n"
    pathlib.Path(path).write_text(body, encoding="utf-8")


def load_json(path, default=None):
    p = pathlib.Path(path)
    if not p.exists():
        return default
    return json.loads(p.read_text(encoding="utf-8"))


def save_json(path, data):
    pathlib.Path(path).write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def read_log():
    if not LOG.exists():
        return []
    return [json.loads(l) for l in LOG.read_text(encoding="utf-8").splitlines() if l.strip()]


# · the bank

def _split(v, sep=";"):
    return [x.strip() for x in (v or "").split(sep) if x.strip()]


def load_bank():
    rows = {}
    with open(BANK, newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            r = {k: (v or "").strip() for k, v in r.items()}
            r["muscles_primary"] = _split(r["muscles_primary"])
            r["muscles_secondary"] = _split(r["muscles_secondary"])
            r["equipment"] = [_split(alt, "+") for alt in _split(r["equipment"], "|")]
            r["regions"] = _split(r["regions"])
            r["tags"] = _split(r["tags"])
            r["level"] = int(r["level"] or 1)
            r["needs_coaching"] = r["needs_coaching"] == "yes"
            r["impact"] = r["impact"] == "yes"
            rows[r["id"]] = r
    return rows


def has_equipment(row, tags):
    """True if any equipment alternative of the row is fully covered by the tags."""
    tags = set(tags)
    return any(set(alt) <= tags for alt in row["equipment"])


def expand_equipment(items):
    out = set()
    for it in items or []:
        out |= set(PRESETS.get(it, [it]))
    out.add("bodyweight")
    return sorted(out)


# · programs and modules

def load_program(pid):
    p = PROGRAMS / (pid + ".md")
    data = read_json_block(p)
    if data is None:
        raise SystemExit("No program file for '%s' (looked for %s)." % (pid, p.relative_to(ROOT)))
    return data


def all_programs():
    out = []
    for p in sorted(PROGRAMS.glob("*.md")):
        if p.name == "README.md":
            continue
        d = read_json_block(p)
        if d:
            out.append(d)
    return out


def load_module(mid):
    d = read_json_block(MODULES / (mid + ".md"))
    if d is None:
        raise SystemExit("No module file for '%s'." % mid)
    return d


# · profile, plan, state

def profile():
    return read_json_block(PROFILE)


def plan():
    return read_json_block(PLAN)


def state():
    return load_json(STATE)


def place_tags(prof, place=None):
    places = prof.get("places") or {}
    key = place or prof.get("default_place") or (list(places)[0] if places else None)
    pl = places.get(key, {}) if key else {}
    return expand_equipment(pl.get("equipment", []))


def kg_round_down(kg, step):
    if kg is None:
        return None
    step = step or 2.5
    return round((int(kg / step + 1e-9)) * step, 2)


def fmt_load(kg, units="kg"):
    if kg is None:
        return ""
    if units == "lb":
        lb = kg * 2.20462
        return "%g lb" % (round(lb / 5) * 5)
    return ("%g kg" % round(kg, 2))
