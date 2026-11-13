/* Personal trainer · the one-link web page.
 *
 * The engine (engine/plan.py and the doctrine) runs unchanged inside Pyodide. This file is only
 * the talking: one job per screen, taps instead of words, and the bridge that hands the engine its
 * answer files and keeps me/ and sessions/ on this device (IndexedDB).
 *
 * Swap points, each in ONE place:
 *   strings and tone   STR below (en, fr)
 *   icons              the sprite in index.html (#i-*, #t-*), written by site/build_icons.py
 *   the agent's mark   site/mark.svg, drawn by #agent-mark in the sprite, used through mark()
 *   faces and paint    :root tokens in app.css
 */
'use strict';

// ─────────────────────────────────────────────────────────────── strings
const STR = {
  en: {
    brand: 'Personal trainer', settings: 'Settings',
    boot: ['Starting', 'Waking up your trainer', 'Reading the rules', 'Finding your notes', 'Ready'],
    bootTitle: 'Getting your trainer ready',
    bootFail: 'I couldn’t start on this device. Reload the page and we’ll try again.',
    reload: 'Reload',
    bootLead: 'The first time takes a few seconds while I set up on this device. After that it opens fast.',
    bootSlow: 'Still working. A slow connection can take up to a minute. If nothing moves, reload the page.',
    stepOf: (i, n, name) => 'Step ' + i + ' of ' + n + ' · ' + name,
    phases: ['Safety', 'You', 'Program', 'Today', 'Sheet'],
    welcomeTitle: 'Your <em>Personal</em> trainer',
    welcomeLead: 'A few taps and I build you a proven program, then a one-page sheet for every session, each built on how the last one went. Tap Start and we go.',
    welcomeNote: 'Everything stays on this device.',
    start: 'Start',
    safetyTitle: 'A quick safety check',
    safetyLead: 'Quick one before we start. Tap any that apply to you. None? Tap “None of these” at the bottom.',
    safetyHint: 'Tap “None of these” or the ones that apply.',
    safety: [
      'A doctor said you have a heart condition or high blood pressure',
      'Chest pain at rest, in daily life, or when you are active',
      'Lost balance from dizziness, or fainted, in the last 12 months',
      'Another long-term medical condition',
      'You take medication for a long-term condition',
      'A bone, joint or muscle problem that being more active could make worse',
      'A doctor said you should only exercise with medical supervision',
      'You are pregnant',
      'You gave birth in the last 12 months',
      'Diabetes treated with insulin or tablets that can cause low blood sugar',
      'An eating disorder, now or in the past',
      'A doctor said you have low bone density',
    ],
    noneOfThese: 'None of these', noneSub: 'I am good to go',
    next: 'Next', cont: 'Continue', back: 'Back', skip: 'Skip',
    tapOne: 'Tap one.',
    screenMsg: {
      under_18: 'I’m built for adults for now. Your best move: ask a coach at your school or club to set up your training.',
      parq: 'Thanks for being straight with me. Before I build anything, a professional should check you. Do the free follow-up at eparmedx.com or see your doctor. Got the green light? Come back and tap "I have been cleared".',
      pregnancy: 'Congratulations. Training through and after pregnancy is usually good for you, and your midwife or doctor says yes first. Once they have, tap the button below.',
      diabetes: 'Exercise can drop your blood sugar, so agree the plan with your doctor first. Then tap the button below.',
      symptoms: 'Chest pain or fainting means a doctor before training, every time. If it hits during a session, stop and get medical help.',
    },
    pauseTitle: 'Let’s pause here',
    holdTitle: 'One go-ahead first',
    cleared: 'I have been cleared', clearedSub: 'A doctor or professional said yes',
    mistake: 'I ticked one by mistake',
    clearedConfirm: 'Just checking: a doctor or a qualified pro has seen you and said you can train? If so, tap yes.',
    yesCleared: 'Yes, they said I can',
    mistakeTitle: 'Which one does not apply?',
    mistakeLead: 'Untick it, then confirm.',
    confirm: 'Confirm',
    providerOk: 'My midwife or doctor said yes',
    doctorOk: 'My doctor agreed',
    notYet: 'Not yet',
    waitLine: 'No rush, I’ll be right here. Come back when you’ve got the go-ahead.',
    checkFirst: 'OK, I’ll get checked first',
    eparLink: 'Open the free follow-up (eparmedx.com)',
    returnTitle: 'Welcome back',
    returnLead: 'Good to see you. Last time we paused for a check. Got the go-ahead?',
    clearLine: 'All good. Now tell me what you want.',
    edLine: 'We’ll keep the focus on getting strong and feeling good.',
    goalTitle: 'What do you want most?',
    goal2Title: 'A second goal?',
    goal2Lead: 'Optional. It adds a little extra to your week. Pick one, or tap no.',
    noSecond: 'No, just the one',
    goals: {
      muscle: 'Build muscle', strength: 'Get stronger', powerlifting: 'Compete in powerlifting',
      weightlifting: 'Learn the Olympic lifts', functional: 'All-round fitness', hyrox: 'A HYROX race',
      run: 'Running', fat_loss: 'Lose fat', health: 'Feel healthier',
    },
    goalSub: {
      functional: 'CrossFit style, in a gym', run: '5 km up to a half marathon', powerlifting: 'Squat, bench press and deadlift', weightlifting: 'Snatch, clean and jerk',
      hyrox: 'A race of running and gym stations', muscle: 'Bigger, firmer muscles', strength: 'Lift heavier things',
    },
    youDecide: 'You decide', youDecideSub: 'I’ll pick the safe choice',
    expTitle: 'How long have you been training?',
    exp: {
      none: ['Never', 'Or not for 2 years or more'],
      novice: ['Under 6 months', 'Still adding weight most sessions'],
      intermediate: ['6 months to 2 years', 'Progress comes week to week'],
      advanced: ['2 years or more', 'Progress comes month to month, or I compete'],
    },
    daysTitle: 'How many days a week can you train?',
    daysUnit: (n) => n === 1 ? 'day' : 'days',
    minutesTitle: 'How long per session?',
    min: 'min',
    whereTitle: 'Where do you train?',
    where: { gym: 'A gym', home_gym: 'A home gym', outdoors: 'Outdoors' },
    whereSub: { home_gym: 'Your own kit: a barbell, dumbbells or a cardio machine', outdoors: 'For running only' },
    kitTitle: 'What’s there?',
    kit: { full_gym: 'Full gym', basic_gym: 'Basic gym', crossfit_box: 'CrossFit box', home_dumbbells: 'Dumbbells or bands', outdoors: 'Outdoors, for a run' },
    kitSub: { basic_gym: 'Racks, dumbbells, a few machines', crossfit_box: 'Barbells, rowers, bikes, a rig' },
    homeKitTitle: 'What’s in your home gym?',
    homeKitLead: 'Tick everything you have.',
    homeKitHint: 'Tick a rack and barbell, dumbbells or a cardio machine. Kettlebells or bands alone aren’t enough for this trainer.',
    homeKit: { rack: 'Rack, barbell and plates', bench: 'Bench', dumbbell: 'Dumbbells', kettlebell: 'Kettlebells', pullup_bar: 'Pull-up bar', band: 'Bands', rower: 'Rower', bike: 'Bike', skierg: 'Ski erg', treadmill: 'Treadmill' },
    dbTitle: 'Which dumbbells do you have?',
    db: { light: 'A light pair or two', mid: 'Up to 12 kg', heavy: 'Up to 20 kg', adj: 'Adjustable, up to 24 kg' },
    dbSub: { light: '4 and 8 kg', mid: '4, 8 and 12 kg', heavy: '4 to 20 kg', adj: 'In 2 kg steps' },
    youTitle: 'A few extras, all optional',
    youLead: 'Tap what fits, or just tap Continue.',
    hurtQ: 'Anything hurting, or an injury to work around?',
    hurtNow: 'Hurts now', hurtOld: 'Old, cleared',
    regions: { knee: 'Knee', hip: 'Hip', low_back: 'Lower back', shoulder: 'Shoulder', elbow: 'Elbow', wrist: 'Wrist', ankle: 'Ankle', neck: 'Neck' },
    seated: 'I train seated',
    likeQ: 'Styles you love',
    hateQ: 'Styles you’d rather skip',
    styles: { barbell: 'Barbell', machines: 'Machines', dumbbells: 'Dumbbells', kettlebells: 'Kettlebells', bodyweight: 'Bodyweight', circuits: 'Circuits', running: 'Running', classes: 'Classes' },
    areaQ: 'An area to bring up?',
    areas: { glutes: 'Glutes', arms: 'Arms', back: 'Back', chest: 'Chest', legs: 'Legs', shoulders: 'Shoulders', core: 'Core' },
    unitsNote: (u) => u === 'lb' ? 'I’ll use pounds.' : 'I’ll use kilos.',
    skillQ: { run_30min: 'Can you run 30 minutes without stopping?', olympic_coached: 'Has a coach taught you the snatch and the clean?', pullup: 'Can you do one strict pull-up?' },
    yes: 'Yes', no: 'No', notSure: 'Not sure',
    saving: 'One moment',
    errorsTitle: 'Something needs a change',
    progTitle: 'Your best fits',
    progLead: 'I picked these by rule from your answers. Tap the one you want. Not sure? Take the first one.',
    chooseThis: 'Choose this',
    changeAnswers: 'Change my answers',
    recommended: 'Recommended',
    perWeek: (n) => n + ' days a week',
    fit: { 3: 'Built for your goal', 2: 'Good for your goal', 1: 'Helps your goal', 0: 'A safe start' },
    evidence: { A: 'Strong evidence', B: 'Good evidence', C: 'Proven by coaches', G: 'Official guidelines' },
    from: 'Based on',
    oneChange: (name, why) => 'One change would open ' + name + ': ' + why + '.',
    nothingFits: 'Nothing I have fits you safely yet. Your best next step is a qualified coach, or for seated training an adaptive fitness pro.',
    notServed: 'I don’t cover that goal yet, so here are the nearest.',
    weekTitle: 'Your week',
    weekLine: (days, prog) => days + ' sessions a week of ' + prog + ', in order, on whatever days suit you. Ready for the first one?',
    addons: 'Add-ons',
    firstNow: 'Make my first session', later: 'Later',
    energyTitle: 'How’s your energy?',
    energy: { 7: ['Normal', '6 to 7 out of 10'], 9: ['Great', '8 to 10'], 5: ['Low', '4 to 5'], 3: ['Wrecked', '1 to 3'] },
    painTitle: 'Anything hurting?',
    pain: { none: 'Nothing', little: 'A little', sharp: 'Yes, sharp or getting worse' },
    painSub: { little: 'I can train around it' },
    whereHurt: 'Where?',
    timeTitle: 'How long have you got today?',
    usual: 'My usual',
    unusualTitle: 'Anything unusual today?',
    unusual: { no: 'No', slept: 'Slept badly', cardio: 'Hard cardio or a run in the last 24 hours', ill: 'Ill or feverish', kit: 'Different place or kit today' },
    kitToday: 'What’s there today?',
    building: 'Building your session',
    rendering: 'Drawing your sheet',
    restTitle: 'A rest day',
    restIll: 'You’re ill, so no training today. Rest, drink, sleep. Come back when you feel better and we pick it up.',
    restLow: 'Energy at 3 or lower means a rest day. Want to move anyway? This easy session helps and doesn’t touch your plan.',
    easySheet: 'Show the easy session', done: 'Done',
    sheetTitle: 'Your session is ready',
    toBeat: 'To beat today: ',
    firstTime: 'First time on these lifts: the sheet shows how to find your weight. Start light, then log what you found.',
    savePdf: 'Save my sheet (PDF)',
    pdfSaved: 'Saved.', pdfDeclined: 'Not saved.', pdfFail: 'Could not save here. Try again.',
    sheetLead: 'Step 1: save your sheet. Step 2: train with it. Step 3: come back and tap “I trained”.',
    pdfWhere: (name) => 'Saved as ' + name,
    pdfWhereLine: 'Look in your Downloads folder. On an iPhone: the Files app, then Downloads. On Android: the Files or Downloads app.',
    pdfNext: ['Print it and take it with you.', 'Or open it on your phone while you train and tick the boxes as you go.', 'Done? Come back here and tap “I trained”.'],
    pdfNoFile: 'Nothing saved? Tap Save again. If your browser asks, choose Download or Save.',
    zoomIn: 'See the sheet bigger', zoomOut: 'Fit the sheet to the screen',
    trained: 'I trained: log it',
    myWeek: 'My week',
    tooLong: 'That one ran past your time. Tap Try again and I’ll rebuild it.',
    tryAgain: 'Try again',
    howTitle: (t) => 'How did it go?',
    howLead: (t) => t,
    howAll: 'All done as written', howSome: 'Mostly, a few changes', howNot: 'I didn’t do it',
    seeSheet: 'Not yet, show my sheet',
    needsTitle: 'What weight did you end on?',
    needsLead: 'First time on these, so tell me the weight you landed on.',
    optionalLine: 'And if you remember, roughly what you used here too.',
    changesTitle: 'What changed?',
    changesLead: 'Change only what was different. Anything you leave counts as done as written.',
    didIt: 'Done', skipped: 'Skipped',
    weight: 'Weight', repsEach: 'Reps each set', minutes: 'Minutes',
    tapToSet: 'Tap + to set it', less: 'Less', more: 'More',
    needsHint: 'Set each weight with + or −, then save.',
    feltQ: 'How did it feel?',
    felt: { great: 'Great', good: 'Good', hard: 'Hard', flat: 'Flat' },
    hurtQ2: 'Anything hurt?',
    hurtNo: 'Nothing hurt',
    mild: 'Mild', sharpW: 'Sharp',
    wordsQ: 'Or tell it in your own words',
    wordsPh: 'squats felt heavy, last set only 3, skipped the curls',
    readWords: 'Fill this in from my words',
    reading: 'Reading your words',
    readDone: 'Filled in from your words. Check it, then save.',
    readFail: 'I couldn’t read that. Use the taps above instead.',
    readNo: 'Claude isn’t available here. Use the taps above.',
    saveLog: 'Save how it went',
    loggedTitle: 'Logged',
    home: 'Done',
    nextTime: 'Next time',
    weekClosed: 'That closes your week. Nice work.',
    blockClosed: 'That closes a block. The next one starts from your new numbers.',
    deload: 'Your body is asking for an easier week, so the next sessions run lighter. Keep showing up.',
    noProblem: 'No problem, it happens. The next one is ready when you are.',
    notInSession: 'Noted in your log. It doesn’t change the plan.',
    todaySession: 'Today’s session',
    readyTitle: 'Ready when you are',
    readyLead: (n) => 'Next up: ' + n + '. Tap below when you’re ready.',
    weekSoFar: (d, p) => d + ' of ' + p + ' sessions done this week',
    weekViewTitle: 'This week',
    doneOf: (d, p) => d + ' of ' + p + ' sessions done',
    last7: 'The last 7 days',
    nothingYet: 'Nothing logged yet this week. Your next session fills it.',
    loggedNext: 'Rest up. Your next session is ready when you are.',
    streakTitle: 'Your streak',
    streakWeeks: (n) => n === 1 ? '1 week in a row' : n + ' weeks in a row',
    streakCount: (n, w) => n + (n === 1 ? ' session' : ' sessions') + ' in ' + w + ' weeks',
    streakNone: 'No sessions yet. Your first one fills the first square.',
    dow: ['M', 'T', 'W', 'T', 'F', 'S', 'S'],
    prTitle: 'Your records',
    prNone: 'Your best lifts land here after your first logged session.',
    prNew: 'New',
    recordTitle: (n) => n === 1 ? 'New record' : n + ' new records',
    recordLine: 'You beat your best. Keep the form clean and go again next time.',
    hardSets: 'Work per muscle this week',
    usualBand: 'Each bar counts the hard sets for that muscle. The shaded band is the usual range.',
    muscles: { chest: 'Chest', back: 'Back', shoulders: 'Shoulders', quads: 'Quads', glutes: 'Glutes', hamstrings: 'Hamstrings', biceps: 'Biceps', triceps: 'Triceps', calves: 'Calves', core: 'Core' },
    setTitle: 'Settings',
    backup: 'Save my trainer', backupSub: 'A file with everything, to keep or move to another device',
    restore: 'Load my trainer', restoreSub: 'From a file you saved before',
    restored: 'Your trainer is back.', restoreBad: 'That file is not a saved trainer.',
    startOver: 'Start over', startOverSub: 'Erase everything on this device',
    startOverQ: 'Erase everything?',
    startOverLead: 'Your answers, your plan, your log and your sheets on this device are erased. This cannot be undone. Save your trainer first if you might want it back.',
    erase: 'Yes, erase everything', keep: 'Keep everything',
    theme: 'Look', themes: { auto: 'Auto', light: 'Light', dark: 'Dark' },
    noStorage: 'This device is not keeping notes for this page, so your trainer lasts until you close it. Save your trainer to keep it.',
    close: 'Close',
    sayAlso: {},
    iv: {
      forkTitle: 'Do you already train?',
      forkLead: 'All good on the safety side. Now, where do you start? Tap one.',
      fork: { new: ['Build me a new plan', 'I’m starting, or I want something fresh'], improve: ['Improve what I already do', 'I have a routine and want more from it'] },
      outcomeTitle: 'What do you want training to do for you?',
      outcomeLead: 'Pick up to three. The first one you tap leads.',
      outcomeHint: 'Tap at least one.',
      main: 'Main', also: 'Also',
      outcome: { look: ['Look better', 'More muscle, or leaner and defined'], strong: ['Get strong', 'Stronger at everything, or a lift to compete in'],
        athletic: ['Be athletic', 'Fit for anything, or strong and able to run far'], event: ['Get ready for an event', 'A 5K to a marathon, HYROX, a lifting meet'],
        keep_going: ['Keep it going', 'Steady training with numbers to beat'] },
      follow: {
        look: { q: 'What change do you want most?', opts: { size: ['More muscle, more size', 'Bigger and fuller'], lean: ['Leaner and defined', 'Lose fat, keep the muscle'] } },
        strong: { q: 'Strong for what?', opts: { general: ['Stronger at everything', 'Lift heavier, feel solid'], powerlifting: ['Squat, bench and deadlift', 'A lift to compete in'], olympic: ['The Olympic lifts', 'Snatch, clean and jerk'] } },
        athletic: { q: 'What kind of athletic?', opts: { crossfit: ['Fit for anything', 'Lifts, gymnastics and hard conditioning'], hybrid: ['Strong and able to run far', 'Lifting and running in one week'] } },
        event: { q: 'Which event?', opts: { run_5k_10k: ['A 5K or 10K', 'A road race'], run_half: ['A half marathon', '21 km'], run_marathon: ['A marathon', '42 km'], hyrox: ['HYROX', 'Running plus gym stations'], meet: ['A lifting meet', 'Squat, bench and deadlift on the day'] } },
        keep_going: { q: 'What do you want to keep doing?', opts: { lifting: ['Lifting', 'Getting a bit stronger every month'], fitness: ['Fitness and cardio', 'Fitter every month'], mix: ['A bit of everything', 'Strength and easy cardio'] } },
      },
      dateQ: 'When is it?', dateLead: 'The date lets me build toward it. No date yet is fine.', noDate: 'No date yet',
      balanceTitle: 'How much of your week for each?',
      balanceLead: 'A rough split is enough. Not sure? Tap You decide: the main one gets most.',
      weight: { little: 'A little', some: 'Some', lots: 'Most' },
      historyTitle: 'What have you done regularly?',
      historyLead: 'At any point, not just now. Tick all that fit.',
      act: { lifting: 'I lift weights', running: 'I run', cardio: 'I cycle, row or swim', classes: 'I do classes or circuits', crossfit: 'I do CrossFit or HYROX' },
      nothingYet: 'Nothing yet', nothingYetSub: 'I’m new to this, and that’s fine',
      expTitle: 'How long have you done it?',
      expLead: 'One tap each. Roughly is fine: your first sessions fine-tune it.',
      howLong: { novice: 'Under 6 months', intermediate: 'Up to 2 years', advanced: '2 years +' },
      returning: 'I’m coming back after a break',
      styleTitle: 'Do you have a training style you prefer?',
      styleLead: 'Optional. You know your way around, so you can say. Or leave it to me.',
      style: { trainer: 'Let the trainer decide', strength: 'Strength', bodybuilding: 'Bodybuilding', powerbuilding: 'Power-building', crossfit: 'CrossFit-style', hyrox: 'HYROX-style', running: 'Running', hybrid: 'Hybrid' },
      enjoyTitle: 'What do you enjoy?',
      enjoyLead: 'This helps me pick a plan you’ll stick with. Skip anything.',
      enjoyQ: 'I enjoy', avoidQ: 'I can’t stand',
      enjoy: { heavy: 'Heavy lifting', pump: 'Muscle work and the pump', circuits: 'Fast circuits', long_cardio: 'Long cardio', running: 'Running' },
      kitQ: 'Free weights or machines?', kitPref: { free_weights: 'Free weights', machines: 'Machines', either: 'Either' },
      splitTitle: 'What does your week look like?', splitLead: 'Pick the closest.',
      split: { ppl: ['Push, pull, legs', 'Chest and arms, back, legs'], upper_lower: ['Upper and lower', 'Upper body days, lower body days'],
        full_body: ['Full body', 'Everything each session'], body_part: ['One body part a day', 'Chest day, back day, leg day'],
        strength_cardio: ['Strength days plus cardio days', 'Lifting and running or rowing'], run_plan: ['A running plan', 'Easy runs, intervals, a long run'],
        classes: ['Classes', 'CrossFit, HYROX or HIIT classes'], custom: ['A mix I made up', 'My own thing'] },
      rdaysTitle: 'How many days a week do you train?',
      exTitle: 'Your main exercises',
      exLead: 'I ticked the usual ones. Untick, tick or type your own.',
      typeEx: 'Type an exercise', add: 'Add',
      dayName: { push: 'Push', pull: 'Pull', legs: 'Legs', upper: 'Upper', lower: 'Lower', fa: 'Full body A', fb: 'Full body B', fc: 'Full body C',
        chest: 'Chest', back: 'Back', shoulders: 'Shoulders', arms: 'Arms', strength: 'Strength', cardio: 'Cardio', easy: 'Easy run',
        intervals: 'Intervals', long: 'Long run', class: 'Class', d1: 'Day 1', d2: 'Day 2', d3: 'Day 3', d4: 'Day 4', d5: 'Day 5', d6: 'Day 6' },
      ageTitle: 'How long have you run this routine?',
      age: { under_1m: 'Under a month', '1_3m': '1 to 3 months', '3_12m': '3 to 12 months', over_1y: 'Over a year' },
      goingTitle: 'How is it going?', goingLead: 'Tap what fits. Both are optional.',
      stallQ: 'What’s stuck?', stall: { lift_stuck: 'A lift won’t go up', not_growing: 'Not growing', tired: 'Always tired or sore', bored: 'Bored', skipping: 'I skip sessions', pain: 'Something hurts', fine: 'It’s fine' },
      keepQ: 'What must stay?', keep: { split: 'The split', exercises: 'The exercises', days: 'The days', pump: 'The pump', short: 'Short sessions', everything: 'Everything' },
      minLead: 'Type it, or use + and −. Anything from 15 to 120.',
      minHint: 'Pick a number from 15 to 120.',
      unitsQ: 'Kilos or pounds?',
      dbLb: { light: ['A light pair or two', '10 and 15 lb'], mid: ['Up to 25 lb', '10 to 25 lb'], heavy: ['Up to 45 lb', '10 to 45 lb'], adj: ['Adjustable, up to 50 lb', 'In 5 lb steps'] },
      youTitle: 'About you',
      youLead: 'All optional, but it makes the plan yours. Tap what fits, then Continue.',
      goodQ: 'What you’re good at', good: { strong: 'Strong for my size', engine: 'Good engine', flexible: 'Flexible', technique: 'Good technique', consistent: 'I show up' },
      holdQ: 'What holds you back', hold: { time: 'Time', motivation: 'Motivation', energy: 'Energy or sleep', stress: 'Stress', pain: 'Pain or stiffness', know_how: 'Not knowing what to do', bored: 'Getting bored' },
      painQ: 'Anything that hurts, or hurt before?',
      status: { now: 'Hurts now', mild: 'Only on some moves', cleared: 'Old, cleared', unchecked: 'Old, never checked' },
      triggerQ: 'What sets it off?',
      trigger: { bending: 'Bending forward', overhead: 'Reaching overhead', impact: 'Jumping or running', kneeling: 'Kneeling or deep squats', gripping: 'Gripping', twisting: 'Twisting' },
      sleepQ: 'Sleep most nights', sleep: { under_6: 'Under 6 h', '6_7': '6 to 7 h', '7_plus': '7 h +' },
      stressQ: 'Stress lately', stress: { low: 'Low', medium: 'Medium', high: 'High' },
      numbersQ: 'Numbers you know', numbersLead: 'A recent weight and reps. Skip if you don’t know.', reps: 'Reps',
      planTitle: 'Your plan',
      planLead: 'From your answers, this is what I’d have you do.',
      planBadge: 'Picked for you',
      rethought: 'Got it. Here’s what I’d have you do instead.',
      family: { strength: 'Strength first', powerbuild: 'Strength and size', muscle: 'Muscle building', weightlifting: 'Olympic lifting',
        functional: 'Mixed fitness', hyrox: 'HYROX race training', hybrid: 'Strength and running', run: 'Running', health: 'Full body health' },
      familyLine: { strength: 'Heavy main lifts first, then muscle work.', powerbuild: 'Heavy days and muscle days in the same week.',
        muscle: 'Plenty of sets close to failure, every muscle twice a week.', weightlifting: 'Technique first, then strength for the lifts.',
        functional: 'A strength part, then fast conditioning.', hyrox: 'Running plus the race stations, built toward the day.',
        hybrid: 'Lifting and running in one week, spaced so both improve.', run: 'Mostly easy running, building up week by week.',
        health: 'Full body strength with easy cardio.' },
      shape: { ppl: 'Push, pull, legs', upper_lower: 'Upper and lower days', full_body: 'Full body', body_part: 'Body part days',
        strength_cardio: 'Strength and run days', run_plan: 'Different runs', classes: 'A new mix each time' },
      about: (m) => 'About ' + m + ' min',
      whyFits: 'Why it fits you',
      howItWorks: 'How it works',
      howLine: (name, from) => 'Built on ' + name + (from ? ', from ' + from : '') + '. The trainer runs it for you: loads, progress and easier weeks.',
      startPlan: 'Start this plan', notForMe: 'Not for me',
      whyNotTitle: 'What’s wrong with it?', whyNotLead: 'Tell me, and I’ll rethink it.',
      whyNot: { too_long: 'Sessions are too long', too_much_running: 'Too much running', not_enjoy: 'I wouldn’t enjoy it', days: 'I can’t do these days' },
      oneChange: (why) => 'One change would open a better fit: ' + why + '.',
      expect: 'What to expect: the first 2 to 4 weeks are for learning the moves and finding your weights. Strength shows up before the mirror does. A missed week is normal: you just pick up the next session.',
      notes: {},
    },
    engineFail: 'Something went wrong on my side. Tap Try again.',
  },
  fr: {
    brand: 'Coach perso', settings: 'Réglages',
    boot: ['Démarrage', 'Ton coach se réveille', 'Lecture des règles', 'Tes notes', 'Prêt'],
    bootTitle: 'Ton coach se prépare',
    bootFail: 'Je n’ai pas pu démarrer sur cet appareil. Recharge la page et on réessaie.',
    reload: 'Recharger',
    bootLead: 'La première fois prend quelques secondes, le temps de m’installer sur cet appareil. Ensuite, ça s’ouvre vite.',
    bootSlow: 'Je travaille encore. Une connexion lente peut prendre une minute. Si rien ne bouge, recharge la page.',
    stepOf: (i, n, name) => 'Étape ' + i + ' sur ' + n + ' · ' + name,
    phases: ['Sécurité', 'Toi', 'Programme', 'Aujourd’hui', 'Fiche'],
    welcomeTitle: 'Ton <em>coach</em> perso',
    welcomeLead: 'Quelques touches et je te construis un programme éprouvé, puis une fiche d’une page pour chaque séance, construite sur la précédente. Touche Commencer et on y va.',
    welcomeNote: 'Tout reste sur cet appareil.',
    start: 'Commencer',
    safetyTitle: 'Un petit point sécurité',
    safetyLead: 'Un point rapide avant de commencer. Touche ce qui te concerne. Rien ? Touche « Rien de tout ça » en bas.',
    safetyHint: 'Touche « Rien de tout ça » ou ce qui te concerne.',
    safety: [
      'Un médecin t’a dit que tu as un problème cardiaque ou de la tension',
      'Une douleur à la poitrine au repos, au quotidien ou à l’effort',
      'Une perte d’équilibre par vertige, ou un malaise, ces 12 derniers mois',
      'Une autre maladie de longue durée',
      'Un traitement pour une maladie de longue durée',
      'Un problème d’os, d’articulation ou de muscle que l’activité pourrait aggraver',
      'Un médecin t’a dit de ne faire du sport que sous surveillance médicale',
      'Tu es enceinte',
      'Tu as accouché ces 12 derniers mois',
      'Un diabète traité par insuline ou par des comprimés qui peuvent faire baisser le sucre',
      'Un trouble alimentaire, aujourd’hui ou par le passé',
      'Un médecin t’a dit que ta densité osseuse est basse',
    ],
    noneOfThese: 'Rien de tout ça', noneSub: 'Je suis prêt',
    next: 'Suivant', cont: 'Continuer', back: 'Retour', skip: 'Passer',
    tapOne: 'Touche une réponse.',
    screenMsg: {
      under_18: 'Je suis fait pour les adultes pour l’instant. Le bon réflexe : demande à un coach de ton école ou de ton club de construire ton entraînement.',
      parq: 'Merci d’être franc. Avant de construire quoi que ce soit, un professionnel doit te voir. Fais le suivi gratuit sur eparmedx.com ou vois ton médecin. Tu as le feu vert ? Reviens et touche « J’ai le feu vert ».',
      pregnancy: 'Félicitations. Bouger pendant et après la grossesse fait en général du bien, et ta sage-femme ou ton médecin dit oui d’abord. Quand c’est fait, touche le bouton ci-dessous.',
      diabetes: 'Le sport peut faire baisser ton sucre, alors valide le plan avec ton médecin d’abord. Ensuite, touche le bouton ci-dessous.',
      symptoms: 'Une douleur à la poitrine ou un malaise demande un médecin avant de s’entraîner, à chaque fois. Si ça arrive pendant une séance : arrête et appelle les secours.',
    },
    pauseTitle: 'On fait une pause',
    holdTitle: 'Un feu vert d’abord',
    cleared: 'J’ai le feu vert', clearedSub: 'Un médecin ou un pro a dit oui',
    mistake: 'J’ai coché par erreur',
    clearedConfirm: 'Juste pour être sûr : un médecin ou un pro qualifié t’a vu et t’a dit que tu peux t’entraîner ? Si oui, touche oui.',
    yesCleared: 'Oui, on m’a dit oui',
    mistakeTitle: 'Laquelle ne te concerne pas ?',
    mistakeLead: 'Décoche-la, puis confirme.',
    confirm: 'Confirmer',
    providerOk: 'Ma sage-femme ou mon médecin a dit oui',
    doctorOk: 'Mon médecin est d’accord',
    notYet: 'Pas encore',
    waitLine: 'Pas de souci, je reste là. Reviens quand tu as le feu vert.',
    checkFirst: 'D’accord, je me fais vérifier d’abord',
    eparLink: 'Ouvrir le suivi gratuit (eparmedx.com)',
    returnTitle: 'Te revoilà',
    returnLead: 'Content de te revoir. La dernière fois, on a fait une pause pour un avis médical. Tu as eu le feu vert ?',
    clearLine: 'Tout est bon. Maintenant, dis-moi ce que tu veux.',
    edLine: 'On garde le cap sur la force et le bien-être.',
    goalTitle: 'Ce que tu veux le plus ?',
    goal2Title: 'Un deuxième objectif ?',
    goal2Lead: 'Facultatif. Ça ajoute un petit plus à ta semaine. Choisis-en un, ou touche non.',
    noSecond: 'Non, un seul',
    goals: {
      muscle: 'Prendre du muscle', strength: 'Devenir plus fort', powerlifting: 'Faire de la compétition de force',
      weightlifting: 'Apprendre l’haltérophilie', functional: 'Une forme complète', hyrox: 'Une course HYROX',
      run: 'La course à pied', fat_loss: 'Perdre du gras', health: 'Être en meilleure santé',
    },
    goalSub: {
      functional: 'Style CrossFit, en salle', run: 'Du 5 km au semi',
      powerlifting: 'Squat, développé couché, soulevé de terre', weightlifting: 'Arraché, épaulé-jeté',
      hyrox: 'Une course avec des ateliers de salle', muscle: 'Des muscles plus fermes et plus gros', strength: 'Soulever plus lourd',
    },
    youDecide: 'Choisis pour moi', youDecideSub: 'Je prends le choix prudent',
    expTitle: 'Depuis quand tu t’entraînes ?',
    exp: {
      none: ['Jamais', 'Ou pas depuis 2 ans ou plus'],
      novice: ['Moins de 6 mois', 'J’ajoute encore du poids presque à chaque séance'],
      intermediate: ['6 mois à 2 ans', 'Je progresse de semaine en semaine'],
      advanced: ['2 ans ou plus', 'Je progresse de mois en mois, ou je fais de la compétition'],
    },
    daysTitle: 'Combien de jours par semaine ?',
    daysUnit: (n) => n === 1 ? 'jour' : 'jours',
    minutesTitle: 'Combien de temps par séance ?',
    min: 'min',
    whereTitle: 'Où t’entraînes-tu ?',
    where: { gym: 'En salle', home_gym: 'Ma salle à la maison', outdoors: 'Dehors' },
    whereSub: { home_gym: 'Ton matériel : une barre, des haltères ou une machine cardio', outdoors: 'Pour courir seulement' },
    kitTitle: 'Qu’est-ce qu’il y a ?',
    kit: { full_gym: 'Une salle complète', basic_gym: 'Une salle simple', crossfit_box: 'Une box de CrossFit', home_dumbbells: 'Haltères ou élastiques', outdoors: 'Dehors, pour courir' },
    kitSub: { basic_gym: 'Racks, haltères, quelques machines', crossfit_box: 'Barres, rameurs, vélos, une cage' },
    homeKitTitle: 'Qu’y a-t-il dans ta salle à la maison ?',
    homeKitLead: 'Coche tout ce que tu as.',
    homeKitHint: 'Coche une cage et une barre, des haltères ou une machine cardio. Des kettlebells ou des élastiques seuls ne suffisent pas pour ce coach.',
    homeKit: { rack: 'Cage, barre et disques', bench: 'Banc', dumbbell: 'Haltères', kettlebell: 'Kettlebells', pullup_bar: 'Barre de traction', band: 'Élastiques', rower: 'Rameur', bike: 'Vélo', skierg: 'SkiErg', treadmill: 'Tapis de course' },
    dbTitle: 'Quels haltères as-tu ?',
    db: { light: 'Une ou deux paires légères', mid: 'Jusqu’à 12 kg', heavy: 'Jusqu’à 20 kg', adj: 'Réglables, jusqu’à 24 kg' },
    dbSub: { light: '4 et 8 kg', mid: '4, 8 et 12 kg', heavy: 'De 4 à 20 kg', adj: 'Par pas de 2 kg' },
    youTitle: 'Quelques extras, facultatifs',
    youLead: 'Touche ce qui te va, ou touche Continuer.',
    hurtQ: 'Une douleur ou une blessure à ménager ?',
    hurtNow: 'Ça fait mal', hurtOld: 'Ancienne, guérie',
    regions: { knee: 'Genou', hip: 'Hanche', low_back: 'Bas du dos', shoulder: 'Épaule', elbow: 'Coude', wrist: 'Poignet', ankle: 'Cheville', neck: 'Cou' },
    seated: 'Je m’entraîne assis',
    likeQ: 'Ce que tu aimes',
    hateQ: 'Ce que tu préfères éviter',
    styles: { barbell: 'Barre', machines: 'Machines', dumbbells: 'Haltères', kettlebells: 'Kettlebells', bodyweight: 'Poids du corps', circuits: 'Circuits', running: 'Course', classes: 'Cours' },
    areaQ: 'Une zone à travailler en plus ?',
    areas: { glutes: 'Fessiers', arms: 'Bras', back: 'Dos', chest: 'Pectoraux', legs: 'Jambes', shoulders: 'Épaules', core: 'Gainage' },
    unitsNote: (u) => u === 'lb' ? 'J’utilise les livres.' : 'J’utilise les kilos.',
    skillQ: { run_30min: 'Tu peux courir 30 minutes sans t’arrêter ?', olympic_coached: 'Un coach t’a appris l’arraché et l’épaulé ?', pullup: 'Tu peux faire une traction stricte ?' },
    yes: 'Oui', no: 'Non', notSure: 'Pas sûr',
    saving: 'Un instant',
    errorsTitle: 'Une réponse à revoir',
    progTitle: 'Ce qui te va le mieux',
    progLead: 'Je les ai choisis par des règles, à partir de tes réponses. Touche celui que tu veux. Pas sûr ? Prends le premier.',
    chooseThis: 'Choisir celui-ci',
    changeAnswers: 'Changer mes réponses',
    recommended: 'Recommandé',
    perWeek: (n) => n + ' jours par semaine',
    fit: { 3: 'Fait pour ton objectif', 2: 'Bon pour ton objectif', 1: 'Aide ton objectif', 0: 'Un départ sûr' },
    evidence: { A: 'Preuves solides', B: 'Bonnes preuves', C: 'Éprouvé par les coachs', G: 'Recommandations officielles' },
    from: 'Inspiré de',
    oneChange: (name, why) => 'Un seul changement ouvrirait ' + name + ' : ' + why + '.',
    nothingFits: 'Rien de ce que j’ai ne te convient sans risque pour l’instant. La bonne étape : un coach diplômé, ou pour l’entraînement assis un pro du sport adapté.',
    notServed: 'Je ne couvre pas encore cet objectif, voici les plus proches.',
    weekTitle: 'Ta semaine',
    weekLine: (days, prog) => days + ' séances par semaine de ' + prog + ', dans l’ordre, les jours qui t’arrangent. Prêt pour la première ?',
    addons: 'En plus',
    firstNow: 'Ma première séance', later: 'Plus tard',
    energyTitle: 'Ton énergie ?',
    energy: { 7: ['Normale', '6 à 7 sur 10'], 9: ['Super', '8 à 10'], 5: ['Basse', '4 à 5'], 3: ['À plat', '1 à 3'] },
    painTitle: 'Quelque chose fait mal ?',
    pain: { none: 'Rien', little: 'Un peu', sharp: 'Oui, vif ou ça empire' },
    painSub: { little: 'Je peux faire avec' },
    whereHurt: 'Où ?',
    timeTitle: 'Combien de temps aujourd’hui ?',
    usual: 'Comme d’habitude',
    unusualTitle: 'Quelque chose d’inhabituel ?',
    unusual: { no: 'Non', slept: 'Mal dormi', cardio: 'Gros cardio ou course ces dernières 24 h', ill: 'Malade ou fiévreux', kit: 'Autre lieu ou autre matériel' },
    kitToday: 'Qu’est-ce qu’il y a aujourd’hui ?',
    building: 'Je construis ta séance',
    rendering: 'Je dessine ta fiche',
    restTitle: 'Jour de repos',
    restIll: 'Tu es malade, donc pas d’entraînement aujourd’hui. Repos, eau, sommeil. Reviens quand ça va mieux et on reprend.',
    restLow: 'Énergie à 3 ou moins, c’est repos. Envie de bouger quand même ? Cette séance douce aide et ne touche pas ton plan.',
    easySheet: 'Voir la séance douce', done: 'Terminé',
    sheetTitle: 'Ta séance est prête',
    toBeat: 'À battre aujourd’hui : ',
    firstTime: 'Première fois sur ces exercices : la fiche montre comment trouver ta charge. Commence léger, puis note ce que tu as trouvé.',
    savePdf: 'Enregistrer ma fiche (PDF)',
    pdfSaved: 'Enregistrée.', pdfDeclined: 'Pas enregistrée.', pdfFail: 'Impossible ici. Réessaie.',
    sheetLead: 'Étape 1 : enregistre ta fiche. Étape 2 : entraîne-toi avec. Étape 3 : reviens et touche « Je me suis entraîné ».',
    pdfWhere: (name) => 'Enregistrée sous ' + name,
    pdfWhereLine: 'Regarde dans ton dossier Téléchargements. Sur iPhone : l’app Fichiers, puis Téléchargements. Sur Android : l’app Fichiers ou Téléchargements.',
    pdfNext: ['Imprime-la et emporte-la.', 'Ou ouvre-la sur ton téléphone pendant la séance et coche les cases au fur et à mesure.', 'Fini ? Reviens ici et touche « Je me suis entraîné ».'],
    pdfNoFile: 'Rien d’enregistré ? Touche Enregistrer à nouveau. Si ton navigateur demande, choisis Télécharger ou Enregistrer.',
    zoomIn: 'Voir la fiche en grand', zoomOut: 'Ajuster la fiche à l’écran',
    trained: 'Je me suis entraîné : on note',
    myWeek: 'Ma semaine',
    tooLong: 'Celle-ci dépassait ton temps. Touche Réessayer et je la refais.',
    tryAgain: 'Réessayer',
    howTitle: (t) => 'Comment ça s’est passé ?',
    howLead: (t) => t,
    howAll: 'Tout fait comme prévu', howSome: 'En gros, avec des changements', howNot: 'Je ne l’ai pas faite',
    seeSheet: 'Pas encore, montre ma fiche',
    needsTitle: 'Avec quelle charge as-tu fini ?',
    needsLead: 'Première fois sur ceux-là, dis-moi la charge où tu es arrivé.',
    optionalLine: 'Et si tu t’en souviens, à peu près ce que tu as pris ici aussi.',
    changesTitle: 'Qu’est-ce qui a changé ?',
    changesLead: 'Change seulement ce qui était différent. Le reste compte comme fait comme prévu.',
    didIt: 'Fait', skipped: 'Sauté',
    weight: 'Charge', repsEach: 'Reps par série', minutes: 'Minutes',
    tapToSet: 'Touche + pour la régler', less: 'Moins', more: 'Plus',
    needsHint: 'Règle chaque charge avec + ou −, puis enregistre.',
    feltQ: 'Comment tu l’as sentie ?',
    felt: { great: 'Super', good: 'Bien', hard: 'Dure', flat: 'Sans jus' },
    hurtQ2: 'Quelque chose a fait mal ?',
    hurtNo: 'Rien',
    mild: 'Léger', sharpW: 'Vif',
    wordsQ: 'Ou raconte avec tes mots',
    wordsPh: 'squats lourds, dernière série à 3, j’ai sauté les curls',
    readWords: 'Remplir à partir de mes mots',
    reading: 'Je lis tes mots',
    readDone: 'Rempli à partir de tes mots. Vérifie, puis enregistre.',
    readFail: 'Je n’ai pas pu lire ça. Utilise les touches au-dessus.',
    readNo: 'Claude n’est pas disponible ici. Utilise les touches au-dessus.',
    saveLog: 'Enregistrer ma séance',
    loggedTitle: 'C’est noté',
    home: 'Terminé',
    nextTime: 'La prochaine fois',
    weekClosed: 'Ta semaine est bouclée. Beau travail.',
    blockClosed: 'Un bloc se termine. Le suivant part de tes nouveaux chiffres.',
    deload: 'Ton corps demande une semaine plus facile, donc les prochaines séances seront plus légères. Continue de venir.',
    noProblem: 'Pas de souci, ça arrive. La prochaine est prête quand tu veux.',
    notInSession: 'Noté dans ton carnet. Ça ne change pas le plan.',
    todaySession: 'La séance du jour',
    readyTitle: 'Prêt quand tu l’es',
    readyLead: (n) => 'Prochaine séance : ' + n + '. Touche en bas quand tu es prêt.',
    weekSoFar: (d, p) => d + ' séance' + (d > 1 ? 's' : '') + ' sur ' + p + ' cette semaine',
    weekViewTitle: 'Cette semaine',
    doneOf: (d, p) => d + ' séance' + (d > 1 ? 's' : '') + ' sur ' + p,
    last7: 'Les 7 derniers jours',
    nothingYet: 'Rien de noté cette semaine. Ta prochaine séance le remplit.',
    loggedNext: 'Récupère bien. Ta prochaine séance est prête quand tu veux.',
    streakTitle: 'Ta série',
    streakWeeks: (n) => n === 1 ? '1 semaine d’affilée' : n + ' semaines d’affilée',
    streakCount: (n, w) => n + (n === 1 ? ' séance' : ' séances') + ' en ' + w + ' semaines',
    streakNone: 'Pas encore de séance. La première remplit la première case.',
    dow: ['L', 'M', 'M', 'J', 'V', 'S', 'D'],
    prTitle: 'Tes records',
    prNone: 'Tes meilleures charges arrivent ici après ta première séance notée.',
    prNew: 'Nouveau',
    recordTitle: (n) => n === 1 ? 'Nouveau record' : n + ' nouveaux records',
    recordLine: 'Tu as battu ton record. Garde une technique propre et on remet ça la prochaine fois.',
    hardSets: 'Travail par muscle cette semaine',
    usualBand: 'Chaque barre compte les séries dures pour ce muscle. La bande grisée est la fourchette habituelle.',
    muscles: { chest: 'Pectoraux', back: 'Dos', shoulders: 'Épaules', quads: 'Quadriceps', glutes: 'Fessiers', hamstrings: 'Ischios', biceps: 'Biceps', triceps: 'Triceps', calves: 'Mollets', core: 'Gainage' },
    setTitle: 'Réglages',
    backup: 'Sauvegarder mon coach', backupSub: 'Un fichier avec tout, à garder ou à passer sur un autre appareil',
    restore: 'Charger mon coach', restoreSub: 'Depuis un fichier sauvegardé',
    restored: 'Ton coach est de retour.', restoreBad: 'Ce fichier n’est pas une sauvegarde du coach.',
    startOver: 'Tout recommencer', startOverSub: 'Effacer tout sur cet appareil',
    startOverQ: 'Tout effacer ?',
    startOverLead: 'Tes réponses, ton plan, ton carnet et tes fiches sur cet appareil seront effacés. Impossible de revenir en arrière. Sauvegarde ton coach avant si tu veux pouvoir le récupérer.',
    erase: 'Oui, tout effacer', keep: 'Tout garder',
    theme: 'Apparence', themes: { auto: 'Auto', light: 'Clair', dark: 'Sombre' },
    noStorage: 'Cet appareil ne garde pas de notes pour cette page : ton coach dure jusqu’à la fermeture. Sauvegarde ton coach pour le garder.',
    close: 'Fermer',
    sayAlso: {
      'Balance work is in every session.': 'Il y a de l’équilibre dans chaque séance. Si tu es déjà tombé ou que tu as peur de tomber, un programme anti-chutes avec un kiné est le meilleur ajout.',
      'No jumping or running until you tell me it feels fine.': 'Pas de sauts ni de course tant que tu ne me dis pas que ça va. Fuites, lourdeur ou douleur pelvienne : vois un kiné spécialisé en périnée.',
      'Everything stays seated.': 'Tout reste assis. Certains objectifs demandent d’être debout ; pour ceux-là, un professionnel du sport adapté est la bonne personne.',
    },
    iv: {
      forkTitle: 'Tu t’entraînes déjà ?',
      forkLead: 'Côté sécurité, tout est bon. Maintenant, d’où pars-tu ? Touche une réponse.',
      fork: { new: ['Construis-moi un nouveau plan', 'Je commence, ou je veux du neuf'], improve: ['Améliore ce que je fais déjà', 'J’ai une routine et j’en veux plus'] },
      outcomeTitle: 'Qu’est-ce que l’entraînement doit t’apporter ?',
      outcomeLead: 'Jusqu’à trois. Le premier touché passe en tête.',
      outcomeHint: 'Touche au moins une réponse.',
      main: 'En tête', also: 'Aussi',
      outcome: { look: ['Être mieux dans mon corps', 'Plus de muscle, ou plus sec et dessiné'], strong: ['Devenir fort', 'Plus fort partout, ou un mouvement en compétition'],
        athletic: ['Être athlétique', 'Prêt à tout, ou fort et endurant'], event: ['Préparer un événement', 'Du 5 km au marathon, HYROX, une compétition de force'],
        keep_going: ['Garder le rythme', 'Un entraînement régulier avec des chiffres à battre'] },
      follow: {
        look: { q: 'Quel changement veux-tu le plus ?', opts: { size: ['Plus de muscle, plus de volume', 'Plus gros, plus plein'], lean: ['Plus sec et dessiné', 'Perdre du gras, garder le muscle'] } },
        strong: { q: 'Fort pour quoi ?', opts: { general: ['Plus fort partout', 'Soulever plus lourd, se sentir solide'], powerlifting: ['Squat, développé couché, soulevé de terre', 'Un mouvement en compétition'], olympic: ['L’haltérophilie', 'Arraché, épaulé-jeté'] } },
        athletic: { q: 'Quel genre d’athlète ?', opts: { crossfit: ['Prêt à tout', 'Charges, gymnastique et cardio intense'], hybrid: ['Fort et endurant', 'Musculation et course dans la même semaine'] } },
        event: { q: 'Quel événement ?', opts: { run_5k_10k: ['Un 5 ou 10 km', 'Une course sur route'], run_half: ['Un semi-marathon', '21 km'], run_marathon: ['Un marathon', '42 km'], hyrox: ['HYROX', 'Course et ateliers de salle'], meet: ['Une compétition de force', 'Squat, développé couché, soulevé de terre'] } },
        keep_going: { q: 'Qu’est-ce que tu veux garder ?', opts: { lifting: ['La musculation', 'Un peu plus fort chaque mois'], fitness: ['Le cardio et la forme', 'Plus en forme chaque mois'], mix: ['Un peu de tout', 'Force et cardio doux'] } },
      },
      dateQ: 'C’est quand ?', dateLead: 'La date me permet de construire vers le jour J. Pas encore de date, ça va aussi.', noDate: 'Pas encore de date',
      balanceTitle: 'Quelle part de ta semaine pour chacun ?',
      balanceLead: 'Une idée suffit. Pas sûr ? Touche Choisis pour moi : le premier prend le plus.',
      weight: { little: 'Un peu', some: 'Une part', lots: 'Le plus' },
      historyTitle: 'Qu’as-tu fait régulièrement ?',
      historyLead: 'À un moment ou un autre, pas seulement maintenant. Coche tout ce qui va.',
      act: { lifting: 'De la musculation', running: 'De la course', cardio: 'Du vélo, de l’aviron ou de la natation', classes: 'Des cours ou des circuits', crossfit: 'Du CrossFit ou de l’HYROX' },
      nothingYet: 'Rien encore', nothingYetSub: 'Je débute, et c’est très bien',
      expTitle: 'Depuis combien de temps ?',
      expLead: 'Une touche chacun. À peu près suffit : tes premières séances affinent.',
      howLong: { novice: 'Moins de 6 mois', intermediate: 'Jusqu’à 2 ans', advanced: '2 ans +' },
      returning: 'Je reprends après une pause',
      styleTitle: 'Tu as un style d’entraînement préféré ?',
      styleLead: 'Facultatif. Tu connais le terrain, alors tu peux le dire. Ou laisse-moi choisir.',
      style: { trainer: 'Laisse le coach choisir', strength: 'Force', bodybuilding: 'Bodybuilding', powerbuilding: 'Power-building', crossfit: 'Style CrossFit', hyrox: 'Style HYROX', running: 'Course', hybrid: 'Hybride' },
      enjoyTitle: 'Qu’est-ce que tu aimes ?',
      enjoyLead: 'Ça m’aide à choisir un plan que tu tiendras. Passe ce que tu veux.',
      enjoyQ: 'J’aime', avoidQ: 'Je ne supporte pas',
      enjoy: { heavy: 'Soulever lourd', pump: 'Le travail musculaire, la congestion', circuits: 'Les circuits rapides', long_cardio: 'Le cardio long', running: 'La course' },
      kitQ: 'Poids libres ou machines ?', kitPref: { free_weights: 'Poids libres', machines: 'Machines', either: 'Peu importe' },
      splitTitle: 'À quoi ressemble ta semaine ?', splitLead: 'Choisis le plus proche.',
      split: { ppl: ['Push, pull, legs', 'Pecs et bras, dos, jambes'], upper_lower: ['Haut et bas du corps', 'Des jours haut, des jours bas'],
        full_body: ['Full body', 'Tout le corps à chaque séance'], body_part: ['Un muscle par jour', 'Jour pecs, jour dos, jour jambes'],
        strength_cardio: ['Force et cardio', 'Musculation et course ou rameur'], run_plan: ['Un plan de course', 'Footings, fractionné, sortie longue'],
        classes: ['Des cours', 'CrossFit, HYROX ou HIIT'], custom: ['Mon propre mélange', 'Mon truc à moi'] },
      rdaysTitle: 'Combien de jours par semaine ?',
      exTitle: 'Tes exercices principaux',
      exLead: 'J’ai coché les classiques. Décoche, coche ou écris les tiens.',
      typeEx: 'Écris un exercice', add: 'Ajouter',
      dayName: { push: 'Push', pull: 'Pull', legs: 'Jambes', upper: 'Haut', lower: 'Bas', fa: 'Full body A', fb: 'Full body B', fc: 'Full body C',
        chest: 'Pecs', back: 'Dos', shoulders: 'Épaules', arms: 'Bras', strength: 'Force', cardio: 'Cardio', easy: 'Footing',
        intervals: 'Fractionné', long: 'Sortie longue', class: 'Cours', d1: 'Jour 1', d2: 'Jour 2', d3: 'Jour 3', d4: 'Jour 4', d5: 'Jour 5', d6: 'Jour 6' },
      ageTitle: 'Depuis quand tu suis cette routine ?',
      age: { under_1m: 'Moins d’un mois', '1_3m': '1 à 3 mois', '3_12m': '3 à 12 mois', over_1y: 'Plus d’un an' },
      goingTitle: 'Comment ça se passe ?', goingLead: 'Touche ce qui va. Les deux sont facultatifs.',
      stallQ: 'Qu’est-ce qui bloque ?', stall: { lift_stuck: 'Une charge ne monte plus', not_growing: 'Je ne grossis plus', tired: 'Toujours fatigué ou courbaturé', bored: 'Je m’ennuie', skipping: 'Je saute des séances', pain: 'J’ai mal quelque part', fine: 'Tout va bien' },
      keepQ: 'Qu’est-ce qui doit rester ?', keep: { split: 'La répartition', exercises: 'Les exercices', days: 'Les jours', pump: 'La congestion', short: 'Les séances courtes', everything: 'Tout' },
      minLead: 'Tape-le, ou utilise + et −. De 15 à 120.',
      minHint: 'Choisis un nombre entre 15 et 120.',
      unitsQ: 'Kilos ou livres ?',
      dbLb: { light: ['Une ou deux paires légères', '10 et 15 lb'], mid: ['Jusqu’à 25 lb', '10 à 25 lb'], heavy: ['Jusqu’à 45 lb', '10 à 45 lb'], adj: ['Réglables, jusqu’à 50 lb', 'Par pas de 5 lb'] },
      youTitle: 'À propos de toi',
      youLead: 'Tout est facultatif, mais ça rend le plan vraiment à toi. Touche ce qui va, puis Continuer.',
      goodQ: 'Ce que tu fais bien', good: { strong: 'Fort pour mon gabarit', engine: 'Bon cardio', flexible: 'Souple', technique: 'Bonne technique', consistent: 'Je suis régulier' },
      holdQ: 'Ce qui te freine', hold: { time: 'Le temps', motivation: 'La motivation', energy: 'L’énergie ou le sommeil', stress: 'Le stress', pain: 'Douleurs ou raideurs', know_how: 'Ne pas savoir quoi faire', bored: 'L’ennui' },
      painQ: 'Une douleur, maintenant ou avant ?',
      status: { now: 'Ça fait mal', mild: 'Seulement sur certains gestes', cleared: 'Ancienne, guérie', unchecked: 'Ancienne, jamais vérifiée' },
      triggerQ: 'Qu’est-ce qui la déclenche ?',
      trigger: { bending: 'Se pencher en avant', overhead: 'Lever les bras', impact: 'Sauter ou courir', kneeling: 'À genoux ou squat profond', gripping: 'Serrer', twisting: 'Tourner le buste' },
      sleepQ: 'Ton sommeil', sleep: { under_6: 'Moins de 6 h', '6_7': '6 à 7 h', '7_plus': '7 h +' },
      stressQ: 'Ton stress ces temps-ci', stress: { low: 'Bas', medium: 'Moyen', high: 'Élevé' },
      numbersQ: 'Des chiffres que tu connais', numbersLead: 'Une charge récente et les répétitions. Passe si tu ne sais pas.', reps: 'Répétitions',
      planTitle: 'Ton plan',
      planLead: 'D’après tes réponses, voilà ce que je te fais faire.',
      planBadge: 'Choisi pour toi',
      rethought: 'Compris. Voilà ce que je te propose à la place.',
      family: { strength: 'La force d’abord', powerbuild: 'Force et volume', muscle: 'Prise de muscle', weightlifting: 'Haltérophilie',
        functional: 'Forme complète', hyrox: 'Préparation HYROX', hybrid: 'Force et course', run: 'Course à pied', health: 'Santé, tout le corps' },
      familyLine: { strength: 'Les gros mouvements lourds d’abord, puis le travail musculaire.', powerbuild: 'Des jours lourds et des jours volume dans la même semaine.',
        muscle: 'Beaucoup de séries proches de l’échec, chaque muscle deux fois par semaine.', weightlifting: 'La technique d’abord, puis la force.',
        functional: 'Une partie force, puis du cardio rapide.', hyrox: 'Course et ateliers, construits vers le jour J.',
        hybrid: 'Musculation et course dans la même semaine, espacées pour progresser des deux côtés.', run: 'Surtout du footing facile, qui monte semaine après semaine.',
        health: 'Force sur tout le corps et cardio doux.' },
      shape: { ppl: 'Push, pull, legs', upper_lower: 'Jours haut et bas', full_body: 'Full body', body_part: 'Un muscle par jour',
        strength_cardio: 'Jours force et course', run_plan: 'Des sorties variées', classes: 'Un mélange nouveau à chaque fois' },
      about: (m) => 'Environ ' + m + ' min',
      whyFits: 'Pourquoi il te va',
      howItWorks: 'Comment ça marche',
      howLine: (name, from) => 'Construit sur ' + name + (from ? ', inspiré de ' + from : '') + '. Le coach le pilote pour toi : charges, progrès et semaines plus légères.',
      startPlan: 'Commencer ce plan', notForMe: 'Pas pour moi',
      whyNotTitle: 'Qu’est-ce qui ne va pas ?', whyNotLead: 'Dis-le-moi et je revois ma copie.',
      whyNot: { too_long: 'Séances trop longues', too_much_running: 'Trop de course', not_enjoy: 'Ça ne me plairait pas', days: 'Je ne peux pas ces jours-là' },
      oneChange: (why) => 'Un seul changement ouvrirait un meilleur plan : ' + why + '.',
      expect: 'À quoi t’attendre : les 2 à 4 premières semaines servent à apprendre les gestes et trouver tes charges. La force arrive avant le miroir. Une semaine ratée, c’est normal : tu reprends à la séance suivante.',
      notes: {
        outcome_note: 'Je n’ai pas encore de plan taillé pour cet objectif, alors je prends le plus proche, et je te le dis franchement.',
        style_note: 'Le style que tu préfères ne sert pas aussi bien ton objectif avec ta semaine, alors j’ai choisi ce qui le sert mieux.',
        improve_note: 'Pour l’instant, c’est le plan le plus proche de ta semaine actuelle. Le coaching à l’intérieur de ta propre routine arrive dans une prochaine mise à jour.',
        dose_note: 'Sommeil court ou stress élevé : les premières semaines démarrent au bas des séries, avec une répétition de plus en réserve.',
      },
    },
    engineFail: 'Un souci de mon côté. Touche Réessayer.',
  },
};
const QLANG = (() => { try { return new URLSearchParams(location.search).get('lang'); } catch (e) { return null; } })();
const LANG = (QLANG || navigator.language || 'en').toLowerCase().startsWith('fr') ? 'fr' : 'en';
const T = STR[LANG];
let UNITS = (!QLANG && (navigator.language || '') === 'en-US') ? 'lb' : 'kg';
// the engine's score line always prints kilos; a pounds user sees pounds
const scoreText = (s) => UNITS === 'lb' ? String(s || '').replace(/(\d+(?:\.\d+)?) kg/g, (m, n) => (Math.round(n * 2.20462 / 5) * 5) + ' lb') : (s || '');
let PAPER = UNITS === 'lb' ? 'Letter' : 'A4';
document.documentElement.lang = LANG;

