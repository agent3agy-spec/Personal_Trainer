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
AGE_BAND = "18_39"            # the audience is adults 18 to 40: age is never asked, the engine fixes the band (00_MISSION.md)
REGIONS = ["knee", "hip", "low_back", "shoulder", "elbow", "wrist", "ankle", "neck"]

# The interview of 13 nov 2026 (doctrine/02_INTERVIEW.md). The person never picks a method or a style: they say what they
# want, what they have done, what they enjoy, and the engine decides the plan (doctrine/03_MATRIX.md).
MODES = ["new", "improve"]
# outcome -> follow-up -> (goal, goal2). OUTCOME_DEFAULT is the follow-up when they skip it.
OUTCOMES = {
    "look": {"size": ("muscle", None), "lean": ("fat_loss", "muscle")},
    "strong": {"general": ("strength", None), "powerlifting": ("powerlifting", None), "olympic": ("weightlifting", None)},
    "athletic": {"crossfit": ("functional", None), "hybrid": ("functional", "run")},
    "event": {"run_5k_10k": ("run", None), "run_half": ("run", None), "run_marathon": ("run", None),
              "hyrox": ("hyrox", None), "meet": ("powerlifting", None)},
    "keep_going": {"lifting": ("muscle", "strength"), "fitness": ("functional", "health"), "mix": ("health", "muscle")},
}
OUTCOME_DEFAULT = {"look": "size", "strong": "general", "athletic": "crossfit", "event": "run_5k_10k", "keep_going": "mix"}
# Outcomes no program is built for: routed to the closest, with this honest line (03_MATRIX.md Step 5).
OUTCOME_GAP = {
    "run_marathon": "No plan here is built for a marathon yet. You get the running base plan: it builds the easy running a "
                    "marathon stands on, up to half marathon distance.",
    "keep_going": "No plan here is built around monthly challenges yet. You get the closest steady plan, and every sheet has a "
                  "number to beat: that is your challenge each session.",
}
# What they have done regularly, as activities, never as a method. Also the keys of experience_by.
ACTIVITIES = ["lifting", "running", "cardio", "classes", "crossfit"]
# What they enjoy or can't stand doing, in plain activity words. An adherence input only.
ENJOY = ["heavy", "pump", "circuits", "long_cardio", "running"]
KIT_PREF = ["free_weights", "machines", "either"]
SPLITS = ["ppl", "upper_lower", "full_body", "body_part", "strength_cardio", "run_plan", "classes", "custom"]
ROUTINE_AGE = ["under_1m", "1_3m", "3_12m", "over_1y"]
ROUTINE_STALLS = ["lift_stuck", "not_growing", "tired", "bored", "skipping", "pain", "fine"]
ROUTINE_KEEP = ["split", "exercises", "days", "pump", "short", "everything"]
STRENGTHS = ["strong", "engine", "flexible", "technique", "consistent"]
BARRIERS = ["time", "motivation", "energy", "stress", "pain", "know_how", "bored"]
LIMIT_STATUS = ["now", "mild", "cleared", "unchecked"]           # mild: only on some moves, trained with care
TRIGGERS = ["bending", "overhead", "impact", "kneeling", "gripping", "twisting"]
SLEEP = ["under_6", "6_7", "7_plus"]
STRESS = ["low", "medium", "high"]
# A preferred training style: asked only of experienced people (intermediate or advanced, or the improve path).
# "trainer" means let the trainer decide, the default. Beginners are never asked (02_INTERVIEW.md).
STYLES = ["trainer", "strength", "bodybuilding", "powerbuilding", "crossfit", "hyrox", "running", "hybrid"]
REJECT_REASONS = ["too_long", "too_much_running", "not_enjoy", "days"]
MINUTES_RANGE = (15, 120)

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

# The scope (doctrine/00_MISSION.md): a gym, a home gym with real kit, or outdoors for running and cardio.
# `home_bodyweight` and `park` stay above for old profiles and the travel day; nobody can choose them as a place.
OFFERED_PRESETS = ["full_gym", "basic_gym", "crossfit_box"]
NOT_OFFERED = {"home_bodyweight", "park"}
REAL_KIT = {"barbell", "dumbbell", "rower", "bike", "skierg", "treadmill", "sled", "cable", "lat_pulldown",
            "leg_press", "smith", "chest_press_machine", "row_machine"}      # a kettlebell or bands alone are not a home gym
CARDIO_ONLY = {"bodyweight", "outdoors", "jump_rope"}


def place_in_scope(equipment):
    """A place someone may train at: real kit (a gym or a home gym), or outdoors for running and cardio only."""
    if set(equipment or []) & NOT_OFFERED:
        return False
    tags = set(expand_equipment(equipment))
    return bool(tags & REAL_KIT) or ("outdoors" in tags and tags <= CARDIO_ONLY)


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


LB_PER_KG = 2.20462


def lb_to_kg(lb):
    return None if lb is None else round(float(lb) / LB_PER_KG, 3)


def fmt_load(kg, units="kg"):
    """A stored load (always kilograms) in the person's own unit. Pound users train on a pound grid
    (build.load_ctx), so whole pounds are exact; a half pound they typed themselves survives."""
    if kg is None:
        return ""
    if units == "lb":
        lb = kg * LB_PER_KG
        half = round(lb * 2) / 2
        return "%g lb" % (half if abs(lb - half) < 0.05 else round(lb))
    return ("%g kg" % round(kg, 2))
