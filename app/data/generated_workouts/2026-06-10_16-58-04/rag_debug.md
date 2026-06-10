# RAG Debug Report

## Retrieval Query

```text
User goal: muscle gain
Experience level: beginner-intermediate
Available equipment today: ['dumbbells', 'pull-up bar']
Time available: 45 minutes
Energy level: medium
Soreness: ['quads', 'glutes']
Recent workouts: [{'id': 'workout-008', 'user_id': 'demo-user-001', 'date': '2026-06-03', 'workout_type': 'upper body push', 'duration_minutes': 55, 'energy_before': 'medium', 'difficulty': 7, 'completed': True, 'exercises': [{'name': 'Incline dumbbell bench press', 'category': 'upper body push', 'primary_muscles': ['chest', 'shoulders', 'triceps'], 'equipment': 'dumbbells and incline bench', 'sets': [{'set': 1, 'reps': 10, 'weight_kg_per_hand': 15}, {'set': 2, 'reps': 8, 'weight_kg_per_hand': 17.5}, {'set': 3, 'reps': 7, 'weight_kg_per_hand': 17.5}, {'set': 4, 'reps': 10, 'weight_kg_per_hand': 15}]}, {'name': 'Cable triceps pressdown', 'category': 'arms', 'primary_muscles': ['triceps'], 'equipment': 'cable machine', 'sets': [{'set': 1, 'reps': 12, 'weight_kg': 20}, {'set': 2, 'reps': 12, 'weight_kg': 20}, {'set': 3, 'reps': 10, 'weight_kg': 25}]}, {'name': 'Plank', 'category': 'core', 'primary_muscles': ['core'], 'equipment': 'mat', 'sets': [{'set': 1, 'duration_seconds': 50}, {'set': 2, 'duration_seconds': 45}]}], 'soreness_after': ['chest', 'triceps'], 'notes': 'Push session was solid. Incline dumbbell bench still strongest around 17.5 kg per hand for 7-8 reps.'}, {'id': 'workout-009', 'user_id': 'demo-user-001', 'date': '2026-06-05', 'workout_type': 'lower body posterior chain', 'duration_minutes': 65, 'energy_before': 'medium', 'difficulty': 8, 'completed': True, 'exercises': [{'name': 'Smith machine Romanian deadlift', 'category': 'lower body', 'primary_muscles': ['hamstrings', 'glutes', 'lower back'], 'equipment': 'smith machine', 'sets': [{'set': 1, 'reps': 10, 'weight_kg': 40}, {'set': 2, 'reps': 10, 'weight_kg': 45}, {'set': 3, 'reps': 9, 'weight_kg': 45}, {'set': 4, 'reps': 8, 'weight_kg': 45}]}, {'name': 'Hip thrust', 'category': 'lower body', 'primary_muscles': ['glutes', 'hamstrings'], 'equipment': 'barbell or hip thrust machine', 'sets': [{'set': 1, 'reps': 12, 'weight_kg': 70}, {'set': 2, 'reps': 10, 'weight_kg': 80}, {'set': 3, 'reps': 8, 'weight_kg': 90}]}, {'name': 'Plank', 'category': 'core', 'primary_muscles': ['core'], 'equipment': 'mat', 'sets': [{'set': 1, 'duration_seconds': 55}, {'set': 2, 'duration_seconds': 45}, {'set': 3, 'duration_seconds': 40}]}], 'soreness_after': ['hamstrings', 'glutes'], 'notes': 'Posterior chain was the focus. Romanian deadlift at 45 kg is becoming consistent.'}, {'id': 'workout-010', 'user_id': 'demo-user-001', 'date': '2026-06-07', 'workout_type': 'upper body pull', 'duration_minutes': 60, 'energy_before': 'medium', 'difficulty': 7, 'completed': True, 'exercises': [{'name': 'Assisted pull-up', 'category': 'upper body pull', 'primary_muscles': ['lats', 'upper back', 'biceps'], 'equipment': 'gravitron assisted pull-up machine', 'sets': [{'set': 1, 'reps': 8, 'assistance_kg': 15}, {'set': 2, 'reps': 8, 'assistance_kg': 15}, {'set': 3, 'reps': 9, 'assistance_kg': 25}, {'set': 4, 'reps': 8, 'assistance_kg': 25}], 'note': 'Good session. 15 kg assistance was manageable for two sets.'}, {'name': 'Front lat pulldown', 'category': 'upper body pull', 'primary_muscles': ['lats', 'upper back', 'biceps'], 'equipment': 'lat pulldown machine', 'sets': [{'set': 1, 'reps': 12, 'weight_kg': 35}, {'set': 2, 'reps': 10, 'weight_kg': 40}, {'set': 3, 'reps': 8, 'weight_kg': 45}]}, {'name': 'Bicep curl', 'category': 'arms', 'primary_muscles': ['biceps'], 'equipment': 'dumbbells', 'sets': [{'set': 1, 'reps': 12, 'weight_kg_per_hand': 10}, {'set': 2, 'reps': 10, 'weight_kg_per_hand': 10}, {'set': 3, 'reps': 10, 'weight_kg_per_hand': 10}]}, {'name': 'Plank', 'category': 'core', 'primary_muscles': ['core'], 'equipment': 'mat', 'sets': [{'set': 1, 'duration_seconds': 60}, {'set': 2, 'duration_seconds': 45}]}], 'soreness_after': ['lats', 'biceps'], 'notes': 'Upper pull session went well. Assisted pull-ups are improving, especially on the gravitron.'}]

Find relevant workout programming rules, recovery guidance,
exercise options, warmup/cooldown advice, and substitutions.
```