// ─────────────────────────────────────────────────────────────── small dom kit
function h(tag, attrs, ...kids) {
  const el = document.createElement(tag);
  for (const [k, v] of Object.entries(attrs || {})) {
    if (v == null || v === false) continue;
    if (k === 'class') el.className = v;
    else if (k === 'html') el.innerHTML = v;
    else if (k.startsWith('on')) el.addEventListener(k.slice(2), v);
    else el.setAttribute(k, v === true ? '' : v);
  }
  for (const c of kids.flat()) if (c != null && c !== false) el.append(c.nodeType ? c : document.createTextNode(String(c)));
  return el;
}
function icon(id, cls) {
  const ns = 'http://www.w3.org/2000/svg';
  const s = document.createElementNS(ns, 'svg');
  s.setAttribute('class', 'ic' + (cls ? ' ' + cls : ''));
  s.setAttribute('aria-hidden', 'true');
  const u = document.createElementNS(ns, 'use');
  u.setAttribute('href', '#' + id);
  s.append(u);
  return s;
}
const mark = (cls) => icon('agent-mark', 'mark' + (cls ? ' ' + cls : ''));
const coach = (...kids) => h('div', { class: 'coach' }, mark(), h('div', {}, ...kids.map(k => typeof k === 'string' ? h('p', {}, k) : k)));
function tile({ ic, label, sub, onclick, pressed, cls, tick }) {
  return h('button', { class: 'tile ' + (cls || ''), type: 'button', onclick, 'aria-pressed': pressed == null ? null : String(!!pressed) },
    ic ? icon(ic, 'lg') : null, h('span', {}, h('b', {}, label), sub ? h('small', {}, sub) : null),
    tick ? h('span', { class: 'tick' }, icon('t-check')) : null);
}
function btn(label, onclick, kind, ic) {
  return h('button', { class: 'btn ' + (kind || ''), type: 'button', onclick }, ic ? icon(ic) : null, h('span', {}, label));
}
const decideTile = (onclick) => tile({ ic: 'i-spark', label: T.youDecide, sub: T.youDecideSub, onclick, cls: 'decide' });
const $app = () => document.getElementById('app');

