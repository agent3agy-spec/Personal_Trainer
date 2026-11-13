"""words.py · the words a person reads, in their language. Standard library only.

The engine thinks and writes in plain English. When the person's language is French, this pass turns every
person-facing word of a built session (and of the log, the records and the next loads) into French:

    doctrine/exercises/fr.csv   every exercise of the bank: name_fr, cue_fr, by id
    doctrine/words/fr.csv       every person-facing line of the programs and add-ons (titles, headings, efforts, reps)
    SAY and PATTERNS below      the engine's own sentences, numbers kept as they are

Numbers, loads and units never change. A line with no French is kept in English and recorded in MISSES,
so the tests can prove that a French sheet holds no English.
"""
import csv, re
import core

LANGS = ("en", "fr")
MISSES = []
_CACHE = {}


def _rows(path):
    if not path.exists():
        return []
    with open(path, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def bank_fr():
    """{id: {"name": name_fr, "cue": cue_fr}} from doctrine/exercises/fr.csv."""
    if "bank" not in _CACHE:
        _CACHE["bank"] = {r["id"]: {"name": r["name_fr"], "cue": r["cue_fr"]} for r in _rows(core.DOCTRINE / "exercises" / "fr.csv")}
    return _CACHE["bank"]


def phrases_fr():
    """{English line: French line}: the programs' and add-ons' lines, then the engine's fixed lines."""
    if "phrases" not in _CACHE:
        d = {r["en"]: r["fr"] for r in _rows(core.DOCTRINE / "words" / "fr.csv")}
        d.update(SAY)
        bank, fr = core.load_bank(), bank_fr()
        names = {}
        for i, row in bank.items():
            if i in fr:
                names[row["name"]] = fr[i]["name"]
                d.setdefault(row["cue"], fr[i]["cue"])
        _CACHE["names"] = names
        _CACHE["names_by_len"] = sorted(names, key=len, reverse=True)
        _CACHE["fr_names"] = set(names.values())
        _CACHE["phrases"] = d
    return _CACHE["phrases"]


def ex_name(ex, en_name, lang):
    if lang != "fr":
        return en_name
    return bank_fr().get(ex, {}).get("name") or tr(en_name, lang)


# · the engine's fixed lines (build.py, progress.py, logbook.py, coach.py, compose.py)

SAY = {
    "a normal day": "journée normale", "a steady day, nothing all out": "journée tranquille, rien à fond",
    "a light day: fewer sets, a little lighter": "journée légère : moins de séries, un peu plus léger", "rest day": "jour de repos",
    "travel day: nothing progresses": "jour de voyage : rien ne progresse",
    "Warm-up": "Échauffement", "Brisk walk or marching on the spot": "Marche rapide ou marche sur place",
    "Arm circles and seated punches": "Cercles de bras et coups de poing assis",
    "easy, then a little faster in the last 30 s": "facile, puis un peu plus vite sur les 30 dernières secondes",
    "5 slow reps": "5 reps lentes", "2 to 3 lighter sets": "2 à 3 séries plus légères",
    "half, then three quarters of today's weight, few reps, then start": "la moitié, puis les trois quarts de la charge du jour, peu de reps, puis c'est parti",
    "bodyweight": "poids du corps", "a band that leaves 2 to 3 reps spare": "un élastique qui laisse 2 à 3 reps en réserve",
    "your usual form": "ta technique habituelle",
    "about 3 reps spare: today you find your weight": "environ 3 reps en réserve : aujourd'hui tu trouves ta charge",
    "about 2 reps spare: find your weight on the first set, then the rest at it": "environ 2 reps en réserve : trouve ta charge sur la première série, puis le reste à cette charge",
    "2 reps spare": "2 reps en réserve", "1 to 2 reps spare": "1 à 2 reps en réserve",
    "steady, then hard in the last third": "régulier, puis dur sur le dernier tiers",
    "too hard? lighter first, then fewer reps, then an easier move, to keep the pace": "trop dur ? d'abord plus léger, puis moins de reps, puis un exercice plus simple, pour garder le rythme",
    "easy: you can talk in full sentences": "facile : tu peux parler en phrases entières",
    "Easy cardio to finish": "Cardio facile pour finir", "Optional easy movement": "Bouger en douceur, si tu veux",
    "Easy walk outside, or easy bike": "Marche facile dehors, ou vélo facile",
    "Easy bike, row or marching on the spot": "Vélo, rameur ou marche sur place, tranquille",
    "15 to 20 min": "15 à 20 min", "you can talk in full sentences the whole time": "tu peux parler en phrases entières tout du long",
    "Rest day": "Jour de repos", "Travel session": "Séance voyage", "Travel day": "Jour de voyage",
    "You said you're ill: no training today. Rest, drink, sleep. Come back when you're better.":
        "Tu as dit que tu es malade : pas d'entraînement aujourd'hui. Repose-toi, bois, dors. Reviens quand ça va mieux.",
    "Event day: no session. Warm up the way you practised, start easy, and enjoy it. Tell the trainer how it went.":
        "Jour J : pas de séance. Échauffe-toi comme à l'entraînement, pars doucement et profite. Raconte au coach comment ça s'est passé.",
    "Energy 3 or lower: today is a rest day. If you want to move, this easy session helps and counts for nothing in your plan.":
        "Énergie à 3 ou moins : aujourd'hui, c'est repos. Si tu as envie de bouger, cette séance douce aide et ne compte pas dans ton plan.",
    "Your main lifts need equipment you don't have today, so this is the travel session.":
        "Tes exercices principaux demandent du matériel que tu n'as pas aujourd'hui, alors voici la séance voyage.",
    "keep moving: this day keeps the habit, your loads wait for you": "continue de bouger : ce jour garde l'habitude, tes charges t'attendent",
    "Do the first round only.": "Fais seulement le premier tour.",
    "Done as written? If not, what changed": "Fait comme prévu ? Sinon, qu'est-ce qui a changé",
    "Anything that hurt (where, 0 to 10)": "Une douleur (où, de 0 à 10)",
    "Finish the main lifts, do one extra move, skip the last part, and log what you did.":
        "Termine les exercices principaux, fais un exercice en plus, saute la dernière partie, et note ce que tu as fait.",
    "first time on this session: today sets the numbers you will beat": "première fois sur cette séance : aujourd'hui fixe les chiffres que tu battras",
    "first time: it sets your score": "première fois : elle fixe ton score",
    "find your step: the hardest version you can do 3 sets of 5 with clean form": "trouve ton niveau : la version la plus dure que tu fais en 3 séries de 5 propres",
    "learn the move with no weight first (a shoe balanced on your fist works), then a light weight. Smooth beats heavy":
        "apprends le mouvement sans charge d'abord (une chaussure posée sur ton poing suffit), puis une charge légère. Fluide vaut mieux que lourd",
    "find your 5: empty bar first, sets of 5 climbing until one leaves about 2 reps spare. That set sets your working weight":
        "trouve tes 5 : barre à vide d'abord, des séries de 5 de plus en plus lourdes jusqu'à garder environ 2 reps en réserve. Cette série fixe ta charge de travail",
    "done as written": "fait comme prévu", "unreported": "non noté", "the timed piece": "le circuit chronométré",
    "the first session": "la première séance",
    # the notes on the sheet
    "If chest pain, dizziness or fainting happens: stop and get medical help.":
        "En cas de douleur dans la poitrine, de vertige ou de malaise : arrête et demande une aide médicale.",
    "Please see a physiotherapist or doctor before loading it again.": "Vois un kiné ou un médecin avant de le recharger.",
    "Tell the trainer what sets yours off and only those moves are swapped.": "Dis au coach ce qui la réveille et seuls ces exercices seront changés.",
    "One more easy session after your break; full sessions from the next one.": "Encore une séance facile après ta pause ; des séances complètes dès la suivante.",
    "The next step is waiting in your routine's proposals.": "L'étape suivante t'attend dans les idées pour ta routine.",
    "Make it harder with a 3 second lowering and a pause.": "Rends-le plus dur avec une descente en 3 secondes et une pause.",
    "Go by feel, and stop the set if it hurts.": "Fie-toi à tes sensations, et arrête la série si ça fait mal.",
    "The main lift can't be done with today's equipment or limits: today is the travel session.":
        "L'exercice principal n'est pas possible avec le matériel ou les limites du jour : aujourd'hui, c'est la séance voyage.",
    "The trainer can trim it if you want: see your routine's proposals.": "Le coach peut la raccourcir si tu veux : vois les idées pour ta routine.",
    "This week runs a little easier, as agreed at your check-in: one set fewer on the extra moves.":
        "Cette semaine est un peu plus facile, comme convenu au point de la semaine : une série de moins sur les exercices en plus.",
    "Very sore: the main work stays, one set fewer on the extra moves for the sore muscles, and no all-out sets.":
        "Très courbaturé : le travail principal reste, une série de moins sur les exercices en plus pour les muscles courbaturés, et aucune série à fond.",
    "Soreness is not an injury; it eases as you warm up and fades as you keep training.":
        "Une courbature n'est pas une blessure ; elle se calme à l'échauffement et disparaît quand tu continues à t'entraîner.",
    "A bit sore is normal after training: the warm-up eases it.": "Un peu de courbatures, c'est normal après l'entraînement : l'échauffement les calme.",
    "Train as written.": "Entraîne-toi comme prévu.",
    "This week: your starting numbers, a few minutes of simple tests the trainer gives you.":
        "Cette semaine : tes chiffres de départ, quelques minutes de tests simples que le coach te donne.",
    "They show how far you come.": "Ils montrent le chemin parcouru.",
    "Do not add anything: the fitness is already in the bank.": "N'ajoute rien : la forme est déjà là.",
    "Put it on the day you have the time; it is the run your event is built on.":
        "Mets-la le jour où tu as le temps ; c'est la sortie sur laquelle repose ta course.",
    "It comes back next session.": "Il revient la séance suivante.",
    "It is part of your goal, so it is the first thing back next time.": "Il fait partie de ton objectif, donc il revient en premier la prochaine fois.",
    "Welcome back. A lighter session to get going again; the plan carries on where you left it.":
        "Content de te revoir. Une séance plus légère pour repartir ; le plan reprend là où tu l'as laissé.",
    "Welcome back: after two weeks or more off, loads start about 15 percent lighter today, and the next session is easy too.":
        "Content de te revoir : après deux semaines ou plus d'arrêt, les charges repartent environ 15 % plus légères aujourd'hui, et la séance suivante est facile aussi.",
    "Welcome back.": "Content de te revoir.",
    "Loads start about 15 percent lighter, the next session is easy too, and this week we redo your starting numbers so the plan fits the you of today.":
        "Les charges repartent environ 15 % plus légères, la séance suivante est facile aussi, et cette semaine on refait tes chiffres de départ pour que le plan colle à toi aujourd'hui.",
    "Easing off before your event: less work, the same weights, so you arrive fresh.":
        "On lève le pied avant ta course : moins de travail, les mêmes charges, pour arriver frais.",
    # the coach's notes on a load
    "missed 3 times: this lift drops 10 percent and climbs back": "raté 3 fois : cet exercice baisse de 10 % et remonte",
    "missed the last set: your working weight drops 10 percent and climbs back": "dernière série ratée : ta charge de travail baisse de 10 % et remonte",
    "missed again: back to the first sets and reps, 15 percent lighter": "encore raté : retour aux premières séries et reps, 15 % plus léger",
    # this month's challenge (compose.CHALLENGES)
    "one more clean rep on your first main lift than in week 1, at the same weight":
        "une rep propre de plus qu'en semaine 1 sur ton premier exercice principal, à la même charge",
    "beat your first score on one of the timed pieces": "battre ton premier score sur un des circuits chronométrés",
    "beat your first score on the cardio burst": "battre ton premier score sur le cardio",
    "one easy run 5 minutes longer than in week 1, still able to talk": "une course facile 5 minutes plus longue qu'en semaine 1, en pouvant toujours parler",
    "beat your first time on the run straight off a station": "battre ton premier temps sur la course juste après un atelier",
    "a new best on any main lift or run": "un nouveau record sur un exercice principal ou une course",
    # the improve path's add-on proposal (improve.py)
    "HYROX stations practice": "Les ateliers HYROX", "An easy run": "Une course facile", "A cardio burst": "Du cardio",
    # what the plan says when it is chosen (plan.py choose, compose.py, eye.py)
    "Balance work is in every session.": "Il y a de l'équilibre dans chaque séance.",
    "If you have fallen or are afraid of falling, a falls programme run by a physiotherapist is the best thing you can add.":
        "Si tu es déjà tombé ou que tu as peur de tomber, un programme anti-chutes avec un kiné est le meilleur ajout.",
    "No jumping or running until you tell me it feels fine.": "Pas de sauts ni de course tant que tu ne me dis pas que ça va.",
    "Leaking, heaviness or pelvic pain: see a pelvic health physio.": "Fuites, lourdeur ou douleur pelvienne : vois un kiné spécialisé en périnée.",
    "Your classes stay yours; this plan is the closest to the rest of your week.": "Tes cours restent à toi, tels quels ; ce plan est le plus proche du reste de ta semaine.",
    "Everything stays seated.": "Tout reste assis.",
    "Some goals need standing moves; for those, an adaptive fitness professional is the right person.":
        "Certains objectifs demandent d'être debout ; pour ceux-là, un professionnel du sport adapté est la bonne personne.",
    "Its five sessions take turns: every one is a main lift plus new conditioning, so each main lift comes round every one to two weeks.":
        "Ses cinq séances tournent : chacune a un exercice principal et un nouveau circuit, donc chaque exercice principal revient toutes les une à deux semaines.",
    "Every one trains the whole body, so nothing is lost: each just comes round a little less often.":
        "Chacune fait travailler tout le corps, donc rien n'est perdu : chacune revient juste un peu moins souvent.",
    "Every one trains the whole body, so nothing is lost: each lift just comes round a little less often.":
        "Chacune fait travailler tout le corps, donc rien n'est perdu : chaque exercice revient juste un peu moins souvent.",
    "On 3 days the easy run is the session left out.": "Sur 3 jours, c'est la course facile qui saute.",
    "One easy 30 minutes on a free day is the best thing to add.": "30 minutes faciles un jour libre, c'est le meilleur ajout.",
    "One of your days is a short full body strength session: it keeps a runner's legs and trunk strong.":
        "Un de tes jours est une courte séance de renfo pour tout le corps : elle garde les jambes et le tronc d'un coureur solides.",
    "For your fitness goal, easy cardio after each run uses the rest of your minutes.":
        "Pour ton objectif de forme, du cardio facile après chaque course utilise le reste de tes minutes.",
    "a short cardio burst to finish": "un peu de cardio pour finir", "a short practice of the HYROX stations": "un court passage aux ateliers HYROX",
    "a short easy run": "une courte course facile", "a few core moves to finish": "quelques exercices de gainage pour finir",
    "No long run in the week for a running event.": "Pas de sortie longue dans la semaine pour une course.",
    "HYROX needs running and at least one station piece each week.": "L'HYROX demande de la course et au moins un passage aux ateliers chaque semaine.",
    "Mixed fitness needs at least two conditioning pieces a week.": "La forme complète demande au moins deux circuits par semaine.",
    "No conditioning reached the week: the minutes ran out before it.": "Aucun cardio dans la semaine : les minutes ont manqué avant.",
}

WORDS = {   # the small words the patterns slot in
    "region": {"knee": "genou", "hip": "hanche", "low back": "bas du dos", "shoulder": "épaule", "elbow": "coude",
               "wrist": "poignet", "ankle": "cheville", "neck": "cou", "limit": "limite"},
    "trigger": {"bending forward": "se pencher en avant", "reaching overhead": "lever les bras au-dessus de la tête",
                "jumping or running": "sauter ou courir", "kneeling or deep squats": "s'agenouiller ou descendre bas en squat",
                "gripping": "serrer fort", "twisting": "tourner le buste"},
    "muscle": {"quads": "quadriceps", "hamstrings": "ischios", "glutes": "fessiers", "calves": "mollets", "chest": "pectoraux",
               "lats": "dos", "upper back": "haut du dos", "front delts": "épaules", "side delts": "épaules",
               "rear delts": "arrière des épaules", "biceps": "biceps", "triceps": "triceps", "forearms": "avant-bras",
               "core": "gainage", "obliques": "obliques", "lower back": "bas du dos", "adductors": "adducteurs"},
    "area": {"glutes": "fessiers", "arms": "bras", "biceps": "biceps", "triceps": "triceps", "back": "dos", "chest": "pectoraux",
             "shoulders": "épaules", "legs": "jambes", "quads": "quadriceps", "hamstrings": "ischios", "core": "gainage",
             "calves": "mollets", "abs": "abdos", "pulling": "tirage"},
    "pattern": {"the press": "le développé", "the overhead press": "le développé militaire", "the row": "le rowing",
                "the pull-up or pull-down": "les tractions ou le tirage", "the squat": "le squat", "the hinge": "le soulevé",
                "the lunge": "les fentes", "curls": "les curls", "triceps work": "les triceps", "lateral raises": "les élévations latérales",
                "rear shoulder work": "l'arrière des épaules", "calf raises": "les mollets", "leg curls": "le leg curl",
                "leg extensions": "le leg extension", "glute work": "les fessiers", "core work": "le gainage", "the carry": "le portage",
                "the cardio": "le cardio", "the olympic lift": "le mouvement olympique", "balance work": "l'équilibre",
                "mobility": "la mobilité", "jumps": "les sauts", "throws": "les lancers", "crawls": "les déplacements au sol",
                "one move": "un exercice", "volume": "volume"},
    "family": {"Strength": "Force", "Strength and size": "Force et muscle", "Muscle": "Muscle", "Olympic lifting": "Haltérophilie",
               "Mixed fitness": "Forme complète", "HYROX": "HYROX", "Strength and running": "Muscu et course", "Running": "Course",
               "Full body strength": "Renfo tout le corps", "Easy cardio": "Cardio facile", "Training": "Entraînement",
               "Your plan": "Ton plan"},
}


def _w(kind, s):
    v = WORDS[kind].get(s.lower() if kind == "pattern" else s)
    if v is None:
        raise KeyError(s)
    return v


def _cap(s):
    return s[:1].upper() + s[1:]


def _list(s, kind, sep_en=" and ", sep_fr=" et "):
    parts = re.split(r", | and ", s)
    out = [_w(kind, p) for p in parts]
    return ", ".join(out[:-1]) + sep_fr + out[-1] if len(out) > 1 else out[0]


def _names(s):
    """One name, or several joined by ', ' (a name may hold a comma itself)."""
    whole = _t(s)
    if whole is not None:
        return whole
    parts = s.split(", ")
    for i in range(1, len(parts)):
        a, b = _t(", ".join(parts[:i])), None
        if a is not None:
            try:
                b = _names(", ".join(parts[i:]))
            except KeyError:
                b = None
        if a is not None and b is not None:
            return a + ", " + b
    raise KeyError(s)


def _req(s):
    v = _t(s)
    if v is None:
        raise KeyError(s)
    return v


def _num_fr(s):
    return s.replace(" percent", " %")


# (regex on one English sentence or line, without its final period; a function of the match giving the French)
PATTERNS = [
    (r"Session (\d+) of (\d+) this week", lambda m: "Séance %s sur %s cette semaine" % m.groups()),
    (r"Week (\d+) of (\d+)", lambda m: "Semaine %s sur %s" % m.groups()),
    (r"Week (\d+) of (\d+) \(an easy week: lighter on purpose, so you come back stronger\)",
     lambda m: "Semaine %s sur %s (semaine légère : plus facile exprès, pour revenir plus fort)" % m.groups()),
    (r"Today's main work: (.+)", lambda m: "Au programme principal : " + _names(m.group(1))),
    (r"Energy (\S+): (.+)", lambda m: "Énergie %s : %s" % (m.group(1), _req(m.group(2)))),
    (r"(\d+) weeks to (.+)", lambda m: "%s semaines avant %s" % (m.group(1), "ta course" if m.group(2) == "your event" else m.group(2))),
    (r"This month's challenge: (.+)", lambda m: "Le défi du mois : " + _req(m.group(1))),
    (r"Easing off: (\d+) days to (.+)", lambda m: "On lève le pied : J-%s avant %s" % m.groups()),
    (r"About (\d+) percent of your usual work, at the same weights and effort, so you arrive fresh",
     lambda m: "Environ %s %% de ton travail habituel, aux mêmes charges et au même effort, pour arriver frais" % m.group(1)),
    (r"Sharp, worsening or lasting pain \((.+)\): that area is left out",
     lambda m: "Douleur vive, qui empire ou qui dure (%s) : cette zone est mise de côté" % _list(m.group(1).replace("_", " "), "region")),
    (r"Your (.+?): the moves that (usually )?set it off \((.+)\) are swapped for ones that leave it alone; the rest is trained with care",
     lambda m: "Ton %s : les exercices qui %sla réveillent (%s) sont remplacés par d'autres qui la laissent tranquille ; le reste se travaille avec soin"
     % (_w("region", m.group(1)), "souvent " if m.group(2) else "", ", ".join(_w("trigger", x) for x in m.group(3).split(", ")))),
    (r"(.+): top of your range", lambda m: "%s : en haut de ta fourchette" % _req(m.group(1))),
    (r"(.+) moves up a step: (.+)", lambda m: "%s passe une étape : %s" % (_req(m.group(1)), _req(m.group(2)))),
    (r"(.+): top step for your kit", lambda m: "%s : dernière étape avec ton matériel" % _req(m.group(1))),
    (r"(.+) is not possible today \(your kit or what hurts today\): (.+) instead, today only",
     lambda m: "%s n'est pas possible aujourd'hui (ton matériel ou ce qui fait mal) : %s à la place, juste aujourd'hui" % (_req(m.group(1)), _req(m.group(2)))),
    (r"Your routine keeps (.+)", lambda m: "Ta routine garde %s" % _req(m.group(1))),
    (r"(.+) swapped for (.+) today", lambda m: "%s remplacé par %s aujourd'hui" % (_req(m.group(1)), _req(m.group(2)))),
    (r"Your (.+?): you kept (.+) in your routine",
     lambda m: "Ton %s : tu as gardé %s dans ta routine" % (_list(m.group(1), "region"), _req(m.group(2)))),
    (r"No move for your (.+) fits your kit or limits today",
     lambda m: "Aucun exercice pour %s ne colle à ton matériel ou à tes limites aujourd'hui" % _w("muscle", m.group(1))),
    (r"(.+) left out today \(your equipment or limits\); the rest of the main lifts stand",
     lambda m: "%s mis de côté aujourd'hui (ton matériel ou tes limites) ; le reste des exercices principaux tient" % _cap(_w("pattern", m.group(1)))),
    (r"(.+) left out today: no move for it fits your equipment and limits",
     lambda m: "%s mis de côté aujourd'hui : aucun exercice ne colle à ton matériel et à tes limites" % _cap(_w("pattern", m.group(1)))),
    (r"Shorter today because you asked for (\d+) minutes; your routine stays as it is",
     lambda m: "Plus court aujourd'hui car tu as demandé %s minutes ; ta routine reste telle quelle" % m.group(1)),
    (r"Your (.+) takes about (\d+) minutes as you wrote it, more than your usual (\d+)",
     lambda m: "Ta séance %s prend environ %s minutes telle que tu l'as écrite, plus que tes %s habituelles" % (_req(m.group(1)), m.group(2), m.group(3))),
    (r"Long run day: about (\d+) minutes in all today", lambda m: "Jour de sortie longue : environ %s minutes en tout aujourd'hui" % m.group(1)),
    (r"(.+) cut to (\d+) minutes to fit your time today", lambda m: "%s ramené à %s minutes pour tenir dans ton temps" % (_req(m.group(1)), m.group(2))),
    (r"(.+) added to use your minutes", lambda m: "Ajouté pour utiliser tes minutes : %s" % _req(m.group(1))),
    (r"(.+) left out to fit your minutes", lambda m: "Retiré pour tenir dans tes minutes : %s" % _req(m.group(1))),
    (r"(.+) left out today: the clock ran out", lambda m: "Retiré aujourd'hui, faute de temps : %s" % _req(m.group(1))),
    (r"(.+) left out today: it needs about (\d+) more minutes than you have",
     lambda m: "%s retiré aujourd'hui : il faudrait environ %s minutes de plus que ce que tu as" % (_req(m.group(1)), m.group(2))),
    (r"Its (\d+) sessions take turns over your (\d+) days", lambda m: "Ses %s séances tournent sur tes %s jours" % m.groups()),
    (r"This plan uses (\d+) of your (\d+) days: the other (?:is|are) rest or an easy walk",
     lambda m: "Ce plan utilise %s de tes %s jours : les autres, repos ou marche facile" % m.groups()),
    (r"Your (lifting sessions|sessions) end with (.+), and the clock cuts it last",
     lambda m: "Tes %s finissent par %s, et c'est ce qui saute en premier si le temps manque"
     % ("séances de muscu" if m.group(1) == "lifting sessions" else "séances", " et ".join(_req(x) for x in m.group(2).split(" and ")))),
    (r"Your long run is protected: when it needs more than your usual minutes, the sheet says so and you put it on the day you have the time",
     lambda m: "Ta sortie longue est protégée : quand elle demande plus que tes minutes habituelles, la fiche le dit et tu la places le jour où tu as le temps"),
    (r"It grows about 10 percent every (\d+) weeks, up to about (\d+) minutes",
     lambda m: "Elle grandit d'environ 10 %% toutes les %s semaines, jusqu'à environ %s minutes" % m.groups()),
    (r"The trainer added (\d+) weekly sets of (.+) to balance the week",
     lambda m: "Le coach a ajouté %s séries par semaine pour %s, pour équilibrer la semaine" % (m.group(1), _w("area", m.group(2)))),
    (r"Only (\d+) heavy session this week for a strength goal", lambda m: "Une seule séance lourde cette semaine pour un objectif de force" if m.group(1) == "1"
     else "Seulement %s séances lourdes cette semaine pour un objectif de force" % m.group(1)),
    (r"Pulling still trails pushing a little: (\d+) sets against (\d+) this week",
     lambda m: "Le tirage reste un peu derrière la poussée : %s séries contre %s cette semaine" % m.groups()),
    # block headings and lines the engine writes
    (r"Priority: (.+)", lambda m: "Priorité : " + _list(m.group(1), "area")),
    (r"More (.+)", lambda m: "En plus : " + _w("pattern", "the " + m.group(1)) if ("the " + m.group(1)).lower() in WORDS["pattern"]
     else "En plus : " + _w("pattern", m.group(1))),
    (r"Ramp: (.+)", lambda m: "Montée en charge : " + _req(m.group(1))),
    (r"(\d+:\d\d) after each round", lambda m: "%s après chaque tour" % m.group(1)),
    (r"As many rounds as you can in (\d+) min", lambda m: "Max de tours en %s min" % m.group(1)),
    (r"As fast as you can, stop at (\d+) min", lambda m: "Le plus vite possible, arrêt à %s min" % m.group(1)),
    (r"A set at the start of every minute, (\d+) min", lambda m: "Une série au début de chaque minute, %s min" % m.group(1)),
    (r"Intervals, (\d+) min", lambda m: "Fractionné, %s min" % m.group(1)),
    (r"Run, about (\d+) min", lambda m: "Course, environ %s min" % m.group(1)),
    (r"easy and crisp, (.+) reps spare", lambda m: "facile et net, %s reps en réserve" % m.group(1)),
    (r"(\d+(?: (?:or|to) \d+)?) reps? spare", lambda m: "%s reps en réserve" % m.group(1).replace(" or ", " ou ").replace(" to ", " à ")),
    (r"band: (.+)", lambda m: "élastique : " + m.group(1)),
    (r"(.+), then (.+)", lambda m: "%s, puis %s" % (_req(m.group(1)), _req(m.group(2)))),
    # first time on a move (progress.first_outing_text)
    (r"empty bar first, sets of (\d+) adding a little each set\. Stop at the first set of (\d+) that leaves about 3 reps spare\. Write that weight down",
     lambda m: "barre à vide d'abord, des séries de %s en ajoutant un peu à chaque fois. Arrête-toi à la première série de %s qui laisse environ 3 reps en réserve. Note cette charge" % m.groups()),
    (r"start with a weight you could lift 15 times\. Do (\d+)\. Go a little heavier each set until (\d+) reps leave 3 or 4 reps spare\. Write that weight down",
     lambda m: "commence avec une charge que tu pourrais soulever 15 fois. Fais-en %s. Monte un peu à chaque série jusqu'à ce que %s reps laissent 3 ou 4 reps en réserve. Note cette charge" % m.groups()),
    (r"the band that makes (\d+) reps hard but clean, 3 reps spare\. Write its colour",
     lambda m: "l'élastique qui rend %s reps dures mais propres, 3 reps en réserve. Note sa couleur" % m.group(1)),
    (r"work up in small jumps to a set of (\d+) that leaves about (\d+) reps spare\. That is your heaviest set\. Then (\d+) more sets of (\d+) at about 90 percent of it",
     lambda m: "monte par petits sauts jusqu'à une série de %s qui laisse environ %s reps en réserve. C'est ta série la plus lourde. Puis %s séries de %s à environ 90 %% de cette charge" % m.groups()),
    # the score to beat (progress.py)
    (r"all (\d+) x (\S+) at (.+)", lambda m: "toutes les %s x %s à %s" % m.groups()),
    (r"(\d+)\+ reps a set at (.+)", lambda m: "%s reps ou plus par série à %s" % m.groups()),
    (r"(\d+)\+ a set", lambda m: "%s ou plus par série" % m.group(1)),
    (r"last set: more than (\S+) at (.+)", lambda m: "dernière série : plus de %s à %s" % m.groups()),
    (r"heaviest set (\S+ (?:kg|lb)) for (\d+) with (\d+) reps spare or more",
     lambda m: "série la plus lourde à %s pour %s avec %s reps en réserve ou plus" % m.groups()),
    (r"heaviest set (\S+ (?:kg|lb)) x (\S+)", lambda m: "série la plus lourde %s x %s" % m.groups()),
    (r"3 x (\d+) on this step", lambda m: "3 x %s à ce niveau" % m.group(1)),
    (r"inside (.+) at (.+)", lambda m: "dans %s à %s" % (_req(m.group(1)) if m.group(1) != "the standard" else "le temps visé", m.group(2))),
    (r"your best on this piece: (.+)", lambda m: "ton record sur ce circuit : %s" % m.group(1)),
    (r"(\d+) min at a pace where you can talk in full sentences", lambda m: "%s min à une allure où tu peux parler en phrases entières" % m.group(1)),
    (r"week (\d+), run (\d+) of 3: finish it, walking where it says walk",
     lambda m: "semaine %s, sortie %s sur 3 : va au bout, en marchant là où c'est écrit" % m.groups()),
    # what to write down after the session (build.log_lines)
    (r"(.+): score \(rounds \+ reps, or time\)", lambda m: "%s : score (tours + reps, ou temps)" % _req(m.group(1))),
    (r"(.+): the weight you found", lambda m: "%s : la charge trouvée" % _req(m.group(1))),
    (r"(.+): minutes, and could you talk in full sentences\?", lambda m: "%s : les minutes, et pouvais-tu parler en phrases entières ?" % _req(m.group(1))),
    (r"(.+): heaviest set weight x reps, and how many reps were spare",
     lambda m: "%s : charge x reps de la série la plus lourde, et combien de reps en réserve" % _req(m.group(1))),
    (r"(.+): reps on the last set, and how many reps were spare",
     lambda m: "%s : reps de la dernière série, et combien de reps en réserve" % _req(m.group(1))),
    # after the log: next loads and records (plan.py, logbook.py)
    (r"(.+): next time (\S+ (?:kg|lb)) on the last set", lambda m: "%s : la prochaine fois %s sur la dernière série" % (_req(m.group(1)), m.group(2))),
    (r"(.+): next time (\S+ (?:kg|lb))", lambda m: "%s : la prochaine fois %s" % (_req(m.group(1)), m.group(2))),
    (r"(.+): (\S+ (?:kg|lb)) x (\d+), your best yet", lambda m: "%s : %s x %s, ton record" % (_req(m.group(1)), m.group(2), m.group(3))),
    (r"(.+): (\d+) reps(?: at (\S+ (?:kg|lb)))?, more than ever before",
     lambda m: "%s : %s reps%s, plus que jamais" % (_req(m.group(1)), m.group(2), (" à " + m.group(3)) if m.group(3) else "")),
    (r"([\d/]+) reps", lambda m: "%s reps" % m.group(1)),
    # the plan's plain name (compose.py): "Strength, 3 days" or "Strength 2 days · Running 1 day"
    (r"(.+), (\d+) days?", lambda m: "%s, %s %s" % (_w("family", m.group(1)), m.group(2), "jour" if m.group(2) == "1" else "jours")),
    (r"(.+) (\d+) days?", lambda m: "%s %s %s" % (_w("family", m.group(1)), m.group(2), "jour" if m.group(2) == "1" else "jours")),
]
PATTERNS = [(re.compile("^" + p + "$"), f) for p, f in PATTERNS]

# The reps and distances of runs and moves: a few words, every number kept.
REPS_WORDS = [(" each side", " de chaque côté"), (" each leg", " chaque jambe"), (" each arm", " chaque bras"), (" rounds", " tours"),
              (" round", " tour"), ("brisk walk before and after", "de marche rapide avant et après"), (" min run", " min de course"),
              (" run,", " de course,"), (" run)", " de course)"), (" min walk", " min de marche"), (" walk,", " de marche,"),
              (" walk)", " de marche)"), (" steps", " pas"), (" heavy", " lourd"), (" to ", " à "), (" stop with ", " arrête avec "),
              ("(stop with 1 rep spare)", "(arrête avec 1 rep en réserve)"), (" slow reps", " reps lentes"), (" then ", " puis ")]
NUMERIC = re.compile(r"^[\d\s.,:/+x×()\-%]*(?:\s*(?:min|s|m|km|cal|kg|lb|reps?)\b[\d\s.,:/+x×()\-%]*)*$")


def _t(text):
    """French for one line, or None."""
    if text is None:
        return None
    s = str(text)
    if not s.strip() or NUMERIC.match(s):
        return s
    ph = phrases_fr()
    if s in ph:
        return ph[s]
    if s in _CACHE["names"]:
        return _CACHE["names"][s]
    if s in _CACHE["fr_names"]:                         # already French (a name from a French session)
        return s
    for rx, fn in PATTERNS:
        m = rx.match(s)
        if m:
            try:
                return fn(m)
            except KeyError:
                pass
    if s.endswith(".") and s[:-1] in ph:
        return ph[s[:-1]] + "."
    if " · " in s:                                      # a title or a timed piece: every part on its own
        parts = [_t(p) or _move(p) for p in s.split(" · ")]
        if all(p is not None for p in parts):
            return " · ".join(parts)
    sents = re.split(r"(?<=[.?!])\s+(?=[A-Z])", s)
    if len(sents) > 1 or s.endswith("."):               # a note or a why line: sentence by sentence
        out = []
        for x in sents:
            body, dot = (x[:-1], ".") if x.endswith(".") else (x, "")
            y = _t(body) if body != s else None
            if y is None:
                y = (ph.get(x) or None)
                dot = "" if y else dot
            if y is None:
                return None
            out.append(y + dot)
        return " ".join(out)
    r = _move(s)
    if r is not None:
        return r
    new = s
    for a, b in REPS_WORDS:
        new = new.replace(a, b)
    if new != s and NUMERIC.match(re.sub(r"\b(de chaque côté|chaque jambe|chaque bras|tours?|de marche rapide avant et après|de course|"
                                         r"de marche|pas|lourd|à|arrête avec|rep en réserve|reps lentes|puis)\b", "", new)):
        return new
    return None


def _move(s):
    """'12 cal Row erg' or '10 Kettlebell swing': a timed piece's move, its reps and its French name."""
    phrases_fr()                                        # the tables are loaded
    for en in _CACHE.get("names_by_len", []):
        if s.endswith(" " + en):
            head = s[: -len(en) - 1]
            h = _t(head) if head else ""
            if h is not None and not h.endswith(".") and len(head) < 60:
                return (h + " " + _CACHE["names"][en]).strip()
    return None


def tr(text, lang, soft=False):
    """The line in the person's language. English stays as it is; a line with no French is recorded, unless
    soft (their own words, a day they named: those stay as they wrote them)."""
    if lang != "fr" or text in (None, ""):
        return text
    phrases_fr()
    out = _t(text)
    if out is None:
        if not soft:
            MISSES.append(str(text))
        return text
    return out


def swap_names(text, lang):
    """Every exercise name of the bank inside a free line, in French (the improve path's change lines)."""
    if lang != "fr" or not text:
        return text
    phrases_fr()
    for en in _CACHE["names_by_len"]:
        if en in text:
            text = re.sub(r"(?<![\w])%s(?![\w])" % re.escape(en), lambda m, v=_CACHE["names"][en]: v, text)
    return text


def localize_routine(reply, lang):
    """plan.py own_reply for the improve path: the exercises by id, the days, and the names inside each proposal."""
    if lang != "fr":
        return reply
    fr = bank_fr()
    for d in reply.get("routine") or []:
        d["label"] = tr(d.get("label"), lang, soft=True)
        for e in d.get("exercises") or []:
            if e.get("run") and e.get("name") == "Intervals":
                continue                                # the page names it
            if e.get("id") in fr and not e.get("own"):
                e["name"] = fr[e["id"]]["name"]
            if e.get("tracked_as"):
                e["tracked_as"] = swap_names(e["tracked_as"], lang)
    for x in (reply.get("proposals") or []) + ([reply["done"]] if reply.get("done") else []):
        for k in ("title", "why", "change"):
            if x.get(k):
                x[k] = swap_names(x[k], lang)
        args = x.get("args") or {}
        for k in ("from", "to", "name", "day"):
            if isinstance(args.get(k), str):
                args[k] = tr(args[k], lang, soft=True)
    for c in (reply.get("changes") or []) + (reply.get("declined") or []):
        c["what"] = swap_names(c.get("what"), lang)
    return reply


# · the session, the log and the records

def localize_session(s, bank=None):
    """Every person-facing word of a built session, in its language (s["language"]). Keys, ids, numbers and the
    engine's own fields (those starting with _) are never touched, so logging and progress read it as before."""
    lang = s.get("language", "en")
    if lang != "fr":
        return s
    fr = bank_fr()
    for k in ("title", "program_name", "level_text", "why", "notes", "low_energy", "score_to_beat"):
        if s.get(k):
            s[k] = tr(s[k], lang)
    s["log"] = [tr(x, lang) for x in s.get("log") or []]
    for b in s.get("blocks", []):
        b["name"] = tr(b.get("name"), lang)
        if b.get("rest_note"):
            b["rest_note"] = tr(b["rest_note"], lang)
        for it in b.get("items", []):
            row = fr.get(it.get("ex"))
            own = (it.get("_slot") or {}).get("slot", {}).get("own_name")
            keys = ["cue", "effort", "reps", "load", "first_outing"]
            if row and not (own and it.get("name") == own):
                it["name"] = row["name"]
                if it.get("cue") == (bank or core.load_bank()).get(it["ex"], {}).get("cue"):
                    it["cue"] = row["cue"]
                    keys.remove("cue")
            else:
                it["name"] = tr(it.get("name"), lang) if not own else it.get("name")
            for k in keys:
                if it.get(k) not in (None, "") and isinstance(it[k], str):
                    it[k] = tr(it[k], lang)
    return s


def localize_lines(lines, lang):
    return [tr(x, lang) for x in lines or []]


def localize_records(recs, lang):
    """logbook.records and new_records: the name by id, the text line by pattern."""
    if lang != "fr":
        return recs
    fr = bank_fr()
    for r in recs or []:
        if r.get("ex") in fr:
            en = r.get("name")
            r["name"] = fr[r["ex"]]["name"]
            if r.get("text") and en:
                r["text"] = tr(r["text"], lang)
    return recs


def person_lines(obj):
    """The person-facing lines of a program or add-on json (titles, block headings, efforts, reps with words, cues)."""
    out = []

    def walk(o):
        if isinstance(o, dict):
            for k, v in o.items():
                if isinstance(v, str) and (k in ("title", "effort", "cue", "standard") or (k == "name" and "kind" in o)
                                           or (k == "reps" and not NUMERIC.match(v))):
                    out.append(v)
                elif not isinstance(v, str):
                    walk(v)
        elif isinstance(o, list):
            for x in o:
                walk(x)
    walk(obj)
    return out


def coverage():
    """What the French tables miss: bank ids without a row (or with an empty one), and program or add-on lines
    without a French line. Both lists empty means a French sheet can be written for every program."""
    fr, bank = bank_fr(), core.load_bank()
    ids = [i for i in bank if not (fr.get(i) or {}).get("name") or not (fr.get(i) or {}).get("cue")]
    extra = [i for i in fr if i not in bank]
    ph = {r["en"] for r in _rows(core.DOCTRINE / "words" / "fr.csv") if r.get("fr")}
    objs = [(p["id"], p) for p in core.all_programs()]
    for f in sorted(core.MODULES.glob("*.md")):
        m = core.read_json_block(f)
        if m:
            objs.append(("module " + m["id"], m))
    lines = []
    for owner, o in objs:
        own = person_lines(o) + ([o["name"]] if owner.startswith("module ") else [])
        lines += ["%s: %s" % (owner, x) for x in own if x not in ph]
    return {"bank_missing": ids, "bank_unknown": extra, "lines_missing": lines}


def clear():
    """Forget the tables and the misses (tests)."""
    _CACHE.clear()
    del MISSES[:]
