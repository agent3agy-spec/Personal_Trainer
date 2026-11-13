# DESIGN · the trainer's identity on the web page

The owner's picks of 13 November 2026, and where each one lives in `site/`. Every value below is a token or a
string in one place; change it there and nowhere else.

## The picks

| pick | what was chosen | where it lives |
|---|---|---|
| Form | an object mascot, a gym object with a face, glossy ceramic finish. Final shape not decided (blob and animal options still to come); 3D render later with Higgsfield | `mark.svg`, drawn through `#agent-mark` in `index.html` |
| Placeholder | a small glossy burgundy ceramic kettlebell with two eyes and a small smile | `mark.svg` |
| Icons | Tabler outline 3.19.0 (MIT), inlined as `<symbol>`s, stroke `currentColor`, stroke width 1.75 everywhere | `build_icons.py` writes the sprite in `index.html` |
| Type | Syne for titles, buttons, labels and body; Space Mono for numbers, data lines and kickers | `--font-title`, `--font-ui`, `--font-data` in `app.css` |
| Voice | a mate who coaches: short, second person, warm, every coach line ends on the next step; no em dash, no double dash | `STR` in `app.js`, EN and FR |
| Paint | the MATIÈR house paint, unchanged: paper, ink, burgundy, ochre once a screen, light and dark | `:root` in `app.css` |

## Tokens

Light (`:root`) · dark (`prefers-color-scheme: dark`, or `data-theme="dark"` from Settings).

| token | light | dark | use |
|---|---|---|---|
| `--bg` | `#F7F4F3` | `#1D0A0C` | the ground |
| `--surface` | `#FFFFFF` | `#2A1215` | cards |
| `--surface2` | `#F1ECEB` | `#341A1D` | quiet tiles, empty calendar days |
| `--fg` | `#2B1A1C` | `#F2E7E6` | ink |
| `--muted` | `#7B6669` | `#B9A3A5` | secondary text |
| `--faint` | `#A2908F` | `#7B6669` | day initials, done dots |
| `--accent` | `#8E2440` | `#A8344F` | the one action, selected state, trained days |
| `--accent-ink` | `#8E2440` | `#E08AA0` | accent as text or line |
| `--accent-fg` | `#F2E7E6` | `#F2E7E6` | the only ink on burgundy |
| `--ochre` | `#A9714A` | `#D19A72` | one hot spot a screen ("To beat today") |
| `--line` / `--line2` | ink at 10% / 6% | paper at 12% / 7% | borders, rules |
| `--font-title` | `'Syne'` 700, tracking -0.025em | | screen titles |
| `--font-ui` | `'Syne'` 400 to 700 | | body, buttons, tiles |
| `--font-data` | `'Space Mono'` 400 / 700 | | numbers, steppers, records, next loads, kickers |
| `--r` / `--rs` / `--pill` | 18px / 12px / 100px | | radii |
| `--ease` | `cubic-bezier(.22,1,.36,1)` | | the house ease: the press |
| `--spring` | `cubic-bezier(.34,1.56,.64,1)` | | the release: small overshoot, then settle |

Fonts load from Google Fonts only: `Syne:wght@400..800` and `Space Mono:wght@400;700`.

## Where Syne fought readability, and the fix

- **Two-column tiles.** Syne is a wide face; at 16px half-width tiles on a 375px phone wrapped labels to
  three lines ("Learn the / Olympic / lifts"). In the two-column grid only, the label drops to 15px with
  -0.02em tracking and the icon to 24px. Labels now wrap once at most. Single-column tiles keep 16px.
- **Body text stays Syne 16px.** Checked at phone width: coach lines and the safety cards read fine at
  regular weight, so body was not moved to Space Mono (a monospace body reads worse, not better).
- **Space Mono is reserved for data.** As words it runs wide: the program "fact" chips (3 days a week,
  Good evidence) wrapped one per line in Space Mono, so they stay in Syne. Numbers next to words sit one
  step smaller (13.5px) so a mono line does not shout over the Syne around it.
- **Syne has no italic.** The accent word in the welcome title is coloured, not slanted.