let PHASE = -1;
function dots(phase) {
  PHASE = phase;
  const d = document.getElementById('dots');
  d.innerHTML = '';
  if (phase < 0) return;
  T.phases.forEach((_, i) => d.append(h('i', { class: i < phase ? 'done' : i === phase ? 'on' : '', 'aria-hidden': 'true' })));
  d.append(h('span', { class: 'steplabel' }, T.stepOf(phase + 1, T.phases.length, T.phases[phase])));
}
let TAPS = 0;
document.addEventListener('click', (e) => { if (e.target.closest('button,a,label')) TAPS++; }, true);

function show(phase, ...kids) {
  dots(phase);
  const app = $app();
  app.innerHTML = '';
  const s = h('section', { class: 'screen' }, ...kids);
  app.append(s);
  window.scrollTo(0, 0);
  return s;
}
function busy(text) {
  return show(PHASE, h('div', { class: 'coach' }, mark(), h('div', { style: 'display:flex;gap:10px;align-items:center' }, h('span', { class: 'spinner' }), h('p', {}, text))));
}
function actions(...kids) { return h('div', { class: 'actions' }, ...kids); }
function flowActions(...kids) { return h('div', { class: 'actions flow' }, ...kids); }

// ─────────────────────────────────────────────────────────────── storage (device memory)
const DB = { name: 'personal-trainer', store: 'kv', ok: true };
function idb() {
  return new Promise((resolve) => {
    let done = false;
    const fin = (v) => { if (!done) { done = true; resolve(v); } };
    setTimeout(() => fin(null), 3000);
    try {
      const r = indexedDB.open(DB.name, 1);
      r.onupgradeneeded = () => { try { r.result.createObjectStore(DB.store); } catch (e) { } };
      r.onsuccess = () => fin(r.result);
      r.onerror = () => fin(null);
      r.onblocked = () => fin(null);
    } catch (e) { fin(null); }
  });
}
async function kvGet(key) {
  try {
    const db = await idb(); if (!db) { DB.ok = false; return null; }
    return await new Promise((res) => {
      try {
        const q = db.transaction(DB.store, 'readonly').objectStore(DB.store).get(key);
        q.onsuccess = () => { res(q.result || null); db.close(); }; q.onerror = () => { res(null); db.close(); };
      } catch (e) { res(null); }
    });
  } catch (e) { DB.ok = false; return null; }
}
async function kvSet(key, val) {
  try {
    const db = await idb(); if (!db) { DB.ok = false; return false; }
    return await new Promise((res) => {
      try {
        const tx = db.transaction(DB.store, 'readwrite');
        tx.objectStore(DB.store).put(val, key);
        tx.oncomplete = () => { res(true); db.close(); }; tx.onerror = () => { res(false); db.close(); }; tx.onabort = () => { res(false); db.close(); };
      } catch (e) { res(false); }
    });
  } catch (e) { DB.ok = false; return false; }
}
const pref = {
  get(k) { try { return localStorage.getItem('pt.' + k); } catch (e) { return null; } },
  set(k, v) { try { localStorage.setItem('pt.' + k, v); } catch (e) { } },
};

