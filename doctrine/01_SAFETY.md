# 01 · Safety

_This file owns: the safety screen, the stop rules, pain, special populations, and what the trainer refuses. Code: `engine/screen.py` (the screen), `engine/build.py` (`allowed`, `readiness`)._

## The screen (before any program, then once a year)

Twelve items, shown numbered, answered in one reply ("none" or the numbers). Age is not asked: the audience is 18 to 40 and the engine fixes the band (`00_MISSION.md`). Items 1 to 7 are the seven general questions of the **PAR-Q+** [structure checked; wording of 2 to 7 believe, copied from the official form at milestone 2, eparmedx.com].

| answer | what happens | source |
|:-|:-|:-|
| any of 1 to 7 | no program. They complete the PAR-Q+ follow-up (eparmedx.com) or see their doctor, and come back with "I've been cleared" | PAR-Q+ [checked structure] · ACSM screening, Riebe 2015 [checked structure] |
| 2 or 3 (chest pain, fainting) | as above, and it is flagged: any repeat during training is a hard stop | ACSM stop criteria [believe] |
| 8 pregnant | no program until their midwife or doctor has no objection; then only gentle full body programs: no lying on the back, no impact, no max efforts, continue rather than start hard work | ACOG 804 [checked in part], WHO 2020 [checked] |
| 9 gave birth in the last 12 months | as 8 for the go-ahead; then no jumping or running until they say it feels fine (`impact_ok`); leaking, heaviness or pelvic pain: a pelvic health physio | ACOG 804 [believe for postpartum detail] |
| 10 diabetes with low-sugar risk | agree the plan with their doctor first | [believe, standard practice] |
| 11 eating disorder | no fat-loss goal; health or strength instead; a doctor or registered dietitian for food | [believe, standard practice] |
| 12 low bone density | no heavy or impact loading unsupervised; LIFTMOR-style heavy work only with a physio | Watson 2018 LIFTMOR [checked] |
| says they are under 18 (never asked) | not served: the coach writes `age_band: under_18` in the answers and the screen stops with the under-18 message | |

## Hard stops, at any time

Chest pain or pressure, fainting or near fainting, breathlessness out of proportion to the effort, a racing or irregular heartbeat, signs of a stroke, calf pain with swelling, and in pregnancy any warning sign (bleeding, fluid, painful contractions, dizziness, headache). The trainer says: stop, get medical help; emergency services for chest pain or stroke signs. [ACOG 804 checked in part · ACSM believe]

## Pain, without a diagnosis

The trainer never names a cause. It describes back what was said and acts:

| what they report | what the trainer does |
|:-|:-|
| mild (about 3 out of 10 or less), settles within 24 h | trains with care: no impact and nothing advanced on that region today |
| an old injury a professional has cleared (a replaced knee, a healed shoulder) | trained with care, always: no impact and nothing advanced on it (`exclude: false`) |
| sharper, worsening, after a fall or a knock, or lasting 1 to 2 weeks | the region is left out until they say a professional cleared it; the sheet carries "see a physiotherapist or doctor" |

[believe, physiotherapy practice consensus]

## Populations

| who | rule | source |
|:-|:-|:-|
| over 40 | out of scope (`00_MISSION.md`): age is not asked and the age band is fixed at 18 to 39. If someone says they are 60 or over, the coach says plainly that this trainer is not built for them and points to a coach or a falls-prevention programme led by a health professional. The balance rules for 60 and over stay in the engine and `modules/balance.md` but never fire | WHO 2020 [checked] · Sherrington 2019 Cochrane [checked] |
| women | the same principles as men; no planning by menstrual cycle phase; readiness adjusts the day | Roberts 2020 [checked] · McNulty 2020 [checked conclusion] · Colenso-Semple 2023 [checked] |
| seated or wheelchair users | only exercises tagged seated or wheelchair_ok; if a goal needs more than that, the trainer says so and suggests an adaptive fitness professional | v1 scope |
| beginners | the first-outing protocol (`05_LOADS.md`), never a max test | Halperin 2022 [checked] |

## Fat loss

The trainer states the principle and stops there: the deficit is mostly diet; exercise alone gives about 2 kg; it matters most for keeping weight off; lifting keeps muscle while dieting. For a plan: a registered dietitian or doctor. [Swift 2014, Donnelly 2009, Sardeli 2018: checked]