## The details built

1. **Spring buttons.** Every `.btn`, `.tile`, `.chip`, `.iconbtn`, program card, segment and stepper button
   presses to 0.955 (tiles and cards 0.975) in 90ms on `--ease`, and springs back over 550ms on `--spring`.
   `prefers-reduced-motion: reduce` switches both off.
2. **Streak calendar** (week screen). The last 6 weeks, Monday first, as a 7 x 6 grid of days. A trained day
   is filled burgundy; more than one session that day shows `×2`; today is ringed; future days are outlined.
   Above it: weeks in a row with at least one session (the current week does not break the streak before
   it ends) and sessions in 6 weeks. Read from `me/log.jsonl` in the page's Python filesystem; nothing new
   is stored.
3. **Personal records.** Best weight x reps per main lift (the main and second-lift blocks of each logged
   session), ranked by estimated max (Epley). Shown as a card on the week screen, and on the Logged screen
   as "New record" when a lift beats its own best. A lift's first outing is its baseline, never a record.

## Swapping in the 3D mark

The mark is one file drawn from one place. To use the Higgsfield render:

1. Export it square, transparent background, at least 256 x 256 (512 for a sharp hero), as `site/mark.webp`
   (or `.png`). Keep the object centred with a little air; the welcome screen shows it at 132px, the header
   at 36px, beside coach lines at 36px.
2. In `index.html`, change the one `href` inside `<symbol id="agent-mark">` from `mark.svg` to `mark.webp`.
3. Run `python3 site/build_bundle.py` only if you also changed the engine; the mark is not in the bundle.

Every `mark()` call in `app.js` and the header `<use href="#agent-mark">` follow automatically.

## Changing an icon

Edit the Tabler name in `MAP` in `build_icons.py`, then `python3 site/build_icons.py`. It fetches the SVG with
curl from `cdn.jsdelivr.net/npm/@tabler/icons@3.19.0/icons/outline/<name>.svg` and rewrites the sprite between
the `icons:start` and `icons:end` markers. Tabler 3.19.0 has no kettlebell; `weight` (its kettlebell-shaped
weight) stands in for kettlebell and dumbbell.

## The first-time bar · 13 November 2026

The owner's bar: someone who has never used a fitness app could follow it. The page rules that hold it:

- **Every screen names its step.** Under the dots: `Step 2 of 5 · You` (`T.stepOf`, `T.phases`).
- **Every screen has a way back.** Safety goes back to the welcome, the first goal back to safety, the
  program list says "Change my answers", every readiness question and the weight screen have Back.
- **One main action, pinned on long screens.** The sticky `.actions` bar. On the sheet it holds Save
  first; once saved, "I trained: log it" becomes the main action and Save drops to a quiet button.
- **A disabled button always says why** (`.hint` under it): the safety check and the first-weights screen.
- **No dead ends.** "Not yet" on a safety pause lands on a screen with Back and the follow-up link; "nothing
  fits" offers "Change my answers"; the loader shows Reload after 20 s.
- **After the PDF is saved, the page says where it went** (Downloads, Files on iPhone, Files or Downloads on
  Android), the file name, and the next step: print it, or open it on the phone while training.
- **On a safety stop the safe path is the main button** ("OK, I'll get checked first"); "I have been
  cleared" stays one tap away and still asks to confirm.
- Numbers run in order (days 2 to 6, minutes 20 to 90, energy high to low). Specialist goals carry a plain
  sub line (HYROX, powerlifting, Olympic lifts).
- Taps from Start to the first sheet: 18, measured by `window.__firstSheetTaps`. Keep it at 18 or under.
- Taps from Start to "Your plan" (13 nov interview): 14 on the new path for a beginner, 17 on the improve path,
  measured by `window.__planTaps`. The plan is one, decided by the trainer; "Not for me" takes a reason and re-runs the match.

## Not covered here

The session sheet inside the page (and its PDF) is drawn by the engine, not by `site/`, so it keeps the
engine's own type. Moving the sheet to Space Mono is an engine change.