// ─────────────────────────────────────────────────────────────── the engine bridge
let PY = null, BUNDLE = null;
const ROOT = '/trainer';
const PY_INIT = `
import sys, io, json, runpy, contextlib, os, traceback
os.chdir('/trainer')
def _run(argv_json):
    argv = json.loads(argv_json)
    buf, err = io.StringIO(), io.StringIO()
    sys.argv = ['plan.py', *argv]
    code = 0
    try:
        with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(err):
            runpy.run_path('/trainer/engine/plan.py', run_name='__main__')
    except SystemExit as e:
        if isinstance(e.code, int) or e.code is None:
            code = e.code or 0
        else:
            code = 1
            err.write(str(e.code))
    except Exception:
        traceback.print_exc(file=err)
        code = 1
    return json.dumps({'code': code, 'out': buf.getvalue(), 'err': err.getvalue()})
`;
function fsWalk(dir, out, base) {
  let names = [];
  try { names = PY.FS.readdir(dir); } catch (e) { return out; }
  for (const n of names) {
    if (n === '.' || n === '..') continue;
    const p = dir + '/' + n;
    const st = PY.FS.stat(p);
    if (PY.FS.isDir(st.mode)) fsWalk(p, out, base);
    else out[p.slice(base.length + 1)] = PY.FS.readFile(p);
  }
  return out;
}
function fsWrite(rel, data) {
  const full = ROOT + '/' + rel;
  PY.FS.mkdirTree(full.slice(0, full.lastIndexOf('/')));
  PY.FS.writeFile(full, data);
}
function fsRead(rel, enc) {
  try { return PY.FS.readFile(ROOT + '/' + rel, enc ? { encoding: 'utf8' } : undefined); } catch (e) { return null; }
}
function snapshot() {
  const files = {};
  fsWalk(ROOT + '/me', files, ROOT);
  fsWalk(ROOT + '/sessions', files, ROOT);
  return files;
}
function clearData() {
  for (const d of ['me', 'sessions']) {
    const files = fsWalk(ROOT + '/' + d, {}, ROOT);
    for (const rel of Object.keys(files)) { try { PY.FS.unlink(ROOT + '/' + rel); } catch (e) { } }
  }
}
async function persist() {
  try { if (!(await kvSet('snapshot', { at: Date.now(), files: snapshot() }))) DB.ok = false; } catch (e) { DB.ok = false; }
}
async function restore() {
  const snap = await kvGet('snapshot');
  if (snap && snap.files) for (const [rel, data] of Object.entries(snap.files)) { try { fsWrite(rel, data); } catch (e) { } }
  return !!snap;
}
const READ_ONLY = new Set(['status', 'match', 'week']);
async function run(cmd, args = [], files = {}) {
  for (const [name, obj] of Object.entries(files)) fsWrite('me/' + name, JSON.stringify(obj));
  const raw = JSON.parse(PY.globals.get('_run')(JSON.stringify([cmd, ...args])));
  let res = null;
  try { res = JSON.parse(raw.out); } catch (e) {
    const i = raw.out.indexOf('{');
    try { res = JSON.parse(raw.out.slice(i)); } catch (e2) { res = null; }
  }
  if (!READ_ONLY.has(cmd)) await persist();
  if (!res) {
    console.warn('engine', cmd, raw.code, raw.err);
    throw new Error('engine: ' + cmd + ' gave no answer');
  }
  return res;
}
function jsonBlock(text) {
  const m = /```json\s*\n([\s\S]*?)\n```/.exec(text || '');
  try { return m ? JSON.parse(m[1]) : null; } catch (e) { return null; }
}
const readProfile = () => jsonBlock(fsRead('me/PROFILE.md', true)) || {};
const readState = () => { try { return JSON.parse(fsRead('me/state.json', true)); } catch (e) { return null; } };
function programInfo(id) {
  const text = BUNDLE.files['doctrine/programs/' + id + '.md'] || '';
  const data = jsonBlock(text) || {};
  const m = /\*\*What it is\.\*\*\s*([^]*?\.)(\s|$)/.exec(text);
  return { data, what: m ? m[1].trim() : '' };
}

// ─────────────────────────────────────────────────────────────── the log: streak and records
// Both read me/log.jsonl, the line the engine appends after every logged session. Nothing new is stored.
function readLog() {
  const text = fsRead('me/log.jsonl', true) || '';
  const out = [];
  for (const line of text.split('\n')) { if (!line.trim()) continue; try { out.push(JSON.parse(line)); } catch (e) { } }
  return out;
}
let BANK_NAMES = null;
function bankName(id) {
  if (!BANK_NAMES) {
    BANK_NAMES = {};
    const csv = (BUNDLE && BUNDLE.files['doctrine/exercises/bank.csv']) || '';
    for (const line of csv.split('\n').slice(1)) {
      const m = /^([^,]+),("([^"]*)"|[^,]*)/.exec(line);
      if (m) BANK_NAMES[m[1]] = m[3] != null ? m[3] : m[2];
    }
  }
  return BANK_NAMES[id] || String(id || '').replace(/_/g, ' ');
}
const isoDay = (d) => d.getFullYear() + '-' + String(d.getMonth() + 1).padStart(2, '0') + '-' + String(d.getDate()).padStart(2, '0');
function streakData(weeks) {
  const counts = {};
  for (const l of readLog()) if (!l.unreported && l.date && l.mode !== 'rest') counts[l.date] = (counts[l.date] || 0) + 1;
  const today = new Date(); today.setHours(12, 0, 0, 0);
  const monday = new Date(today); monday.setDate(today.getDate() - ((today.getDay() + 6) % 7));
  const start = new Date(monday); start.setDate(monday.getDate() - 7 * (weeks - 1));
  const days = [], perWeek = [];
  let total = 0;
  for (let i = 0; i < weeks * 7; i++) {
    const d = new Date(start); d.setDate(start.getDate() + i);
    const iso = isoDay(d), n = counts[iso] || 0;
    days.push({ iso, n, day: d.getDate(), today: iso === isoDay(today), future: d > today });
    total += n;
    perWeek[Math.floor(i / 7)] = (perWeek[Math.floor(i / 7)] || 0) + n;
  }
  // weeks in a row with at least one session; the current week does not break it before it is over
  let streak = 0, w = weeks - 1;
  if (!perWeek[w]) w--;
  while (w >= 0 && perWeek[w]) { streak++; w--; }
  return { days, total, streak, weeks };
}
function records(log) {
  const best = {};
  for (const l of log || readLog()) {
    if (l.unreported) continue;
    const info = {};
    try {
      const s = JSON.parse(fsRead(l.session, true));
      for (const b of s.blocks || []) for (const it of b.items || []) if (it._slot) info[it._slot.key] = { name: it.name, main: b.kind === 'main' || b.kind === 'secondary' };
    } catch (e) { }
    for (const d of l.done || []) {
      const r = d.result || {}, load = Number(r.load), reps = (r.reps || []).map(Number).filter(n => n > 0);
      if (d.skipped || !load || !reps.length) continue;
      const top = Math.max(...reps), e1rm = load * (1 + top / 30), meta = info[d.key] || {};
      const cur = best[d.ex];
      if (!cur || e1rm > cur.e1rm + 1e-6) best[d.ex] = { ex: d.ex, load, reps: top, e1rm, date: l.date, name: meta.name || bankName(d.ex), main: meta.main !== false };
    }
  }
  const all = Object.values(best);
  const mains = all.filter(r => r.main);
  return (mains.length ? mains : all).sort((a, b) => b.e1rm - a.e1rm);
}
const prText = (r) => kgToUnits(r.load) + ' ' + UNITS + ' × ' + r.reps;
function streakCard() {
  const S = streakData(6);
  const grid = h('div', { class: 'cal', role: 'img', 'aria-label': T.streakCount(S.total, S.weeks) },
    T.dow.map(x => h('span', { class: 'dow', 'aria-hidden': 'true' }, x)),
    S.days.map(d => h('span', { class: 'd' + (d.n ? ' on' : '') + (d.today ? ' today' : '') + (d.future ? ' future' : ''), title: d.iso + (d.n ? ' · ' + d.n : '') },
      d.n > 1 ? '×' + d.n : d.n || d.today ? String(d.day) : '')));
  return h('div', { class: 'card streak' },
    h('p', { class: 'kicker' }, icon('t-flame'), T.streakTitle),
    S.total ? h('p', { class: 'small' }, h('b', {}, T.streakWeeks(S.streak)), h('span', { class: 'muted' }, ' · ' + T.streakCount(S.total, S.weeks))) : h('p', { class: 'muted small' }, T.streakNone),
    grid);
}
function recordsCard(list, fresh) {
  const isNew = new Set((fresh || []).map(r => r.ex));
  return h('div', { class: 'card prs' + (fresh ? ' record' : '') },
    h('p', { class: 'kicker' }, icon('t-trophy'), fresh ? T.recordTitle(fresh.length) : T.prTitle),
    fresh ? h('p', { class: 'small', style: 'margin:6px 0 0' }, T.recordLine) : null,
    list.length ? h('div', { class: 'list' }, list.slice(0, 6).map(r => h('div', { class: 'row' + (isNew.has(r.ex) ? ' new' : '') },
      h('span', { class: 'lift' }, h('b', {}, r.name), isNew.has(r.ex) && !fresh ? h('span', { class: 'new-tag' }, T.prNew) : null),
      h('span', { class: 'best' }, prText(r)))))
      : h('p', { class: 'muted small', style: 'margin:8px 0 0' }, T.prNone));
}
function freshRecords(before, after) {
  const was = {}; for (const r of before) was[r.ex] = r.e1rm;
  // a record falls when a lift beats its own best; a lift's first outing is a baseline, not a record
  return after.filter(r => was[r.ex] != null && r.e1rm > was[r.ex] + 1e-6);
}

// ─────────────────────────────────────────────────────────────── capabilities (claude.ai runtime)
const CAP = { sample: null, downloads: null };
function resolveCaps() {
  try {
    if (!window.claude || typeof window.claude.use !== 'function') return;
    window.claude.use('sample').then(f => { CAP.sample = f || null; }).catch(() => { });
    window.claude.use('downloads').then(f => { CAP.downloads = f || null; }).catch(() => { });
  } catch (e) { }
}
async function saveFile(filename, data, mime) {
  const blob = data instanceof Blob ? data : new Blob([data], { type: mime });
  if (CAP.downloads) {
    try { await CAP.downloads.save({ filename, data: blob }); return 'saved'; }
    catch (e) { return e && e.code === 'declined' ? 'declined' : 'fail'; }
  }
  try {
    const url = URL.createObjectURL(blob);
    const a = h('a', { href: url, download: filename, style: 'display:none' });
    document.body.append(a); a.click(); a.remove();
    setTimeout(() => URL.revokeObjectURL(url), 30000);
    return 'saved';
  } catch (e) { return 'fail'; }
}