## Retrieved Chunks

### Chunk 1

- **Source:** `06_exercise_subtitutions.md`
- **Similarity score:** `0.7569`

```markdown
# Exercise substitutions

If the user cannot do pull-ups, use band-assisted pull-ups, negative pull-ups, inverted rows, or one-arm dumbbell rows.

If the user cannot do push-ups, use incline push-ups, knee push-ups, or dumbbell floor press.

If the user cannot squat comfortably, use box squats, goblet squats with reduced range, or glute bridges.

If the user has no bench, replace dumbbell bench press with dumbbell floor press.

If the user has no dumbbells, use bodyweight exercises or resistance bands.
```

### Chunk 2

- **Source:** `01_recovery_rules.md`
- **Similarity score:** `0.7543`

```markdown
# Recovery rules

If the user reports strong soreness in a muscle group, avoid high-volume or high-intensity training for that muscle group today.

If the user slept poorly or reports low energy, reduce total workout volume by about 20-30%.

Avoid training the same muscle group intensely on consecutive days.

If the user reports pain rather than normal soreness, recommend stopping the painful movement and choosing a safer alternative.

For a showcase app, always include a short safety note: stop if sharp pain, dizziness, or unusual discomfort occurs.
```

### Chunk 3

- **Source:** `02_training_goals.md`
- **Similarity score:** `0.7350`

```markdown
# Training goals

For general fitness, use a balanced mix of strength, mobility, and light conditioning.

For muscle gain, prioritize resistance exercises, moderate-to-high volume, controlled technique, and progressive overload.

For strength, prioritize compound movements, lower rep ranges, longer rest, and gradual load progression.

For fat loss, combine resistance training with moderate conditioning and sustainable consistency.

For beginners, prioritize simple exercises, good technique, moderate effort, and avoiding excessive soreness.
```

### Chunk 4

- **Source:** `05_warmup_cooldown.md`
- **Similarity score:** `0.7148`

```markdown
# Warm-up and cooldown

Every workout should start with a short warm-up.

A warm-up can include light cardio, mobility, and easier versions of the planned exercises.

For upper-body workouts, include shoulder circles, scapular movement, light rows, or incline push-ups.

For lower-body workouts, include hip circles, bodyweight squats, glute bridges, and light hinges.

Every workout should end with a short cooldown.

A cooldown can include gentle stretching and breathing.

Do not use aggressive stretching if it causes pain.
```

### Chunk 5

- **Source:** `04_bodyweight_exercises.md`
- **Similarity score:** `0.7118`

```markdown
## Pull-up
Primary muscles: lats, upper back, biceps.
Use when: upper-body pull training is appropriate.
Regression: assisted pull-up, band-assisted pull-up, or negative pull-up.
```
