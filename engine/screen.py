"""screen.py · the safety screen before any program (doctrine/01_SAFETY.md).

The answers file (written by the coach from what the person said):
  {"items": [1, 4],            the numbers of the checklist that apply (empty list: none)
   "age_band": "18_39",
   "cleared": false,           they say a doctor or qualified professional cleared them
   "provider_ok": false,       pregnant or postpartum: their midwife or doctor has no objection
   "doctor_ok": false}         diabetes with low-sugar risk: their doctor agreed

The checklist (the coach shows it numbered, in the person's language):
  1 a doctor said you have a heart condition or high blood pressure          (PAR-Q+ 1)
  2 chest pain at rest, in daily life, or when you are active               (PAR-Q+ 2)
  3 you lose balance from dizziness, or fainted, in the last 12 months      (PAR-Q+ 3)
  4 another chronic condition diagnosed                                     (PAR-Q+ 4)
  5 you take medication for a chronic condition                             (PAR-Q+ 5)
  6 a bone, joint or soft tissue problem that activity could make worse     (PAR-Q+ 6)
  7 a doctor said you should only exercise under medical supervision        (PAR-Q+ 7)
  8 you are pregnant
  9 you gave birth in the last 12 months
  10 diabetes treated with insulin or tablets that can cause low blood sugar
  11 an eating disorder, now or in the past
  12 a doctor said you have low bone density (osteoporosis or osteopenia)
PAR-Q+ structure [checked], items 2 to 7 wording [believe, copied from the official form at M2].
"""
PARQ = {1, 2, 3, 4, 5, 6, 7}
HARD = {2, 3}        # symptoms: no clearance by self report alone is enough for vigorous work, so the
                     # coach always shows the stop message first, even when "cleared" is true

MESSAGES = {
    "under_18": "This trainer is for adults (18 and over) for now. A coach at your school or club is the right person to build your training.",
    "parq": "Thanks for being straight with me. Before I build anything, one of your answers means a professional should check you first. "
            "Fill in the free follow-up at eparmedx.com (the official PAR-Q+ site) or talk to your doctor. When you have the green light, "
            "come back and tell me \"I've been cleared\" and we start.",
    "pregnancy": "Congratulations. Training during and after pregnancy is usually good for you, and your midwife or doctor should say yes first. "
                 "Once they have, tell me \"my midwife or doctor said yes\" and I'll build something that fits.",
    "diabetes": "Exercise can drop your blood sugar. Agree the plan with your doctor first, then tell me \"my doctor agreed\".",
    "symptoms": "Chest pain or fainting needs a doctor before training, every time. If it happens during a session: stop and get medical help.",
}


def run(ans):
    items = set(int(i) for i in ans.get("items", []))
    flags, stop, needs = [], [], []
    if ans.get("age_band") == "under_18":
        return {"result": "stop", "reasons": ["under_18"], "message": MESSAGES["under_18"], "flags": []}
    if items & PARQ:
        if not ans.get("cleared"):
            stop.append("parq")
        else:
            flags.append("cleared_by_professional")
        if items & HARD:
            flags.append("symptoms_reported")
    if 8 in items:
        flags.append("pregnant")
        if not ans.get("provider_ok"):
            needs.append("pregnancy")
    if 9 in items:
        flags.append("postpartum")
        if not ans.get("provider_ok"):
            needs.append("pregnancy")
    if 10 in items:
        flags.append("diabetes_hypo")
        if not ans.get("doctor_ok"):
            needs.append("diabetes")
    if 11 in items:
        flags.append("no_fat_loss_goal")
    if 12 in items:
        flags.append("low_bone_density")
    if stop:
        return {"result": "stop", "reasons": stop, "message": MESSAGES["parq"], "flags": flags}
    if needs:
        return {"result": "needs_ok", "reasons": sorted(set(needs)),
                "message": " ".join(MESSAGES[n] for n in sorted(set(needs))), "flags": flags}
    return {"result": "clear", "reasons": [], "message": "", "flags": flags}