// ─────────────────────────────────────────────────────────────── boot
function bootStep(i, pct) {
  const b = document.getElementById('boot-bar'), s = document.getElementById('boot-step');
  if (b) b.style.width = pct + '%';
  if (s) s.textContent = T.boot[i];
}
async function boot() {
  document.getElementById('brand-name').textContent = T.brand;
  const tt = document.querySelector('.loading .title'); if (tt) tt.textContent = T.bootTitle;
  const bl = document.getElementById('boot-lead'); if (bl) bl.textContent = T.bootLead;
  const st = document.getElementById('boot-slow-text'); if (st) st.textContent = T.bootSlow;
  const rl = document.getElementById('boot-reload'); if (rl) rl.textContent = T.reload;
  const slow = setTimeout(() => { const el = document.getElementById('boot-slow'); if (el) el.hidden = false; }, 20000);
  const theme = pref.get('theme'); if (theme && theme !== 'auto') document.documentElement.dataset.theme = theme;
  resolveCaps();
  try {
    bootStep(1, 12);
    let creep = 12;
    const timer = setInterval(() => { creep = Math.min(68, creep + 3); const b = document.getElementById('boot-bar'); if (b) b.style.width = creep + '%'; }, 400);
    const bundleP = fetch('bundle.json').then(r => r.json());
    PY = await loadPyodide({ indexURL: new URL('pyodide/', location.href).href, stdLibURL: new URL('pyodide/python_stdlib.zip.wasm', location.href).href });
    clearInterval(timer);
    bootStep(2, 74);
    BUNDLE = await bundleP;
    for (const [path, text] of Object.entries(BUNDLE.files)) fsWrite(path, text);
    PY.FS.mkdirTree(ROOT + '/me'); PY.FS.mkdirTree(ROOT + '/sessions');
    PY.runPython(PY_INIT);
    bootStep(3, 88);
    await restore();
    bootStep(4, 100);
    document.getElementById('settings-btn').hidden = false;
    document.getElementById('settings-btn').setAttribute('aria-label', T.settings);
    document.getElementById('settings-btn').onclick = settings;
    window.__trainerReady = performance.now();
    clearTimeout(slow);
    await route();
  } catch (e) {
    clearTimeout(slow);
    console.error(e);
    show(-1, h('h1', { class: 'title' }, T.bootTitle), coach(T.bootFail), actions(btn(T.reload, () => location.reload(), 'primary', 't-reset')));
  }
}

// ─────────────────────────────────────────────────────────────── routing, always from status
async function route() {
  let st;
  try { st = await run('status'); } catch (e) { return fail(); }
  const u = readProfile().units;
  if (u === 'kg' || u === 'lb') setUnits(u);
  if (st.stage !== 'new' && st.screen_due) return safety(true);
  switch (st.stage) {
    case 'new': return welcome();
    case 'screen_stopped':
    case 'screen_needs_ok': return paused(st);
    case 'interview': return interview();
    case 'needs_program': return programs();
    case 'pending_log': return howItWent(st.pending);
    case 'ready': return readyHome(st);
    default: return welcome();
  }
}
function fail() {
  show(PHASE, coach(T.engineFail), actions(btn(T.tryAgain, route, 'primary', 't-reset')));
}

// ─────────────────────────────────────────────────────────────── welcome and safety
function welcome() {
  show(-1,
    mark('hero'),
    h('h1', { class: 'title', html: T.welcomeTitle }),
    coach(T.welcomeLead),
    h('p', { class: 'muted small' }, icon('i-lock'), ' ', T.welcomeNote),
    actions(btn(T.start, () => safety(false), 'primary', 'i-arrow-right')));
}

function safety(yearly, preset) {
  const picked = new Set(preset ? preset.items : []);
  let none = false;
  const go = btn(T.cont, submit, 'primary', 'i-arrow-right');
  const hint = h('p', { class: 'hint', role: 'status' });
  const refresh = () => {
    const ready = !!(none || picked.size);
    go.disabled = !ready;
    hint.textContent = ready ? '' : T.safetyHint;
    hint.hidden = ready;
  };
  const cards = T.safety.map((label, i) => {
    const n = i + 1;
    const el = tile({ label, tick: true, pressed: picked.has(n), onclick: () => {
      if (picked.has(n)) picked.delete(n); else picked.add(n);
      el.setAttribute('aria-pressed', String(picked.has(n)));
      none = false; noneEl.setAttribute('aria-pressed', 'false'); refresh();
    } });
    return el;
  });
  const noneEl = tile({ ic: 'i-shield', label: T.noneOfThese, sub: T.noneSub, tick: true, pressed: false, cls: 'big', onclick: () => {
    none = !none; if (none) { picked.clear(); cards.forEach(c => c.setAttribute('aria-pressed', 'false')); }
    noneEl.setAttribute('aria-pressed', String(none)); refresh();
  } });
  async function submit() {
    busy(T.saving);
    let r;
    try { r = await run('screen', ['me/answers.json'], { 'answers.json': { items: [...picked].sort((a, b) => a - b), language: LANG } }); }
    catch (e) { return fail(); }
    afterScreen(r, [...picked]);
  }
  refresh();
  show(0,
    yearly ? null : h('button', { class: 'back', type: 'button', onclick: welcome }, icon('t-back'), T.back),
    h('h1', { class: 'title' }, T.safetyTitle),
    coach(T.safetyLead),
    h('div', { class: 'tiles one' }, cards, noneEl),
    actions(hint, go));
}

function screenMessage(r) {
  const reasons = r.reasons || [];
  const parts = reasons.map(x => T.screenMsg[x]).filter(Boolean);
  if ((r.flags || []).includes('symptoms_reported') || ((r.items || []).some(i => i === 2 || i === 3))) parts.push(T.screenMsg.symptoms);
  return parts.length ? parts.join(' ') : (r.message || '');
}
function afterScreen(r, items) {
  if (r.result === 'clear') {
    const ed = (r.flags || []).includes('no_fat_loss_goal');
    return interview(ed ? [T.clearLine, T.edLine] : [T.clearLine]);
  }
  paused({ stage: r.result === 'stop' ? 'screen_stopped' : 'screen_needs_ok', reasons: r.reasons, fresh: true, items, flags: r.flags });
}

function paused(st) {
  const prof = readProfile();
  const scr = prof.screen || {};
  const items = st.items || scr.items || [];
  const reasons = st.reasons || scr.reasons || [];
  const stop = st.stage === 'screen_stopped';
  const msg = screenMessage({ reasons, items, flags: st.flags || scr.flags });
  const again = async (extra) => {
    busy(T.saving);
    let r;
    try { r = await run('screen', ['me/answers.json'], { 'answers.json': Object.assign({ items, language: LANG }, extra) }); }
    catch (e) { return fail(); }
    afterScreen(r, items);
  };
  const confirmOk = (extra) => show(0, h('h1', { class: 'title' }, stop ? T.pauseTitle : T.holdTitle), coach(T.clearedConfirm),
    actions(btn(T.yesCleared, () => again(extra), 'primary', 'i-badge-check'), btn(T.notYet, () => paused(st), 'ghost')));
  const epar = reasons.includes('parq') ? h('p', {}, h('a', { class: 'inline', href: 'https://eparmedx.com', target: '_blank', rel: 'noopener' }, T.eparLink)) : null;
  const wait = () => show(0, h('button', { class: 'back', type: 'button', onclick: () => paused(st) }, icon('t-back'), T.back),
    h('h1', { class: 'title' }, stop ? T.pauseTitle : T.holdTitle), coach(T.waitLine, epar),
    actions(btn(T.back, () => paused(st), '', 't-back')));
  const buttons = [];
  if (reasons.includes('under_18')) {
    buttons.push(btn(T.mistake, () => safety(false, { items }), 'ghost'));
  } else if (stop) {
    buttons.push(btn(T.checkFirst, wait, 'primary', 't-check'));
    buttons.push(btn(T.cleared, () => confirmOk({ cleared: true }), '', 'i-badge-check'));
    buttons.push(btn(T.mistake, () => mistake(items), 'ghost', 't-back'));
  } else {
    const okKey = reasons.includes('pregnancy') ? { provider_ok: true } : {};
    if (reasons.includes('diabetes')) okKey.doctor_ok = true;
    buttons.push(btn(reasons.includes('pregnancy') ? T.providerOk : T.doctorOk, () => confirmOk(okKey), 'primary', 'i-badge-check'));
    buttons.push(btn(T.mistake, () => mistake(items), '', 't-back'));
  }
  if (!stop || reasons.includes('under_18')) buttons.push(btn(T.notYet, wait, 'ghost'));
  show(0,
    h('h1', { class: 'title' }, st.fresh ? (stop ? T.pauseTitle : T.holdTitle) : T.returnTitle),
    st.fresh ? coach(msg, epar) : coach(T.returnLead, h('p', { class: 'muted small' }, msg), epar),
    actions(...buttons));
}

function mistake(items) {
  const keep = new Set(items);
  const go = btn(T.confirm, async () => {
    busy(T.saving);
    let r;
    try { r = await run('screen', ['me/answers.json'], { 'answers.json': { items: [...keep], language: LANG, correction: true } }); }
    catch (e) { return fail(); }
    afterScreen(r, [...keep]);
  }, 'primary', 't-check');
  show(0,
    h('button', { class: 'back', type: 'button', onclick: route }, icon('t-back'), T.back),
    h('h1', { class: 'title' }, T.mistakeTitle),
    coach(T.mistakeLead),
    h('div', { class: 'tiles one' }, items.map(n => {
      const el = tile({ label: T.safety[n - 1], tick: true, pressed: true, onclick: () => {
        if (keep.has(n)) keep.delete(n); else keep.add(n);
        el.setAttribute('aria-pressed', String(keep.has(n)));
      } });
      return el;
    })),
    actions(go));
}

// ─────────────────────────────────────────────────────────────── the interview
// The contract is doctrine/02_INTERVIEW.md. The person says what they want, what they have done and what they enjoy;
// the engine decides the plan (doctrine/03_MATRIX.md). Nobody picks a method. Only experienced people, or someone
// improving their own routine, may name a style they prefer, and "Let the trainer decide" comes first.
const OUTCOME_IC = { look: 't-muscle', strong: 't-barbell', athletic: 'i-bolt', event: 't-flag', keep_going: 'i-trend-up' };
const OUTCOME_GOAL = { look: { size: 'muscle', lean: 'fat_loss' }, strong: { general: 'strength', powerlifting: 'powerlifting', olympic: 'weightlifting' },
  athletic: { crossfit: 'functional', hybrid: 'functional' }, event: { run_5k_10k: 'run', run_half: 'run', run_marathon: 'run', hyrox: 'hyrox', meet: 'powerlifting' },
  keep_going: { lifting: 'muscle', fitness: 'functional', mix: 'health' } };   // engine/core.py OUTCOMES, the main goal of each
const OUTCOME_DEFAULT = { look: 'size', strong: 'general', athletic: 'crossfit', event: 'run_5k_10k', keep_going: 'mix' };
const ACT_IC = { lifting: 't-barbell', running: 't-runner', cardio: 't-circuit', classes: 't-mix', crossfit: 't-flag' };
const STYLE_IC = { trainer: 'i-spark', strength: 't-barbell', bodybuilding: 't-muscle', powerbuilding: 't-trophy', crossfit: 't-circuit',
  hyrox: 't-flag', running: 't-runner', hybrid: 't-mix' };
const SPLIT_IC = { ppl: 't-mix', upper_lower: 't-stairs', full_body: 't-muscle', body_part: 't-barbell', strength_cardio: 't-runner',
  run_plan: 't-runner', classes: 't-circuit', custom: 'i-tools' };
const SPLIT_DAYS = { ppl: ['push', 'pull', 'legs'], upper_lower: ['upper', 'lower'], full_body: ['fa', 'fb', 'fc'],
  body_part: ['chest', 'back', 'legs', 'shoulders', 'arms'], strength_cardio: ['strength', 'cardio'], run_plan: ['easy', 'intervals', 'long'],
  classes: ['class'], custom: ['d1', 'd2', 'd3', 'd4', 'd5', 'd6'] };
const DAY_EX = { push: ['bench_press', 'overhead_press', 'incline_db_press', 'dip', 'lateral_raise'],
  pull: ['pull_up', 'barbell_row', 'lat_pulldown', 'face_pull', 'db_curl'],
  legs: ['back_squat', 'romanian_deadlift', 'leg_press', 'leg_extension', 'calf_raise'],
  upper: ['bench_press', 'barbell_row', 'overhead_press', 'lat_pulldown', 'db_curl'],
  lower: ['back_squat', 'romanian_deadlift', 'leg_press', 'walking_lunge', 'calf_raise'],
  full: ['back_squat', 'bench_press', 'barbell_row', 'romanian_deadlift', 'overhead_press'],
  chest: ['bench_press', 'incline_db_press', 'dip', 'db_bench_press'], back: ['deadlift', 'pull_up', 'barbell_row', 'lat_pulldown'],
  shoulders: ['overhead_press', 'seated_db_press', 'lateral_raise', 'face_pull'], arms: ['db_curl', 'dip', 'chin_up'] };
const DAY_KIND = { fa: 'full', fb: 'full', fc: 'full', strength: 'full', d1: 'full', d2: 'full', d3: 'full', d4: 'full', d5: 'full', d6: 'full' };
const NO_LIST = new Set(['cardio', 'easy', 'intervals', 'long', 'class']);
const NUM_LIFTS = ['back_squat', 'bench_press', 'deadlift', 'overhead_press'];
const DB_SETS = { light: [4, 8], mid: [4, 8, 12], heavy: [4, 6, 8, 10, 12, 14, 16, 18, 20], adj: [2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24] };
const DB_SETS_LB = { light: [10, 15], mid: [10, 15, 20, 25], heavy: [10, 15, 20, 25, 30, 35, 40, 45], adj: [5, 10, 15, 20, 25, 30, 35, 40, 45, 50] };
const KIT_IC = { full_gym: 't-gym', basic_gym: 't-barbell', crossfit_box: 't-circuit' };
// A home gym is ticked item by item; each item is the bank's equipment tags (doctrine/exercises/README.md).
const HOME_KIT = { rack: ['barbell', 'rack', 'plates'], bench: ['bench'], dumbbell: ['dumbbell'], kettlebell: ['kettlebell'], pullup_bar: ['pullup_bar'],
  band: ['band'], rower: ['rower'], bike: ['bike'], skierg: ['skierg'], treadmill: ['treadmill'] };
const HOME_IC = { rack: 't-barbell', bench: 't-seat', dumbbell: 't-dumbbell', kettlebell: 't-kettlebell', pullup_bar: 't-pullup', band: 't-stretch',
  rower: 't-circuit', bike: 't-circuit', skierg: 't-circuit', treadmill: 't-runner' };
const HOME_REAL = ['rack', 'dumbbell', 'rower', 'bike', 'skierg', 'treadmill'];   // real kit (engine/core.py REAL_KIT); kettlebells or bands alone are not
const MIN_RANGE = [15, 120];                                                      // engine/core.py MINUTES_RANGE

function setUnits(u) { UNITS = u; PAPER = u === 'lb' ? 'Letter' : 'A4'; }
const pressChip = (label, on, toggle, ic) => {
  const c = h('button', { class: 'chip', type: 'button', 'aria-pressed': String(!!on), onclick: () => c.setAttribute('aria-pressed', String(!!toggle())) }, ic ? icon(ic) : null, label);
  return c;
};
const setChips = (set, entries, max) => h('div', { class: 'chips' }, entries.map(([k, v]) => pressChip(v, set.has(k), () => {
  if (set.has(k)) set.delete(k); else if (!max || set.size < max) set.add(k);
  return set.has(k);
})));
function segOf(options, value, onpick) {
  const el = h('div', { class: 'seg' });
  const draw = (v) => {
    el.innerHTML = '';
    for (const [k, label] of options) el.append(h('button', { type: 'button', 'aria-pressed': String(v === k), onclick: () => { draw(k); onpick(k); } }, label));
  };
  draw(value);
  return el;
}
// A number the person can type or step: the minutes, 15 to 120 (never four cards).
function numField({ value, min, max, step, unit, onchange }) {
  const input = h('input', { class: 'numin', type: 'number', inputmode: 'numeric', min, max, step: 1, value, 'aria-label': unit });
  const ok = () => { const n = Number(input.value); return Number.isInteger(n) && n >= min && n <= max; };
  const fire = () => onchange(ok() ? Number(input.value) : null);
  input.addEventListener('input', fire);
  const bump = (d) => { const n = Number(input.value) || value; input.value = Math.max(min, Math.min(max, Math.round((n + d) / step) * step)); fire(); };
  const el = h('div', { class: 'stepper' },
    h('button', { type: 'button', 'aria-label': T.less, onclick: () => bump(-step) }, icon('t-minus')),
    input, h('span', { class: 'muted' }, unit),
    h('button', { type: 'button', 'aria-label': T.more, onclick: () => bump(step) }, icon('i-plus')));
  el.setValue = (n) => { input.value = n; fire(); };
  return el;
}

function interview(lines) {
  const prof = readProfile();
  const ed = ((prof.screen || {}).flags || []).includes('no_fat_loss_goal');
  const V = T.iv;
  const A = { units: UNITS, paper: PAPER, units_confirmed: false, language: LANG, enjoys: [], avoids: [], likes: [], dislikes: [], limits: [],
    priority: [], skills: [], numbers: {}, strengths: [], barriers: [] };
  let picks = [];                          // the outcomes, in tap order; the first is the main one
  const stack = [];
  const step = (fn) => { stack.push(fn); fn(); };
  const back = () => { if (stack.length <= 1) return safety(false); stack.pop(); stack[stack.length - 1](); };
  const backBtn = () => h('button', { class: 'back', type: 'button', onclick: back }, icon('t-back'), T.back);
  const title = (t) => h('h1', { class: 'title' }, t);
  const levels = () => Object.values(A.experience_by || {});
  const experienced = () => A.mode === 'improve' || levels().some(l => l === 'intermediate' || l === 'advanced');
  const mainGoal = () => OUTCOME_GOAL[picks[0]][A.outcome_detail || OUTCOME_DEFAULT[picks[0]]];
  const runs = () => picks.some((o, i) => o === 'event' && OUTCOME_GOAL.event[i === 0 ? (A.outcome_detail || 'run_5k_10k') : 'run_5k_10k'] === 'run')
    || (picks[0] === 'athletic' && A.outcome_detail === 'hybrid');

  // the fork
  function fork() {
    const go = (m) => { A.mode = m; step(outcomes); };
    show(1, backBtn(), title(V.forkTitle), coach(...(lines || []).filter(x => x !== T.clearLine), V.forkLead),
      h('div', { class: 'tiles one' },
        tile({ ic: 'i-spark', label: V.fork.new[0], sub: V.fork.new[1], cls: 'big', onclick: () => go('new') }),
        tile({ ic: 'i-trend-up', label: V.fork.improve[0], sub: V.fork.improve[1], cls: 'big', onclick: () => go('improve') })));
  }
  // outcome first, up to three; the first tap is the main one
  function outcomes() {
    const hint = h('p', { class: 'hint', role: 'status' });
    const go = btn(T.cont, () => {
      if (A._mainWas !== picks[0]) { delete A.outcome_detail; delete A.event; }
      A._mainWas = picks[0];
      step(follow);
    }, 'primary', 'i-arrow-right');
    const cards = {};
    const draw = () => {
      for (const [k, el] of Object.entries(cards)) {
        const i = picks.indexOf(k);
        el.setAttribute('aria-pressed', String(i >= 0));
        el.querySelector('.order').textContent = i === 0 ? V.main : i > 0 ? V.also : '';
      }
      go.disabled = !picks.length; hint.hidden = !!picks.length; hint.textContent = picks.length ? '' : V.outcomeHint;
    };
    for (const k of Object.keys(V.outcome)) {
      const el = tile({ ic: OUTCOME_IC[k], label: V.outcome[k][0], sub: V.outcome[k][1], tick: true, onclick: () => {
        const i = picks.indexOf(k);
        if (i >= 0) picks.splice(i, 1); else if (picks.length < 3) picks.push(k);
        draw();
      } });
      el.querySelector('span').append(h('em', { class: 'order' }));
      cards[k] = el;
    }
    draw();
    show(1, backBtn(), title(V.outcomeTitle), coach(V.outcomeLead),
      h('div', { class: 'tiles one' }, Object.values(cards),
        decideTile(() => { picks = ['keep_going']; draw(); A._mainWas = 'keep_going'; A.outcome_detail = 'mix'; step(afterFollow); })),
      actions(hint, go));
  }
  // one follow-up, for the main outcome
  function follow() {
    const o = picks[0];
    const opts = Object.keys(V.follow[o].opts).filter(k => !(ed && k === 'lean'));
    const pick = (k) => { A.outcome_detail = k; step(o === 'event' ? eventDate : afterFollow); };
    show(1, backBtn(), title(V.follow[o].q),
      h('div', { class: 'tiles one' }, opts.map(k => tile({ ic: OUTCOME_IC[o], label: V.follow[o].opts[k][0], sub: V.follow[o].opts[k][1], onclick: () => pick(k) })),
        decideTile(() => pick(OUTCOME_DEFAULT[o]))));
  }
  function eventDate() {
    const ev = A.event || {};
    const input = h('input', { class: 'field', type: 'date', value: ev.date || '', 'aria-label': V.dateQ });
    const go = (date) => { A.event = { name: V.follow.event.opts[A.outcome_detail][0], date: date || null }; step(afterFollow); };
    show(1, backBtn(), title(V.dateQ), coach(V.dateLead), input,
      actions(btn(T.cont, () => go(input.value), 'primary', 'i-arrow-right'), btn(V.noDate, () => go(null), 'ghost')));
  }
  function afterFollow() { if (picks.length > 1) balance(); else afterOutcome(); }
  // the blend: how much of the week each outcome gets
  function balance() {
    const W = { little: 1, some: 2, lots: 3 };
    const w = Object.assign({}, A._weights || {});
    picks.forEach((k, i) => { if (!w[k]) w[k] = i === 0 ? 'lots' : 'some'; });
    const save = () => {
      const tot = picks.reduce((s, k) => s + W[w[k]], 0);
      A._weights = w;
      A.outcomes = picks.map((k, i) => ({ id: k, detail: i === 0 ? (A.outcome_detail || OUTCOME_DEFAULT[k]) : OUTCOME_DEFAULT[k], share: Math.round(100 * W[w[k]] / tot) / 100 }));
      const drift = 1 - A.outcomes.reduce((s, o) => s + o.share, 0);
      A.outcomes[0].share = Math.round((A.outcomes[0].share + drift) * 100) / 100;
      afterOutcome();
    };
    show(1, backBtn(), title(V.balanceTitle), coach(V.balanceLead),
      picks.map(k => h('div', { class: 'group' }, h('h2', {}, icon(OUTCOME_IC[k]), ' ', V.outcome[k][0]),
        segOf(Object.keys(W).map(x => [x, V.weight[x]]), w[k], (x) => { w[k] = x; }))),
      actions(btn(T.cont, save, 'primary', 'i-arrow-right'), btn(T.youDecide, () => { picks.forEach((k, i) => { w[k] = i === 0 ? 'lots' : 'some'; }); save(); }, 'ghost')));
  }
  function afterOutcome() {
    if (picks.length < 2) delete A.outcomes;
    A.outcome = picks[0];
    A.outcome_detail = A.outcome_detail || OUTCOME_DEFAULT[picks[0]];
    if (A.mode === 'improve') step(split); else step(history);
  }
  // the new path: what you have done, as activities, then how long
  function history() {
    const set = new Set(A.done_before || []);
    const go = btn(T.cont, () => { A.done_before = [...set]; step(set.size ? experience : enjoy); }, 'primary', 'i-arrow-right');
    const cards = Object.keys(V.act).map(k => {
      const el = tile({ ic: ACT_IC[k], label: V.act[k], tick: true, pressed: set.has(k), onclick: () => {
        if (set.has(k)) set.delete(k); else set.add(k);
        el.setAttribute('aria-pressed', String(set.has(k)));
      } });
      return el;
    });
    show(1, backBtn(), title(V.historyTitle), coach(V.historyLead),
      h('div', { class: 'tiles one' }, cards,
        tile({ ic: 't-lvl1', label: V.nothingYet, sub: V.nothingYetSub, cls: 'decide', onclick: () => { A.done_before = []; A.experience_by = {}; delete A.returning; step(enjoy); } })),
      actions(go));
  }
  function experience() {
    const by = Object.assign({}, A.experience_by || {});
    let ret = !!A.returning;
    const rows = A.done_before.map(k => h('div', { class: 'group' }, h('h2', {}, icon(ACT_IC[k]), ' ', V.act[k]),
      segOf(['novice', 'intermediate', 'advanced'].map(l => [l, V.howLong[l]]), by[k], (l) => { by[k] = l; })));
    show(1, backBtn(), title(V.expTitle), coach(V.expLead), ...rows,
      h('div', { class: 'chips' }, pressChip(V.returning, ret, () => (ret = !ret), 'i-calendar')),
      actions(btn(T.cont, () => {
        A.experience_by = {}; for (const k of A.done_before) A.experience_by[k] = by[k] || 'novice';
        if (ret) A.returning = true; else delete A.returning;
        step(experienced() ? style : enjoy);
      }, 'primary', 'i-arrow-right')));
  }
  // experienced people, or the improve path, only: an optional preferred style; the trainer deciding comes first
  function style() {
    const pick = (k) => { A.style_pref = k; step(A.mode === 'improve' ? minutes : enjoy); };
    show(1, backBtn(), title(V.styleTitle), coach(V.styleLead),
      h('div', { class: 'tiles' }, Object.keys(V.style).map(k => tile({ ic: STYLE_IC[k], label: V.style[k], cls: k === 'trainer' ? 'decide' : '', onclick: () => pick(k) }))));
  }
  function enjoy() {
    const like = new Set(A.enjoys), hate = new Set(A.avoids);
    let kit = A.kit_pref || 'either';
    const entries = Object.entries(V.enjoy);
    show(1, backBtn(), title(V.enjoyTitle), coach(V.enjoyLead),
      h('div', { class: 'group' }, h('h2', {}, V.enjoyQ), setChips(like, entries)),
      h('div', { class: 'group' }, h('h2', {}, V.avoidQ), setChips(hate, entries)),
      h('div', { class: 'group' }, h('h2', {}, V.kitQ), segOf(Object.entries(V.kitPref), kit, (k) => { kit = k; })),
      actions(btn(T.cont, () => {
        A.enjoys = [...like]; A.avoids = [...hate].filter(x => !like.has(x)); A.kit_pref = kit;
        step(days);
      }, 'primary', 'i-arrow-right')));
  }
  // the improve path: their routine, with low effort
  function split() {
    const pick = (k) => { A._split = k; step(routineDays); };
    show(1, backBtn(), title(V.splitTitle), coach(V.splitLead),
      h('div', { class: 'tiles one' }, Object.keys(V.split).map(k => tile({ ic: SPLIT_IC[k], label: V.split[k][0], sub: V.split[k][1], onclick: () => pick(k) }))));
  }
  function routineDays() {
    show(1, backBtn(), title(V.rdaysTitle),
      h('div', { class: 'tiles' }, [2, 3, 4, 5, 6].map(n => tile({ ic: 'i-calendar', label: n + ' ' + T.daysUnit(n), onclick: () => { A.days = n; step(exercises); } }))));
  }
  function dayLabels() {
    const base = SPLIT_DAYS[A._split];
    return Array.from({ length: A.days }, (_, i) => base[i % base.length]);
  }
  function exercises() {
    const labels = [...new Set(dayLabels())].filter(l => !NO_LIST.has(l));
    if (!labels.length) { A._ex = {}; return step(routineAge); }
    const ex = A._ex && A._exSplit === A._split ? A._ex : {};
    const own = {};
    const groups = labels.map(l => {
      const list = DAY_EX[DAY_KIND[l] || l] || DAY_EX.full;
      const set = ex[l] ? new Set(ex[l].filter(x => list.includes(x))) : new Set(list.slice(0, 3));
      own[l] = ex[l] ? ex[l].filter(x => !list.includes(x)) : [];
      ex[l] = set;
      const ownBox = h('div', { class: 'chips' });
      const drawOwn = () => { ownBox.innerHTML = ''; own[l].forEach((n, i) => ownBox.append(pressChip(n, true, () => { own[l].splice(i, 1); drawOwn(); return false; }, 't-check'))); };
      drawOwn();
      const input = h('input', { class: 'field', type: 'text', placeholder: V.typeEx, 'aria-label': V.typeEx });
      const add = () => { const n = input.value.trim(); if (n) { own[l].push(n); input.value = ''; drawOwn(); } };
      input.addEventListener('keydown', (e) => { if (e.key === 'Enter') add(); });
      return h('div', { class: 'group' }, h('h2', {}, V.dayName[l] || l),
        setChips(set, list.map(id => [id, bankName(id)])), ownBox,
        h('div', { class: 'addrow' }, input, btn(V.add, add, '', 'i-plus')));
    });
    show(1, backBtn(), title(V.exTitle), coach(V.exLead), ...groups,
      actions(btn(T.cont, () => {
        A._exSplit = A._split;
        A._ex = Object.fromEntries(labels.map(l => [l, [...ex[l], ...own[l]]]));
        step(routineAge);
      }, 'primary', 'i-arrow-right')));
  }
  function routineAge() {
    show(1, backBtn(), title(V.ageTitle),
      h('div', { class: 'tiles one' }, Object.keys(V.age).map(k => tile({ ic: 'i-calendar', label: V.age[k], onclick: () => { A._age = k; step(going); } }))));
  }
  function going() {
    const stalls = new Set(A._stalls || []), keep = new Set(A._keep || []);
    show(1, backBtn(), title(V.goingTitle), coach(V.goingLead),
      h('div', { class: 'group' }, h('h2', {}, V.stallQ), setChips(stalls, Object.entries(V.stall))),
      h('div', { class: 'group' }, h('h2', {}, V.keepQ), setChips(keep, Object.entries(V.keep))),
      actions(btn(T.cont, () => {
        A._stalls = [...stalls]; A._keep = [...keep];
        const labels = dayLabels();
        A.current_routine = { split: A._split, days: A.days, day_labels: labels.map(l => V.dayName[l] || l), age: A._age,
          stalls: A._stalls, keep: A._keep,
          exercises: Object.fromEntries(Object.entries(A._ex || {}).map(([l, list]) => [V.dayName[l] || l, list])) };
        step(style);
      }, 'primary', 'i-arrow-right')));
  }
  // the week
  function days() {
    show(1, backBtn(), title(T.daysTitle),
      h('div', { class: 'tiles' }, [2, 3, 4, 5, 6].map(n => tile({ ic: 'i-calendar', label: n + ' ' + T.daysUnit(n), onclick: () => { A.days = n; step(minutes); } })),
        decideTile(() => { A.days = 3; step(minutes); })));
  }
  function minutes() {
    let val = A.minutes || 45;
    const hint = h('p', { class: 'hint', role: 'status', hidden: true });
    const go = btn(T.cont, () => { A.minutes = val; step(where); }, 'primary', 'i-arrow-right');
    const field = numField({ value: val, min: MIN_RANGE[0], max: MIN_RANGE[1], step: 5, unit: T.min, onchange: (n) => {
      val = n; go.disabled = n == null; hint.hidden = n != null; hint.textContent = n == null ? V.minHint : '';
    } });
    show(1, backBtn(), title(T.minutesTitle), coach(V.minLead), field,
      h('div', { class: 'chips' }, [20, 30, 45, 60, 90].map(n => h('button', { class: 'chip', type: 'button', onclick: () => field.setValue(n) }, n + ' ' + T.min))),
      actions(hint, go));
  }
  // Places in scope: a gym, a home gym with real kit, or outdoors when running is part of the outcome.
  function where() {
    const ic = { gym: 't-gym', home_gym: 'i-home', outdoors: 't-runner' };
    const keys = Object.keys(ic).filter(k => k !== 'outdoors' || runs());
    const next = { gym: kit, home_gym: homeKit, outdoors };
    show(1, backBtn(), title(T.whereTitle),
      h('div', { class: 'tiles' }, keys.map(k => tile({ ic: ic[k], label: T.where[k], sub: T.whereSub[k], onclick: () => { A._where = k; step(next[k]); } })),
        decideTile(() => { A._where = 'gym'; step(kit); })));
  }
  function kit() {
    const opts = ['full_gym', 'basic_gym', 'crossfit_box'];
    const pick = (k) => { A.places = { main: { type: 'gym', equipment: [k] } }; A.default_place = 'main'; delete A.dumbbells; step(you); };
    show(1, backBtn(), title(T.kitTitle),
      h('div', { class: 'tiles one' }, opts.map(k => tile({ ic: KIT_IC[k], label: T.kit[k], sub: T.kitSub[k], onclick: () => pick(k) })),
        decideTile(() => pick(opts[0]))));
  }
  function homeKit() {
    const picked = new Set(A._homeKit || []);
    const hint = h('p', { class: 'hint', role: 'status' });
    const go = btn(T.cont, () => {
      A._homeKit = [...picked];
      A.places = { main: { type: 'home_gym', equipment: [...new Set([...picked].flatMap(k => HOME_KIT[k]))] } };
      A.default_place = 'main';
      if (!picked.has('dumbbell')) delete A.dumbbells;
      step(picked.has('dumbbell') ? dumbbells : you);
    }, 'primary', 'i-arrow-right');
    const refresh = () => { const ok = HOME_REAL.some(k => picked.has(k)); go.disabled = !ok; hint.textContent = ok ? '' : T.homeKitHint; hint.hidden = ok; };
    const cards = Object.keys(HOME_KIT).map(k => {
      const el = tile({ ic: HOME_IC[k], label: T.homeKit[k], tick: true, pressed: picked.has(k), onclick: () => {
        if (picked.has(k)) picked.delete(k); else picked.add(k);
        el.setAttribute('aria-pressed', String(picked.has(k))); refresh();
      } });
      return el;
    });
    refresh();
    show(1, backBtn(), title(T.homeKitTitle), coach(T.homeKitLead), h('div', { class: 'tiles one' }, cards), actions(hint, go));
  }
  function outdoors() {
    A.places = { main: { type: 'outdoors', equipment: ['outdoors'] } };
    A.default_place = 'main';
    delete A.dumbbells;
    step(you);
  }
  // the first weight they give: kilos or pounds, the guess preselected, confirmed right here
  const unitsRow = (redraw) => h('div', { class: 'line row2' }, h('span', { class: 'small' }, V.unitsQ),
    segOf([['kg', 'kg'], ['lb', 'lb']], UNITS, (u) => { setUnits(u); A.units = u; A.paper = PAPER; A.units_confirmed = true; if (redraw) redraw(); }));
  function dumbbells() {
    const box = h('div', { class: 'tiles one' });
    const draw = () => {
      const sets = UNITS === 'lb' ? DB_SETS_LB : DB_SETS;
      box.innerHTML = '';
      box.append(...Object.keys(sets).map(k => tile({ ic: 't-dumbbell', label: UNITS === 'lb' ? V.dbLb[k][0] : T.db[k], sub: UNITS === 'lb' ? V.dbLb[k][1] : T.dbSub[k],
        onclick: () => { A.dumbbells = sets[k]; A.units = UNITS; A.paper = PAPER; A.units_confirmed = true; step(you); } })));
    };
    draw();
    show(1, backBtn(), title(T.dbTitle), unitsRow(draw), box);
  }
  // you: skippable, but asked
  function you() {
    const good = new Set(A.strengths), holds = new Set(A.barriers), area = new Set(A.priority);
    let sleep = A.sleep || null, stress = A.stress || null;
    const hurt = new Map((A.limits || []).map(l => [l.region, { status: l.status || 'now', triggers: new Set(l.triggers || []) }]));
    const hurtBox = h('div', { class: 'group' });
    const drawHurt = () => {
      hurtBox.innerHTML = '';
      hurtBox.append(h('h2', {}, V.painQ), h('div', { class: 'chips' }, Object.entries(T.regions).map(([k, v]) => pressChip(v, hurt.has(k), () => {
        if (hurt.has(k)) hurt.delete(k); else hurt.set(k, { status: 'now', triggers: new Set() });
        drawHurt(); return hurt.has(k);
      }))));
      for (const [k, v] of hurt) {
        hurtBox.append(h('div', { class: 'card painrow' }, h('b', {}, icon('t-bandage'), ' ', T.regions[k]),
          h('div', { class: 'chips' }, Object.entries(V.status).map(([s, label]) => pressChip(label, v.status === s, () => { v.status = s; drawHurt(); return true; }))),
          h('p', { class: 'muted small' }, V.triggerQ), setChips(v.triggers, Object.entries(V.trigger))));
      }
    };
    drawHurt();
    const nums = Object.assign({}, A._nums || {});
    const numBox = h('div', { class: 'group' });
    const drawNums = () => {
      numBox.innerHTML = '';
      numBox.append(h('h2', {}, V.numbersQ), h('p', { class: 'muted small' }, V.numbersLead),
        h('div', { class: 'chips' }, NUM_LIFTS.map(id => pressChip(bankName(id), id in nums, () => {
          if (id in nums) delete nums[id]; else nums[id] = { w: UNITS === 'lb' ? 135 : 60, reps: 5 };
          drawNums(); return id in nums;
        }))));
      if (Object.keys(nums).length) numBox.append(unitsRow(() => {
        readNums();
        for (const n of Object.values(nums)) n.w = UNITS === 'lb' ? Math.round(n.w * 2.20462 / 5) * 5 : Math.round(n.w / 2.20462 / 2.5) * 2.5;
        drawNums();
      }));
      for (const [id, n] of Object.entries(nums)) {
        numBox.append(h('div', { class: 'exrow card' }, h('b', {}, bankName(id)),
          h('div', { class: 'line row2' }, h('span', { class: 'small' }, T.weight),
            stepper({ value: n.w, step: UNITS === 'lb' ? 5 : 2.5, min: 0, max: 500, unit: UNITS, onset: function () { } })),
          h('div', { class: 'line row2' }, h('span', { class: 'small' }, V.reps), stepper({ value: n.reps, step: 1, min: 1, max: 30 }))));
      }
    };
    drawNums();
    function readNums() {
      const rows = numBox.querySelectorAll('.exrow');
      Object.keys(nums).forEach((id, i) => {
        const st = rows[i].querySelectorAll('.stepper');
        nums[id] = { w: Number(st[0].querySelector('output').textContent.split(' ')[0]), reps: Number(st[1].querySelector('output').textContent) };
      });
    }
    show(1, backBtn(), title(V.youTitle), coach(V.youLead),
      h('div', { class: 'group' }, h('h2', {}, V.goodQ), setChips(good, Object.entries(V.good))),
      h('div', { class: 'group' }, h('h2', {}, V.holdQ), setChips(holds, Object.entries(V.hold), 2)),
      h('div', { class: 'group' }, h('h2', {}, T.areaQ), setChips(area, Object.entries(T.areas), 2)),
      hurtBox,
      h('div', { class: 'group' }, h('h2', {}, V.sleepQ), segOf(Object.entries(V.sleep), sleep, (x) => { sleep = x; })),
      h('div', { class: 'group' }, h('h2', {}, V.stressQ), segOf(Object.entries(V.stress), stress, (x) => { stress = x; })),
      numBox,
      actions(btn(T.cont, () => {
        readNums();
        A.strengths = [...good]; A.barriers = [...holds]; A.priority = [...area];
        A.limits = [...hurt].map(([region, v]) => ({ region, status: v.status, triggers: [...v.triggers], note: V.status[v.status] }));
        if (sleep) A.sleep = sleep; if (stress) A.stress = stress;
        A._nums = nums;
        A.numbers = Object.fromEntries(Object.entries(nums).map(([id, n]) => [id, { [UNITS]: n.w, reps: n.reps }]));
        if (Object.keys(nums).length) { A.units = UNITS; A.paper = PAPER; A.units_confirmed = true; }
        const goals = [mainGoal(), ...(A.outcomes || []).slice(1).map(o => OUTCOME_GOAL[o.id][o.detail])];
        const skill = goals.includes('run') || goals.includes('hyrox') || (A.outcome_detail === 'hybrid') ? 'run_30min'
          : goals[0] === 'weightlifting' ? 'olympic_coached' : null;
        if (skill) step(() => skillQ(skill)); else save();
      }, 'primary', 'i-arrow-right')));
  }
  function skillQ(skill) {
    const pick = (yes) => { A.skills = yes ? [skill] : []; save(); };
    show(1, backBtn(), title(T.skillQ[skill]),
      h('div', { class: 'tiles one' }, tile({ ic: 't-check', label: T.yes, onclick: () => pick(true) }), tile({ ic: 'i-close', label: T.no, onclick: () => pick(false) }),
        tile({ ic: 'i-spark', label: T.notSure, cls: 'decide', onclick: () => pick(false) })));
  }
  async function save() {
    busy(T.saving);
    const ans = {};
    for (const [k, v] of Object.entries(A)) if (!k.startsWith('_')) ans[k] = v;
    if (ans.mode !== 'improve') delete ans.current_routine;
    if (!experienced()) delete ans.style_pref;
    ans.rejected = [];
    let r;
    try { r = await run('profile', ['me/answers.json'], { 'answers.json': ans }); } catch (e) { return fail(); }
    if (!r.ok) {
      return show(1, title(T.errorsTitle), coach(...(r.errors || [r.error || '']).map(String)),
        actions(btn(T.back, back, 'primary', 't-back')));
    }
    yourPlan();
  }
  step(fork);
}

// ─────────────────────────────────────────────────────────────── your plan: one, decided by the trainer
async function yourPlan(extra) {
  busy(T.saving);
  let m;
  try { m = await run('match'); } catch (e) { return fail(); }
  window.__planTaps = window.__planTaps || TAPS;
  const V = T.iv;
  const prof = readProfile();
  const fb = m.fallback || {};
  const p = m.plan;
  const change = () => h('button', { class: 'back', type: 'button', onclick: () => interview() }, icon('t-back'), T.changeAnswers);
  if (!p) {
    return show(2, change(), h('h1', { class: 'title' }, V.planTitle), coach(T.nothingFits),
      actions(btn(T.changeAnswers, () => interview(), 'primary', 't-back')));
  }
  const info = programInfo(p.id);
  const d = (info.data.days || [prof.days, prof.days]);
  const days = Math.min(prof.days || d[0], d[1]);
  const mins = Math.max(info.data.express_minutes || 30, Math.min(prof.minutes || 45, (info.data.minutes || [45, 60])[1]));
  const notes = [];
  for (const k of ['outcome_note', 'style_note', 'improve_note', 'dose_note']) if (m[k]) notes.push(LANG === 'en' ? m[k] : (V.notes[k] || m[k]));
  if (fb.goal_note || m.goal_gap) notes.push(T.notServed);
  for (const o of (fb.one_change_away || []).slice(0, 1)) notes.push(V.oneChange(o.only_blocker));
  const whyLines = (LANG === 'en' ? String(p.why || '').split(' · ').filter(x => !/^evidence /.test(x)) : [T.fit[Math.min(3, p.goal_fit)]])
    .map(x => x.charAt(0).toUpperCase() + x.slice(1));
  const card = h('div', { class: 'card plan' },
    h('span', { class: 'badge' }, icon('i-star'), V.planBadge),
    h('h3', {}, V.family[p.family] || p.plain.headline),
    h('p', { class: 'muted small' }, V.familyLine[p.family] || p.plain.headline),
    h('div', { class: 'facts' },
      h('span', { class: 'fact' }, icon('i-calendar'), T.perWeek(days)),
      h('span', { class: 'fact' }, icon('i-clock'), V.about(mins)),
      p.split && V.shape[p.split] ? h('span', { class: 'fact' }, icon('t-mix'), V.shape[p.split]) : null,
      h('span', { class: 'fact' }, icon('i-badge-check'), T.evidence[p.evidence] || p.evidence)),
    h('div', { class: 'group' }, h('h2', {}, V.whyFits), h('ul', { class: 'why' }, whyLines.map(x => h('li', {}, x)))),
    h('details', { class: 'how' }, h('summary', {}, icon('i-info'), V.howItWorks),
      h('p', { class: 'small' }, V.howLine(p.name, (p.draws_from || []).filter(x => x !== p.name).slice(0, 3).join(', '))),
      LANG === 'en' && info.what ? h('p', { class: 'muted small' }, info.what) : null));
  show(2, change(), h('h1', { class: 'title' }, V.planTitle),
    coach(extra || V.planLead, ...notes.map(n => h('p', { class: 'muted small' }, n))), card,
    actions(btn(V.startPlan, () => choose(p.id), 'primary', 'i-arrow-right'), btn(V.notForMe, () => notForMe(p.id), '', 'i-close')));
}
function notForMe(pid) {
  const V = T.iv;
  const send = async (reason, more) => {
    busy(T.saving);
    const prof = readProfile();
    const ans = Object.assign({ rejected: (prof.rejected || []).concat([{ program: pid, reason }]) }, more || {});
    let r;
    try { r = await run('profile', ['me/answers.json'], { 'answers.json': ans }); } catch (e) { return fail(); }
    if (!r.ok) return show(2, coach(...(r.errors || [r.error || '']).map(String)), actions(btn(T.back, () => yourPlan(), 'primary', 't-back')));
    yourPlan(V.rethought);
  };
  const daysAgain = () => show(2, h('button', { class: 'back', type: 'button', onclick: () => notForMe(pid) }, icon('t-back'), T.back),
    h('h1', { class: 'title' }, T.daysTitle),
    h('div', { class: 'tiles' }, [2, 3, 4, 5, 6].map(n => tile({ ic: 'i-calendar', label: n + ' ' + T.daysUnit(n), onclick: () => send('days', { days: n }) }))));
  show(2, h('button', { class: 'back', type: 'button', onclick: () => yourPlan() }, icon('t-back'), T.back),
    h('h1', { class: 'title' }, V.whyNotTitle), coach(V.whyNotLead),
    h('div', { class: 'tiles one' },
      tile({ ic: 'i-clock', label: V.whyNot.too_long, onclick: () => send('too_long') }),
      tile({ ic: 't-runner', label: V.whyNot.too_much_running, onclick: () => send('too_much_running') }),
      tile({ ic: 't-face-flat', label: V.whyNot.not_enjoy, onclick: () => send('not_enjoy') }),
      tile({ ic: 'i-calendar', label: V.whyNot.days, onclick: daysAgain })));
}
async function programs() { return yourPlan(); }

function sayAlso(text) {
  if (!text || LANG === 'en') return text;
  const out = [];
  for (const [k, v] of Object.entries(T.sayAlso)) if (text.includes(k)) out.push(v);
  return out.length ? out.join(' ') : text;
}
async function choose(id) {
  busy(T.saving);
  let r;
  try { r = await run('choose', [id]); } catch (e) { return fail(); }
  if (!r.ok) return show(2, coach(r.error || T.engineFail), actions(btn(T.back, programs, 'primary', 't-back')));
  const info = programInfo(id);
  const name = T.iv.family[info.data.family] || info.data.name || id;
  const extra = [T.iv.expect];
  if (r.say_also) extra.push(sayAlso(r.say_also));
  show(2, h('button', { class: 'back', type: 'button', onclick: programs }, icon('t-back'), T.back),
    h('h1', { class: 'title' }, T.weekTitle),
    coach(T.weekLine(r.days, name), ...extra),
    actions(btn(T.firstNow, () => readiness(), 'primary', 't-sheet'), btn(T.later, () => route(), 'ghost')));
}

// ─────────────────────────────────────────────────────────────── today
async function readyHome(st) {
  let wk = null;
  try { wk = await run('week'); } catch (e) { }
  const so = wk && wk.planned ? h('div', { class: 'card' },
    h('p', { class: 'small' }, T.weekSoFar(wk.done_this_week || 0, wk.planned)),
    h('div', { class: 'bar', style: 'margin-top:10px' }, h('span', { style: 'width:' + Math.min(100, 100 * (wk.done_this_week || 0) / wk.planned) + '%' }))) : null;
  show(3, h('h1', { class: 'title' }, T.readyTitle), coach(T.readyLead(st.next_session || st.program_name)), so,
    actions(btn(T.todaySession, () => readiness(), 'primary', 't-sheet'), btn(T.myWeek, weekView, '', 'i-calendar')));
}

function readiness() {
  const prof = readProfile();
  const usual = prof.minutes || 45;
  const R = { pain: [] };
  const hist = [];
  const goBack = () => { hist.pop(); const f = hist.pop(); f ? f() : route(); };
  const backBtn = () => h('button', { class: 'back', type: 'button', onclick: goBack }, icon('t-back'), T.back);
  const q = (title, opts, onPick, extra) => show(3, backBtn(), h('h1', { class: 'title' }, title), extra || null,
    h('div', { class: 'tiles one' }, opts.map(o => tile({ ic: o.ic, label: o.label, sub: o.sub, onclick: () => onPick(o.v) }))));
  const energy = () => { hist.push(energy); q(T.energyTitle, [
    { v: 9, ic: 't-bat-full', label: T.energy[9][0], sub: T.energy[9][1] },
    { v: 7, ic: 't-bat-mid', label: T.energy[7][0], sub: T.energy[7][1] },
    { v: 5, ic: 't-bat-low', label: T.energy[5][0], sub: T.energy[5][1] },
    { v: 3, ic: 't-bat-empty', label: T.energy[3][0], sub: T.energy[3][1] }], (v) => { R.energy = v; pain(); }); };
  const pain = () => { hist.push(pain); q(T.painTitle, [
    { v: 'none', ic: 't-check', label: T.pain.none },
    { v: 'little', ic: 't-bandage', label: T.pain.little, sub: T.painSub.little },
    { v: 'sharp', ic: 't-bandage', label: T.pain.sharp }], (v) => { R.pain = []; if (v === 'none') return time(); region(v === 'sharp' ? 6 : 2); }); };
  const region = (score) => {
    hist.push(() => region(score));
    const sel = new Set();
    const go = btn(T.cont, () => { R.pain = [...sel].map(r => Object.assign({ region: r, score }, score > 3 ? { sharp: true } : {})); time(); }, 'primary', 'i-arrow-right');
    go.disabled = true;
    show(3, backBtn(), h('h1', { class: 'title' }, T.whereHurt), h('div', { class: 'chips' }, Object.entries(T.regions).map(([k, v]) => {
      const c = h('button', { class: 'chip', type: 'button', 'aria-pressed': 'false', onclick: () => {
        if (sel.has(k)) sel.delete(k); else sel.add(k); c.setAttribute('aria-pressed', String(sel.has(k))); go.disabled = !sel.size;
      } }, icon('t-bandage'), v);
      return c;
    })), actions(go));
  };
  const time = () => { hist.push(time); q(T.timeTitle, [
    { v: usual, ic: 'i-clock', label: T.usual, sub: usual + ' ' + T.min },
    ...[30, 45, 60].filter(n => n !== usual).map(n => ({ v: n, ic: 't-timer', label: n + ' ' + T.min }))], (v) => { R.minutes = v; unusual(); }); };
  const unusual = () => { hist.push(unusual); q(T.unusualTitle, [
    { v: 'no', ic: 't-check', label: T.unusual.no },
    { v: 'slept', ic: 't-moon', label: T.unusual.slept },
    { v: 'cardio', ic: 't-runner', label: T.unusual.cardio },
    { v: 'ill', ic: 't-thermo', label: T.unusual.ill },
    { v: 'kit', ic: 'i-map-pin', label: T.unusual.kit }], (v) => {
      const out = Object.assign({}, R);
      if (v === 'slept') out.energy = Math.max(1, R.energy - 1);
      if (v === 'cardio') out.hard_cardio_24h = true;
      if (v === 'ill') out.ill = true;
      if (v === 'kit') return kitToday();
      build(out);
    }); };
  const kitToday = () => { hist.push(kitToday); q(T.kitToday, ['full_gym', 'basic_gym', 'crossfit_box', 'home_dumbbells', 'outdoors'].map(k => ({ v: k, ic: KIT_IC[k], label: T.kit[k] })),
    (k) => { build(Object.assign({}, R, { equipment: [k] })); }); };
  energy();
}

async function build(today) {
  busy(T.building);
  let b;
  try { b = await run('build', ['me/today.json'], { 'today.json': today }); } catch (e) { return fail(); }
  if (!b.ok) return show(3, coach(b.error || T.engineFail), actions(btn(T.tryAgain, route, 'primary', 't-reset')));
  if (b.rest_day) {
    const ill = !!today.ill;
    return show(3, h('h1', { class: 'title' }, T.restTitle), coach(ill ? T.restIll : T.restLow),
      actions(ill ? null : btn(T.easySheet, () => render(b.session, true), 'primary', 't-sheet'), btn(T.done, route, ill ? 'primary' : 'ghost')));
  }
  render(b.session);
}

async function render(session, rest) {
  busy(T.rendering);
  let r;
  try { r = await run('render', [session]); } catch (e) { return fail(); }
  if (!r.ok) {
    return show(3, coach(T.tooLong), actions(btn(T.tryAgain, async () => { try { await run('discard'); } catch (e) { } readiness(); }, 'primary', 't-reset')));
  }
  sheet(session, r.pdf, rest);
}

function sheetFrame(session) {
  // the sheet is laid out as a page (560 px wide) and scaled to fit the phone, never squashed
  const W = 560;
  const html = fsRead(session.replace(/\.json$/, '.html'), true) || '';
  const f = h('iframe', { class: 'sheetframe', title: 'sheet', srcdoc: html, scrolling: 'no' });
  const wrap = h('div', { class: 'sheetwrap' }, f);
  let zoom = false;
  const fit = () => {
    try {
      const d = f.contentDocument; if (!d || !d.body) return;
      const scale = zoom ? 1 : Math.min(1, wrap.clientWidth / W);
      const ht = Math.max(d.documentElement.scrollHeight, d.body.scrollHeight);
      f.style.width = W + 'px'; f.style.height = ht + 'px';
      f.style.transform = 'scale(' + scale + ')';
      wrap.style.height = Math.ceil(ht * scale) + 'px';
    } catch (e) { wrap.style.height = '900px'; }
  };
  f.addEventListener('load', () => { fit(); setTimeout(fit, 300); });
  window.addEventListener('resize', fit);
  const label = h('span', {}, T.zoomIn);
  const zb = h('button', { class: 'btn ghost', type: 'button', onclick: () => {
    zoom = !zoom; wrap.classList.toggle('zoom', zoom); label.textContent = zoom ? T.zoomOut : T.zoomIn; fit();
  } }, icon('i-plus'), label);
  return h('div', { class: 'group' }, zb, wrap);
}
function pdfName(session) {
  const base = session.split('/').pop().replace(/\.json$/, '').replace(/[·]/g, '').replace(/\s+/g, ' ').trim();
  return base + '.pdf';
}
function sheet(session, pdf, rest) {
  let s = {};
  try { s = JSON.parse(fsRead(session, true)); } catch (e) { }
  const first = (s.blocks || []).some(b => b.items.some(i => i.first_outing));
  const note = h('p', { class: 'muted small', role: 'status' });
  const after = h('div', { class: 'card nextstep', role: 'status', hidden: true });
  const name = pdfName(session);
  const nextBtn = rest ? btn(T.done, route, 'ghost') : btn(T.trained, () => howItWent(session), 'ghost', 't-check');
  const saveBtn = btn(T.savePdf, async () => {
    const bytes = fsRead(pdf);
    if (!bytes) { note.textContent = T.pdfFail; return; }
    const r = await saveFile(name, new Blob([bytes], { type: 'application/pdf' }), 'application/pdf');
    if (r !== 'saved') { note.textContent = r === 'declined' ? T.pdfDeclined : T.pdfFail; return; }
    note.textContent = '';
    after.innerHTML = '';
    after.append(h('p', { class: 'kicker' }, icon('t-check'), T.pdfSaved),
      h('p', {}, T.pdfWhere(''), h('code', {}, name)),
      h('p', { class: 'muted small' }, T.pdfWhereLine),
      h('ol', {}, T.pdfNext.map(x => h('li', {}, x))),
      h('p', { class: 'muted small' }, T.pdfNoFile));
    after.hidden = false;
    // the main action moves on: log it once you have trained; saving again stays one tap away
    saveBtn.className = 'btn ghost'; nextBtn.className = 'btn primary';
    after.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }, 'primary', 'i-download');
  window.__firstSheetAt = window.__firstSheetAt || performance.now();
  window.__firstSheetTaps = window.__firstSheetTaps || TAPS;
  show(4, h('h1', { class: 'title' }, T.sheetTitle),
    coach(h('p', {}, h('b', {}, s.title || '')),
      s.score_to_beat ? h('p', { class: 'small' }, h('span', { class: 'hot' }, T.toBeat), s.score_to_beat) : null,
      first ? h('p', { class: 'muted small' }, T.firstTime) : null,
      rest ? null : h('p', { class: 'small' }, T.sheetLead)),
    after,
    sheetFrame(session),
    rest ? null : flowActions(btn(T.myWeek, weekView, 'ghost', 'i-calendar')),
    actions(note, saveBtn, nextBtn));
}

// ─────────────────────────────────────────────────────────────── how did it go
const NO_LOAD = new Set(['bodyweight', 'band', 'time', 'distance', 'calories']);
function slots(s) {
  const out = [];
  for (const b of s.blocks || []) for (const it of b.items) if (it._slot && !it._slot.travel) out.push(it);
  return out;
}
function howItWent(session) {
  let s = {};
  try { s = JSON.parse(fsRead(session, true)); } catch (e) { }
  show(4, h('h1', { class: 'title' }, T.howTitle(s.title)), coach(h('p', {}, h('b', {}, s.title || ''))),
    h('div', { class: 'tiles one' },
      tile({ ic: 't-check', label: T.howAll, cls: 'big', onclick: () => logIt(session, s, { as_written: true }) }),
      tile({ ic: 'i-chat', label: T.howSome, cls: 'big', onclick: () => changes(session, s) }),
      tile({ ic: 'i-close', label: T.howNot, cls: 'big', onclick: () => logIt(session, s, null) })),
    actions(btn(T.seeSheet, () => sheet(session, session.replace(/\.json$/, '.pdf')), 'ghost', 't-sheet')));
}

function stepper({ value, step, min, max, unit, unset, onset }) {
  let v = value, touched = false;
  const out = h('output', { class: unset ? 'unset' : '' }, unset ? '?' : fmt(v));
  function fmt(x) { return (Math.round(x * 100) / 100) + (unit ? ' ' + unit : ''); }
  const set = (nv) => { v = Math.max(min, Math.min(max, nv)); touched = true; out.textContent = fmt(v); out.className = ''; if (onset) onset(); };
  const el = h('div', { class: 'stepper' },
    h('button', { type: 'button', 'aria-label': T.less, onclick: () => set((unset && !touched) ? v : v - step) }, icon('t-minus')),
    out,
    h('button', { type: 'button', 'aria-label': T.more, onclick: () => set((unset && !touched) ? v : v + step) }, icon('i-plus')));
  el.get = () => v; el.touched = () => touched; el.set = set;
  return el;
}
const repRange = (r) => { const m = String(r || '').match(/\d+/g); return m ? m.map(Number) : []; };
const kgToUnits = (kg) => UNITS === 'lb' ? Math.round(kg * 2.20462 / 5) * 5 : kg;
function guessLoad(sl) {
  const lt = sl.load_type;
  const kg = lt === 'barbell' ? 20 : lt === 'kettlebell' ? 12 : lt === 'dumbbell' ? 8 : 20;
  return kgToUnits(kg);
}

function changes(session, s, needs) {
  const items = slots(s);
  const needKeys = new Set((needs || []).map(n => n.key));
  const rows = {};
  const step = UNITS === 'lb' ? 5 : 2.5;
  const cards = items.filter(it => !needs || needKeys.has(it._slot.key)).map(it => {
    const sl = it._slot, p = sl.prescribed || {};
    const loaded = !NO_LOAD.has(sl.load_type);
    const rr = repRange(p.reps || it.reps);
    const timed = sl.load_type === 'time';
    const st = { skipped: false };
    const wHint = p.load == null ? h('small', { class: 'muted', style: 'display:block;font-size:13px' }, T.tapToSet) : null;
    const weight = loaded ? stepper({ value: p.load != null ? kgToUnits(p.load) : guessLoad(sl), step, min: 0, max: 500, unit: UNITS, unset: p.load == null, onset: () => { if (wHint) wHint.remove(); } }) : null;
    const reps = !timed && rr.length && !String(p.reps || it.reps).includes('min') ? stepper({ value: rr[rr.length - 1], step: 1, min: 0, max: 100 }) : null;
    const mins = timed && rr.length ? stepper({ value: rr[0], step: 5, min: 0, max: 240, unit: T.min }) : null;
    const card = h('div', { class: 'card exrow' });
    const seg = h('div', { class: 'seg' },
      h('button', { type: 'button', 'aria-pressed': 'true', onclick: (e) => { st.skipped = false; mark2(); } }, T.didIt),
      h('button', { type: 'button', 'aria-pressed': 'false', onclick: (e) => { st.skipped = true; mark2(); } }, T.skipped));
    function mark2() {
      seg.children[0].setAttribute('aria-pressed', String(!st.skipped)); seg.children[1].setAttribute('aria-pressed', String(st.skipped));
      card.classList.toggle('skipped', st.skipped);
    }
    card.append(h('div', { class: 'head' }, h('div', {}, h('b', {}, it.name), h('p', { class: 'muted small num' }, [it.sets ? it.sets + ' x ' : '', it.reps || '', it.load ? ' · ' + it.load : ''].join(''))), needs ? null : seg));
    if (weight) card.append(h('div', { class: 'line k' }, h('span', {}, T.weight, wHint), weight));
    if (reps && !needs) card.append(h('div', { class: 'line k' }, h('span', {}, T.repsEach), reps));
    if (mins && !needs) card.append(h('div', { class: 'line k' }, h('span', {}, T.minutes), mins));
    rows[sl.key] = { st, weight, reps, mins, sets: it.sets || p.sets || 1, first: !!it.first_outing, set: mark2 };
    return card;
  });
  // felt and pain
  let felt = null;
  const feltIc = { great: 't-face-great', good: 't-face-ok', hard: 't-face-hard', flat: 't-face-flat' };
  const feltRow = h('div', { class: 'tiles' }, Object.keys(feltIc).map(k => {
    const el = tile({ ic: feltIc[k], label: T.felt[k], pressed: false, onclick: () => { felt = k; feltRow.querySelectorAll('.tile').forEach(x => x.setAttribute('aria-pressed', String(x === el))); } });
    return el;
  }));
  const pain = new Map();
  const painBox = h('div', { class: 'group' });
  const drawPain = () => {
    painBox.innerHTML = '';
    painBox.append(h('h2', {}, T.hurtQ2), h('div', { class: 'chips' }, Object.entries(T.regions).map(([k, v]) => {
      const c = h('button', { class: 'chip', type: 'button', 'aria-pressed': String(pain.has(k)), onclick: () => { if (pain.has(k)) pain.delete(k); else pain.set(k, 2); drawPain(); } }, v);
      return c;
    })));
    for (const [k, v] of pain) painBox.append(h('div', { style: 'display:flex;justify-content:space-between;align-items:center;gap:10px' }, h('span', {}, icon('t-bandage'), ' ', T.regions[k]),
      h('div', { class: 'seg' },
        h('button', { type: 'button', 'aria-pressed': String(v <= 3), onclick: () => { pain.set(k, 2); drawPain(); } }, T.mild),
        h('button', { type: 'button', 'aria-pressed': String(v > 3), onclick: () => { pain.set(k, 6); drawPain(); } }, T.sharpW))));
  };
  drawPain();
  // words, read by Claude on the viewer's click only
  const words = h('textarea', { placeholder: T.wordsPh, 'aria-label': T.wordsQ });
  const wordsNote = h('p', { class: 'muted small', role: 'status' });
  const readBtn = btn(T.readWords, async () => {
    if (!CAP.sample) { wordsNote.textContent = T.readNo; return; }
    const text = words.value.trim(); if (!text) return;
    readBtn.disabled = true; wordsNote.textContent = T.reading;
    const list = items.map(it => '- ' + it._slot.key + ': ' + it.name + ', ' + (it.sets || 1) + ' x ' + (it.reps || '') + (it.load ? ', ' + it.load : '')).join('\n');
    const prompt = 'You turn what a person said about their workout into log fields. Their session (key: exercise, sets x reps, weight):\n' + list +
      '\n\nWhat they said, in their words:\n"""' + text.slice(0, 2000) + '"""\n\n' +
      'Reply with only JSON of this shape, and include only what they actually mentioned:\n' +
      '{"results": {"<key>": {"load": <number in ' + UNITS + '>, "reps": [<reps of each set>]}}, "skipped": ["<key>"], ' +
      '"pain": [{"region": "knee|hip|low_back|shoulder|elbow|wrist|ankle|neck", "score": <0 to 10>}], "felt": "great|good|hard|flat|null"}\n' +
      'Use only the keys listed above. Example: {"results": {"squat": {"reps": [5,5,4]}}, "skipped": ["curl"], "pain": [], "felt": "hard"}';
    try {
      const d = await CAP.sample.json(prompt, { modelTier: 'quick' });
      applyWords(d || {});
      wordsNote.textContent = T.readDone;
    } catch (e) { wordsNote.textContent = (e && e.code === 'not_granted') ? T.readNo : T.readFail; }
    readBtn.disabled = false;
  }, '', 'i-chat');
  function applyWords(d) {
    for (const [k, r] of Object.entries(d.results || {})) {
      const row = rows[k]; if (!row || !r) continue;
      if (r.load != null && row.weight && !isNaN(+r.load)) row.weight.set(+r.load);
      if (Array.isArray(r.reps) && r.reps.length && row.reps) { row.reps.set(Math.min(...r.reps.map(Number))); row.repsList = r.reps.map(Number); }
    }
    for (const k of d.skipped || []) if (rows[k]) { rows[k].st.skipped = true; rows[k].set(); }
    for (const p of d.pain || []) if (p && T.regions[p.region]) pain.set(p.region, +p.score > 3 ? 6 : 2);
    drawPain();
    if (d.felt && feltIc[d.felt]) feltRow.querySelectorAll('.tile')[Object.keys(feltIc).indexOf(d.felt)].click();
  }
  const save = btn(T.saveLog, () => {
    const results = {}, skipped = [];
    for (const [k, r] of Object.entries(rows)) {
      if (r.st.skipped) { skipped.push(k); continue; }
      const o = {};
      if (r.weight && r.weight.touched()) o.load = r.weight.get();
      if (r.repsList) o.reps = r.repsList;
      else if (r.reps && r.reps.touched()) o.reps = Array(Number(r.sets) || 1).fill(r.reps.get());
      if (r.mins && r.mins.touched()) o.minutes = r.mins.get();
      if (Object.keys(o).length) results[k] = o;
    }
    const base = needs ? needs.report : { as_written: true };
    const merged = Object.assign({}, base.results || {});
    for (const [k, o] of Object.entries(results)) merged[k] = Object.assign({}, merged[k] || {}, o);
    const report = Object.assign({}, base, { results: merged });
    if (!needs) {
      report.skipped = skipped;
      report.pain = [...pain].map(([region, score]) => ({ region, score }));
      if (felt) report.felt = felt;
      if (words.value.trim()) report.notes = words.value.trim().slice(0, 500);
    }
    logIt(session, s, report);
  }, 'primary', 't-check');
  if (needs) {
    const req = needs.filter(n => !n.optional).map(n => rows[n.key]).filter(Boolean);
    const hint = h('p', { class: 'hint', role: 'status' }, T.needsHint);
    const check = () => { save.disabled = req.some(r => !r.weight || !r.weight.touched()); hint.hidden = !save.disabled; };
    check();
    setTimeout(() => document.getElementById('app').addEventListener('click', () => setTimeout(check, 0)), 0);
    return show(4, h('button', { class: 'back', type: 'button', onclick: () => howItWent(session) }, icon('t-back'), T.back),
      h('h1', { class: 'title' }, T.needsTitle), coach(T.needsLead, needs.optional && needs.optional.length ? h('p', { class: 'muted small' }, T.optionalLine) : null), ...cards, actions(hint, save));
  }
  show(4, h('button', { class: 'back', type: 'button', onclick: () => howItWent(session) }, icon('t-back'), T.back),
    h('h1', { class: 'title' }, T.changesTitle), coach(T.changesLead), ...cards,
    h('div', { class: 'group' }, h('h2', {}, T.feltQ), feltRow),
    painBox,
    h('div', { class: 'group' }, h('h2', {}, T.wordsQ), words, CAP.sample ? readBtn : null, wordsNote),
    actions(save));
}

function nextLoad(line) {
  if (LANG !== 'fr') return line;
  return line.replace(/: next time /, ' : la prochaine fois ').replace(/: training max /, ' : max d’entraînement ').replace(/, wave /, ', vague ');
}
async function logIt(session, s, report) {
  busy(T.saving);
  let r;
  const before = records();
  try { r = report ? await run('log', ['me/report.json'], { 'report.json': report }) : await run('log', ['unreported']); }
  catch (e) { return fail(); }
  if (!r.ok && r.needs) {
    const items = slots(s);
    const opt = items.filter(it => (r.optional || []).includes(it.name)).map(it => ({ key: it._slot.key, name: it.name, optional: true }));
    return changes(session, s, Object.assign([...r.needs, ...opt], { report, optional: r.optional }));
  }
  if (!r.ok) return show(4, coach(r.error || T.engineFail), actions(btn(T.done, route, 'primary')));
  const lines = [];
  if (!report) lines.push(T.noProblem);
  if ((r.not_in_session || []).length) lines.push(T.notInSession);
  const ev = r.events || [];
  if (ev.includes('week_closed')) lines.push(T.weekClosed);
  if (ev.includes('block_closed')) lines.push(T.blockClosed);
  if (ev.includes('early_deload')) lines.push(T.deload);
  if (report && !ev.includes('early_deload')) lines.push(T.loggedNext);
  const fresh = r.ok ? freshRecords(before, records()) : [];
  show(4, h('h1', { class: 'title' }, T.loggedTitle),
    fresh.length ? recordsCard(fresh, fresh) : null,
    coach(r.score ? h('p', {}, h('b', {}, s.title || ''), ' · ', h('span', { class: 'num' }, scoreText(r.score))) : h('p', {}, h('b', {}, s.title || '')), ...lines),
    (r.next_loads || []).length ? h('div', { class: 'card' }, h('p', { class: 'kicker' }, icon('i-trend-up'), ' ', T.nextTime),
      h('div', { class: 'list' }, r.next_loads.slice(0, 6).map(l => h('div', { class: 'row num' }, nextLoad(l))))) : null,
    actions(btn(T.home, route, 'primary', 't-check'), btn(T.myWeek, weekView, '', 'i-calendar')));
}

// ─────────────────────────────────────────────────────────────── the week
async function weekView() {
  busy(T.saving);
  let w;
  try { w = await run('week'); } catch (e) { return fail(); }
  const done = w.done_this_week || 0, planned = w.planned || 0;
  const sets = Object.entries(w.hard_sets_7d || {});
  const maxv = Math.max(20, ...sets.map(([, v]) => v.done));
  show(3, h('button', { class: 'back', type: 'button', onclick: route }, icon('t-back'), T.back),
    h('h1', { class: 'title' }, T.weekViewTitle),
    h('div', { class: 'card' },
      h('div', { class: 'stat' }, h('span', { class: 'n' }, done), h('span', { class: 'muted' }, '/ ' + planned)),
      h('p', { class: 'muted small' }, T.doneOf(done, planned)),
      h('div', { class: 'bar', style: 'margin-top:10px' }, h('span', { style: 'width:' + (planned ? Math.min(100, 100 * done / planned) : 0) + '%' }))),
    streakCard(),
    recordsCard(records()),
    h('div', { class: 'card' }, h('p', { class: 'kicker' }, T.last7),
      (w.last_7_days || []).length ? h('div', { class: 'list' }, w.last_7_days.map(l => h('div', { class: 'row' }, h('span', {}, h('b', {}, l.title || ''), h('br'), h('span', { class: 'muted small num' }, l.date)), h('span', { class: 'num small' }, scoreText(l.score)))))
        : h('p', { class: 'muted small', style: 'margin:8px 0 0' }, T.nothingYet)),
    sets.length ? h('div', { class: 'card group' }, h('p', { class: 'kicker' }, T.hardSets),
      sets.map(([g, v]) => {
        const band = v.usual_range || [0, 0];
        return h('div', { class: 'mbar' }, h('span', {}, T.muscles[g] || g),
          h('div', { class: 'track' },
            h('span', { class: 'band', style: 'left:' + (100 * band[0] / maxv) + '%;width:' + (100 * (band[1] - band[0]) / maxv) + '%' }),
            h('span', { class: 'fill', style: 'width:' + Math.min(100, 100 * v.done / maxv) + '%' })),
          h('span', { class: 'num', style: 'text-align:right' }, v.done));
      }), h('p', { class: 'muted small' }, T.usualBand)) : null,
    actions(btn(T.todaySession, () => readiness(), 'primary', 't-sheet')));
}

// ─────────────────────────────────────────────────────────────── settings
function b64(bytes) {
  let s = '';
  for (let i = 0; i < bytes.length; i += 0x8000) s += String.fromCharCode.apply(null, bytes.subarray(i, i + 0x8000));
  return btoa(s);
}
function unb64(str) {
  const s = atob(str), out = new Uint8Array(s.length);
  for (let i = 0; i < s.length; i++) out[i] = s.charCodeAt(i);
  return out;
}
function settings() {
  if (!PY) return;
  const note = h('p', { class: 'muted small', role: 'status' }, DB.ok ? '' : T.noStorage);
  const file = h('input', { type: 'file', accept: '.json,application/json', class: 'hidden' });
  file.addEventListener('change', async () => {
    const f = file.files && file.files[0]; if (!f) return;
    try {
      const data = JSON.parse(await f.text());
      if (!data || data.app !== 'personal-trainer' || !data.files) throw new Error('bad');
      clearData();
      for (const [rel, v] of Object.entries(data.files)) if (/^(me|sessions)\//.test(rel) && !rel.includes('..')) fsWrite(rel, unb64(v));
      await persist();
      note.textContent = T.restored;
      setTimeout(route, 600);
    } catch (e) { note.textContent = T.restoreBad; }
  });
  const theme = pref.get('theme') || 'auto';
  const themeSeg = h('div', { class: 'seg' }, Object.entries(T.themes).map(([k, v]) => h('button', { type: 'button', 'aria-pressed': String(theme === k), onclick: () => {
    pref.set('theme', k);
    if (k === 'auto') delete document.documentElement.dataset.theme; else document.documentElement.dataset.theme = k;
    settings();
  } }, v)));
  show(-1, h('button', { class: 'back', type: 'button', onclick: route }, icon('t-back'), T.close),
    h('h1', { class: 'title' }, T.setTitle),
    h('div', { class: 'tiles one' },
      tile({ ic: 'i-download', label: T.backup, sub: T.backupSub, onclick: async () => {
        const files = {}; for (const [k, v] of Object.entries(snapshot())) files[k] = b64(v);
        const r = await saveFile('personal-trainer-' + new Date().toISOString().slice(0, 10) + '.json',
          JSON.stringify({ app: 'personal-trainer', version: BUNDLE.version, saved: new Date().toISOString(), files }), 'application/json');
        note.textContent = r === 'saved' ? T.pdfSaved : r === 'declined' ? T.pdfDeclined : T.pdfFail;
      } }),
      tile({ ic: 't-upload', label: T.restore, sub: T.restoreSub, onclick: () => file.click() }),
      tile({ ic: 't-reset', label: T.startOver, sub: T.startOverSub, onclick: startOver })),
    h('div', { class: 'group' }, h('h2', {}, T.theme), themeSeg),
    file, note);
}
function startOver() {
  show(-1, h('h1', { class: 'title' }, T.startOverQ), coach(T.startOverLead),
    actions(btn(T.keep, settings, 'primary'), btn(T.erase, async () => {
      busy(T.saving);
      try { await run('forget', ['yes']); } catch (e) { }
      clearData();
      await persist();
      welcome();
    }, 'danger', 't-reset')));
}

boot();
