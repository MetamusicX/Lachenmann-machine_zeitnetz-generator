# From Serial Grid to Vibe Code: Reconstructing the Zeitnetz of Lachenmann's *Mouvement*

## Full Technical Report

**Based on:** Luís Antunes Pena, *Klangnetz und Klangfarbe in Helmut Lachenmanns Mouvement (– vor der Erstarrung)*, Diplomarbeit, 2004

**Implementation by:** Paulo de Assis, ERC *PostHuman Music*, March 2026

**Repository:** [MetamusicX/Lachenmann-machine_zeitnetz-generator](https://github.com/MetamusicX/Lachenmann-machine_zeitnetz-generator) — Mouvement-specific pipeline (`zeitnetz_pipeline.py`, ~2270 lines)

**Generalised version:** [MetamusicX/zeitnetz-generator](https://github.com/MetamusicX/zeitnetz-generator) — modular package accepting arbitrary inputs, with validation, discovery mode, and web interface

**Dependencies:** Python 3.9+, music21

---

## 1. Introduction

This report documents the first project and prototype developed within **Research Strand 4 — Creative Lab** of the ERC Advanced Grant *PostHuman Music*. At the outset of the project, questions about the relation between automatism and freedom of choice, between structure and expressivity, are crucial and need to be investigated very concretely — by making music or music-generating objects. The project will pursue different approaches to composition and creativity; the early experimental prototypes, such as this one, aim at establishing problems, limits, questions, and possible avenues for future research and creative outcomes.

The choice of Helmut Lachenmann's *Mouvement (– vor der Erstarrung)* (1982–84) as a first case study derives from two considerations. First, Lachenmann's reflection on the relation between structure and expressivity — his conviction that "structure is the last possibility for being expressive," understood as the necessary condition to challenge and overcome the dominant aesthetic apparatus, the whole set of acquired habits of notation, scoring, instrumental choice, and modes of playing — culminates with problems central to the questions *PostHuman Music* wishes to address. Second, the author of this study and PI of the project is highly acquainted with Lachenmann's music, aesthetics, and compositional system, making this a natural starting point for investigation.

### The Dialectic of Structure and Subjectivity

The dialectic of structure and subjectivity, so crucial for Lachenmann, positions *Mouvement* within the composer's core tension: the struggle between strict serial automatism — the grid — and creative subjectivity — the realisation of the grid. Lachenmann himself describes the relationship:

> "The time grid is a temporal scaffold. I relate to such a serial plan as a sculptor relates to a rough, uncarved stone found by chance."

The **Zeitnetz** (time-net) is precisely this temporal scaffold: a pre-determined serial structure serving as a neutral time skeleton. It is a polyphony of arrangements — a multi-dimensional grid organising abstract layers, managing density and flow across the composition. It determines entries and durations before any specific instrumentation. The grid has no intrinsic meaning; it gains sense only through the subjective decisions of the composer — what exactly will become the sonic event at a specific moment in the score.

The serial plan is thus treated like a found object, an unhewn stone: a generated mechanism devoid of inherent meaning until the composer works against it. Meaning emerges only through interpretation, deformation, and layering. Lachenmann actively distorts the grid to serve musical speech, creating a dialectic between strict rule and intuition.

### Generative Constraints

To be valid, the Zeitnetz must satisfy three conditions:

1. **Polyphony.** It must be polyphonic — a multi-layered temporal organisation, not a single line.
2. **Global span.** It must span the entire duration of the piece — a single coherent system covering the whole work.
3. **Durational differentiation.** It must contain strictly differentiated durations — precise diversity of proportions across all layers.

Under these constraints, the grid functions as an aid to invention. It provides the resistance necessary for the composer to discover new structural possibilities that pure intuition or feeling would miss. This is the productive core of Lachenmann's method: constraint as the condition of creativity.

### From Grid to Score: Temporal Structuralism

Understanding the Zeitnetz enables the reconstruction of the compositional process, allowing us to reverse-engineer the work from the bottom up. It offers a precise, reusable model for analysing process-based composition, moving beyond pitch-class set theory into what can be called **temporal structuralism** — the study of how abstract temporal structures generate, constrain, and ultimately give way to concrete musical form.

The Zeitnetz functions as the invisible scaffolding that supports Lachenmann's *musique concrète instrumentale*, linking abstract algorithms to physical gesture. As the Zeitnetz is written and rewritten, notated and re-notated throughout the compositional process, what had been slots in the grid become concrete gestures in the score. The transformation unfolds across several dimensions:

- **From atomic time to varied metre.** The rigid, slot-based atomic time of the Zeitnetz, measured in thirty-second notes, gives way to a varied metre in the score. Bar multiplication creates irregular bars that obscure the original pulse.
- **From abstract polyphony to concrete gesture.** The layers of sound families — defined only by start points, end points, and density, not by specific timbre — become particular instrumental actions. Texture overrides grid.
- **From global span to local articulation.** Where the Zeitnetz provides a single coherent system spanning the entire duration of the work, the score shifts focus to immediate sonic events. The global grid recedes into a subliminal background force.

The present report reconstructs this program in full — Sections 2 through 9 detail every algorithmic stage from row generation to the final duration-as-count transformation. But the reconstruction itself raises an essential question: what happens to the grid once the composer begins to compose?

### Beyond the Zeitnetz: The Time-Grid as Generative Disappearance

What the pipeline reconstructs is, strictly speaking, a precondition — not the composition itself. The Zeitnetz operates as an infrastructural layer that initiates compositional thought but does not prescribe its outcomes. Its function is not that of a template to be realised but of a generative constraint to be progressively overcome.

A direct comparison between the reconstructed time-grid and the published score of *Mouvement* reveals a fundamental asymmetry: the temporal positions derived from the Zeitnetz do not map onto the actual entries of sound families or their constituent materials in the score. This non-correspondence is already structurally inscribed in the opening bars, where the extreme temporal expansion — from 3/8 to 12/4, 8/4, and 6/4 — produces bars so dilated that they can accommodate only one or two entries each. At this scale, the grid ceases to function either as an entry-framework or as a rhythmic scaffold; it belongs to the domain of formal proportions rather than to that of notated rhythm.

Crucially, the time-grid does not maintain a single, stable function throughout the work. At certain junctures — notably the entries of sound families 2 and 3 — the grid does coincide with perceptible formal articulations. The listener registers these as structural thresholds, even without access to the underlying temporal scheme. Elsewhere, however, the grid recedes entirely, operating (if at all) as a distant horizon rather than a proximate cause.

What decisively dissolves the legibility of the Zeitnetz is Lachenmann's method of successive rewriting. Each passage undergoes multiple versions, each new layer superimposed upon — and partially effacing — the previous one. The process is palimpsestic: the original temporal structure persists as a buried trace, but its specificity is progressively absorbed into a texture that obeys its own emergent logic. As Cavallotti has observed, the time-grid in *Mouvement* is respected only to a limited extent. With each renotation, the distance between the generative structure and its compositional realisation widens, until the grid becomes, in effect, unrecognisable.

The Zeitnetz, then, is not a deterministic blueprint but an initial condition — a structured point of departure whose productive force lies precisely in its capacity to be transformed, reinterpreted, and ultimately transcended by the compositional work it sets in motion.

### A Note on Method: Vibe Coding

The entire pipeline documented in this report — over two thousand lines of Python, MusicXML export routines, validation logic, and a generalised generator tool — was developed through a practice that has recently come to be known as *vibe coding*. The term was coined by Andrej Karpathy in February 2025 to describe a mode of programming in which a human operator directs an AI coding assistant through natural-language prompts, specifying intent, logic, and constraints in plain English while the AI generates, debugs, and refines the actual code. Since its naming, vibe coding has gained rapid traction across software engineering and is the subject of growing scholarly attention as a new paradigm of human-machine collaboration in code production.

In the present case, every algorithmic stage was specified by the author — an artist-researcher expert in musicology, music analysis, and composition, not a software engineer — through detailed verbal descriptions of the music-compositional logic, the mathematical transformations, and the desired outputs. The AI assistant (Anthropic's Claude) translated these specifications into functioning code, which was then iteratively tested, corrected, and refined through continued dialogue. The method proved particularly well-suited to this project: the domain knowledge (serial technique, Lachenmann's compositional system, Pena's analytical framework) resided entirely with the human author, while the implementation expertise (Python, MusicXML, algorithmic optimisation) was contributed by the AI. Neither party could have produced the result alone.

The parallel with the report's own subject is worth noting. Just as Lachenmann treats the serial grid as a found object — a neutral structure to be shaped by compositional intelligence — vibe coding treats the AI's code generation as raw material to be directed by domain expertise and critical judgement. In both cases, the productive force lies not in the automatism itself but in the human capacity to work with and against it.

The technical reconstruction that follows should be read in this light: not as the anatomy of a finished composition, but as the archaeology of its generative ground.

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [Project Overview](#2-project-overview)
3. [Stage 1 — Row Generation](#3-stage-1--row-generation)
4. [Stage 2 — Zeitnetz Version 1 (Circular Reading)](#4-stage-2--zeitnetz-version-1)
5. [Stage 3 — Klangfamilien (Sound Families)](#5-stage-3--klangfamilien)
6. [Stage 4 — Full Score (Cyclic Zeitnetz + 75 Families)](#6-stage-4--full-score)
7. [Zeitnetz Version 2 — Variable Time Signatures](#7-zeitnetz-version-2--variable-time-signatures)
8. [Zeitnetz Final — Duration as Count](#8-zeitnetz-final--duration-as-count)
9. [Output Files](#9-output-files)
10. [Technical Architecture](#10-technical-architecture)
11. [Usage](#11-usage)
12. [Conclusion](#12-conclusion)

---

## 2. Project Overview

This project replicates, in a single Python pipeline, the complete algorithmic process by which Helmut Lachenmann generated the temporal structure (Zeitnetz — "time-net") of his orchestral work *Mouvement (– vor der Erstarrung)* (1982–84). The reconstruction follows Luís Antunes Pena's detailed musicological analysis, which reverse-engineered Lachenmann's process from the sketches and identified five compositional stages, originally realised in IRCAM's OpenMusic environment.

The pipeline takes three inputs — a 12-note pitch row, a permutation pattern, and a duration list — and produces, through a chain of deterministic transformations, the complete Zeitnetz with 75 sound families, variable time signatures, and the final duration-as-count transformation. All intermediate and final results are exported as MusicXML files for verification in standard notation software.

### Default Inputs (Lachenmann's *Mouvement*)

| Parameter | Values |
|---|---|
| **Pitch row** | 1 11 0 8 9 3 6 4 2 10 5 7 (cis h c gis a dis fis e d ais f g) |
| **Permutation pattern** | 1 5 0 6 2 7 11 8 3 10 4 9 |
| **Duration list** | −11 6 9 7 6 6 4 3 10 6 3 1 10 (13 values; first is negative = initial rest) |

### Pitch Naming Convention

The pipeline uses German pitch names throughout, following Pena's analysis:

| PC | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **Name** | c | cis | d | dis | e | f | fis | g | gis | a | ais | h |

---

## 3. Stage 1 — Row Generation

**OM patch:** *"1-erzeugt-reihe"*
**Function:** `run_stage1(pitch_row, perm_pattern, duration_list)`
**Export:** `zeitnetz_stage1.musicxml`

### 3.1 Permutation Matrix

The foundation of the entire system is a 12×12 permutation matrix. Starting from the identity row [0, 1, 2, ..., 11], each subsequent row is generated by applying the permutation pattern as an index reordering of the previous row:

```
Row 0 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
Row k = [Row_{k-1}[perm[0]], Row_{k-1}[perm[1]], ..., Row_{k-1}[perm[11]]]
```

With the default permutation pattern [1, 5, 0, 6, 2, 7, 11, 8, 3, 10, 4, 9], this produces a 144-element structure that encodes all pitch and rhythmic relationships in the piece.

### 3.2 Onset Computation

The 13-element duration list is converted to 12 cumulative onset addresses. The first value (−11) indicates an initial rest of 11 units; its absolute value becomes the first onset. Subsequent onsets are cumulative sums:

```
onsets[0] = |duration_list[0]| = 11
onsets[i] = onsets[i-1] + duration_list[i]   (for i = 1..11)
```

Result: [11, 17, 26, 33, 39, 45, 49, 52, 62, 68, 71, 72]

### 3.3 Rhythm Row Derivation

The rhythm row is derived by mapping the pitch row through the flattened permutation matrix using the computed onsets as addresses:

1. Flatten the 12×12 matrix into a 144-element sequence
2. For each pitch `pitch_row[i]`, look up `flattened[onsets[i]]` to get the target position
3. Place the pitch at that position in the rhythm row

Result: f c dis fis gis e g h d a ais cis

### 3.4 Permutation Generation

Both the pitch row and the rhythm row are then permuted 12 times using the permutation matrix, yielding:
- **12 pitch permutations** (12×12 = 144 pitch values)
- **12 rhythm permutations** (12×12 = 144 rhythm values)

These two 144-element sequences form the raw material for Stage 2.

### MusicXML Export

The Stage 1 export creates a 12-part score in 12/4 time, where each part represents one row (k = 0–11). Each part has two measures: the pitch permutation and the rhythm permutation. Sequential indices (0–143) appear as lyrics.

---

## 4. Stage 2 — Zeitnetz Version 1

**OM patch:** *"2 - Zeitnetz Version 1"*
**Function:** `run_stage2(s1)`
**Export:** `zeitnetz_stage2.musicxml`

### 4.1 Circular Scanning Algorithm

Stage 2 produces the Zeitnetz's temporal structure through a circular scanning process:

1. **Concatenate** all 12 rhythm permutations into a single 144-element "rhythm tape"
2. **Concatenate** all 12 pitch permutations into a 144-element "pitch target" sequence
3. For each target pitch in sequence: scan the rhythm tape **circularly forward** from the current cursor position, counting steps until a match is found
4. The **step count** becomes the **duration** of that note in 32nd-note units

The cursor position persists between scans — it does not reset. This circular reading creates the distinctive duration patterns that define the Zeitnetz's rhythmic profile.

### 4.2 Data Structure

The result is 12 voice dictionaries, each containing:

| Field | Description |
|---|---|
| `voice_index` | Row number (0–11) |
| `initial_rest_32nds` | Initial rest in 32nd notes (Row 0 only: 11 units) |
| `notes` | List of `(pitch_class, duration_in_32nds)` tuples |

### 4.3 Example: Row 0 (Voice 1)

```
Rest: 11 thirty-second notes
cis(6)  h(9)  c(7)  gis(6)  a(6)  dis(4)  fis(3)  e(10)  d(6)  ais(3)  f(1)  g(10)
```

Each row contains exactly 12 notes. The durations vary from 1 to 17 thirty-second notes, determined entirely by the circular scanning distances.

### MusicXML Export

The Stage 2 export creates a single-part score in 3/8 time (the fundamental time signature of the Zeitnetz). The basic unit is the thirty-second note. Each bar contains 12 thirty-second-note grid positions. The 12 rows are laid out sequentially (Row 0, then Row 1, etc.), with each note placed at its exact grid position. Duration values appear as lyrics. All arithmetic uses Python's `Fraction` type to prevent floating-point drift in MusicXML positioning.

---

## 5. Stage 3 — Klangfamilien

**OM patch:** *"3 – Klangfamilien"*

### 5.1 Stage 3.1 — Starting Pitches

**Function:** `run_stage3(s1)`
**Export:** `zeitnetz_stage3_1a_rows.musicxml`, `zeitnetz_stage3_1b_families.musicxml`

The 75 sound families are derived by reading the rhythm permutation rows in a specific circular order:

**Row reading order:** [7, 8, 9, 10, 11, 0, 1, 2, 3, 4, 5, 6]

For each row, pitches are read left-to-right until a "target pitch" (determined by pitch permutation 10, the "control row") is reached, inclusive. The number of pitches collected per row varies, yielding a total of exactly 75 starting pitches across all 12 rows:

| Row | Families | Count |
|---|---|---|
| Row 7 | F1–F10 | 10 |
| Row 8 | F11–F18 | 8 |
| Row 9 | F19–F28 | 10 |
| Row 10 | F29–F38 | 10 |
| Row 11 | F39–F41 | 3 |
| Row 0 | F42–F51 | 10 |
| Row 1 | F52 | 1 |
| Row 2 | F53–F57 | 5 |
| Row 3 | F58–F60 | 3 |
| Row 4 | F61–F64 | 4 |
| Row 5 | F65–F70 | 6 |
| Row 6 | F71–F75 | 5 |
| **Total** | | **75** |

### 5.2 Stage 3.2 — End Pitches

**Function:** `run_stage3_2(s3_1)`
**Export:** `zeitnetz_stage3_2.musicxml`

Each family receives an end pitch through a complementary reading process:

1. **End-pitch tape:** Read the same rows in **reverse order** [6, 5, 4, 3, 2, 1, 0, 11, 10, 9, 8, 7], and **reverse each row's pitches**
2. **Pair** start pitch *i* with end-tape pitch *i*

This yields 75 families, each defined by a `(start_pc, end_pc)` pair. Notable special cases: **Families 8, 12, 34, 42, 45, 64, and 68** have identical start and end pitches (e.g., F8: gis→gis). These require special handling in Stage 4.

### MusicXML Export

Two files are generated for Stage 3.1: (a) rows in original order with pitch names as lyrics, and (b) rows in the family reading order [7,8,...,6] with family numbers (F1–F75) as lyrics. Stage 3.2 exports 75 bi-chords (lower note = start pitch in octave 4, upper note = end pitch in octave 5), grouped 10 per bar in 10/4 time.

---

## 6. Stage 4 — Full Score (Cyclic Zeitnetz + 75 Families)

**Function:** `export_stage4_score(s2, s3_2)`
**Export:** `zeitnetz_stage4_score.musicxml`

This is the central stage: the complete Zeitnetz time-grid with all 75 sound families placed on a 13-staff score.

### 6.1 Cyclic Zeitnetz Extension

The original 12 rows of the Zeitnetz (from Stage 2) contain only 144 events — insufficient to activate all 75 families through sequential scanning. Lachenmann's solution: **cyclically extend** the Zeitnetz. After the original 12 rows (Row 0–Row 11), the rows restart as "Row 0b", "Row 1b", "Row 2b", etc., preserving the same durations but without initial rests (continuous concatenation).

The pipeline adds cyclic extensions until all 75 families have activated and deactivated. With the default inputs, **3 extra cycles** are required, producing:
- **576 total Zeitnetz events** (144 original + 3 × 144 cyclic)
- **3,947 thirty-second-note grid positions**
- **329 bars** in 3/8 time

### 6.2 Sequential Scan — Family Activation

A single left-to-right scan of all Zeitnetz events determines when each family activates and deactivates:

1. **Queue:** Families are queued in order F1→F75
2. **Activation:** The next queued family activates when its `start_pc` matches the current Zeitnetz event's pitch class
3. **Event reception:** Every currently active family receives every Zeitnetz event
4. **Deactivation:** A family deactivates (inclusive — it receives the deactivating event) when its `end_pc` matches the current event

**Same-pitch deactivation rule:** For families where `start_pc == end_pc` (F8, F12, F34, F42, F45, F64, F68), the family activates on the first occurrence and deactivates on the **next** occurrence of that same pitch — it must receive at least 2 events before deactivation.

### 6.3 Staff Assignment

Families are assigned to 12 staves below the Zeitnetz using round-robin:

```
Family N → Staff ((N − 1) mod 12) + 1
```

This distributes families evenly: Staves 1–3 receive 7 families each; Staves 4–12 receive 6 each.

### 6.4 Score Structure

| Staff | Content |
|---|---|
| Staff 1 (top) | Zeitnetz — all events with row labels and duration lyrics |
| Staves 2–13 | Sound families — notes at their activation positions, with duration lyrics and family labels (F1, F2, ...) at first entry |

All notes are rendered as single grid units (1 thirty-second note). Rests fill the gaps between notes. Duration values from the Zeitnetz appear as lyrics on every note in both the Zeitnetz staff and the family staves.

### 6.5 Results Summary

- **329 bars**, 3947 grid positions
- **3 cyclic extensions** beyond the original 12 rows
- **75/75 families** activated via sequential scan
- Family spans range from F2 (2 events, pos 39→45) to F75 (18 events, pos 3172→3258)

---

## 7. Zeitnetz Version 2 — Variable Time Signatures

**Function:** `export_zeitnetz_v2(s2, s3_2)`
**Export:** `zeitnetz_v2.musicxml`

### 7.1 Concept

Every bar from Version 1 (uniform 3/8) is transformed by assigning one of 7 time signature types. The crucial principle: **each bar retains exactly 12 internal grid positions**, but the basic rhythmic unit changes proportionally to the bar's total duration.

### 7.2 The Seven Time Signature Types

| Type | Time Sig. | Bar Duration | Unit (bar ÷ 12) | Notation |
|---|---|---|---|---|
| 1 | 3/8 | 3/8 | 1/32 (thirty-second note) | Standard — unchanged from V1 |
| 2 | 4/8 | 4/8 | 1/24 (sixteenth-note triplet) | Tuplet: 3:2 sixteenths per beat |
| 3 | 3/4 | 3/4 | 1/16 (sixteenth note) | Standard — double V1 durations |
| 4 | 4/4 | 4/4 | 1/12 (eighth-note triplet) | Tuplet: 3:2 eighths per beat |
| 5 | 3/2 | 3/2 | 1/8 (eighth note) | Standard |
| 6 | 4/2 | 4/2 | 1/6 (quarter-note triplet) | Tuplet: 3:2 quarters per beat |
| 7 | 12/4 | 12/4 | 1/4 (quarter note) | Standard — 8× V1 durations |

The types form a proportional series: each step roughly doubles the bar duration. Types 2, 4, and 6 require **tuplet notation** (groups of 3 per beat with explicit bracket markup).

### 7.3 The 105-Bar Cyclic Sequence

The time signatures follow a 105-bar pattern applied cyclically to all 329 bars:

```
7,6,6,5,5,5,4,4,4,4,3,3,3,3,3,2,2,2,2,2,2,
1,1,1,1,1,1,1,1,1,1,1,1,1,1,
2,2,2,2,2,2,2,3,3,3,3,3,3,3,4,4,4,4,4,4,4,
5,5,5,5,5,5,5,6,6,6,6,6,6,6,
7,7,7,7,7,7,7,7,7,7,7,7,7,7,
6,6,6,6,6,6,5,5,5,5,5,4,4,4,4,3,3,3,2,2,1
```

The pattern has a characteristic **wedge/arch shape**:
1. **Descent** (bars 1–35): From type 7 (slowest) down to type 1 (fastest), with increasing repetitions as types get smaller
2. **Ascent** (bars 36–84): Back up from type 1 to type 7, 7 bars per type then 14×7
3. **Descent** (bars 85–105): A shorter, accelerating contraction back to type 1

For 329 bars, this 105-bar sequence repeats cyclically (3 full cycles + 14 bars into a 4th).

### 7.4 Tuplet Implementation

For types 2, 4, and 6, each bar's 12 grid positions are grouped into **4 groups of 3** (one per beat). Each group receives explicit tuplet brackets (3:2 ratio). When an entire group consists of rests, it is written as a standard beat-length rest without tuplet markup.

### 7.5 Results Summary

- **329 bars** (same count as V1, but with varied durations)
- **13 staves** (same structure as Stage 4)
- Bar type distribution: Type 1: 45, Type 2: 45, Type 3: 49, Type 4: 49, Type 5: 48, Type 6: 47, Type 7: 46
- Time signatures written only when they change (not repeated in consecutive same-type bars)
- File size: 2.4 MB (vs 1.4 MB for Stage 4) due to tuplet markup complexity

---

## 8. Zeitnetz Final — Duration as Count

**Function:** `export_zeitnetz_final(s2, s3_2)`
**Export:** `zeitnetz_final.musicxml`

### 8.1 Concept

This is Lachenmann's final transformation of the time-grid, as described by Pena:

> "Lachenmann's final step in generating the time-grid consists in multiplying each sound family. The durations of the tones in each family are used to COUNT NOTES in the time-grid in terms of pitches; that is, for example, what previously lasted 6 thirty-second notes now corresponds to the duration of 6 notes of the time-grid."

The duration values that previously defined how long a note lasted (in 32nd-note units) now define **how many Zeitnetz events to skip forward** to reach the next family entry.

### 8.2 Algorithm

For each of the 75 families:

1. **Retrieve** the family's entries from the Stage 4 sequential scan, including the Zeitnetz event index and duration of each entry
2. **First entry** remains at its original Zeitnetz event index
3. **Subsequent entries:** from the current event index, advance forward by the previous entry's duration value (counting Zeitnetz events in staff 1)
4. **Pitch:** each entry takes the pitch of the Zeitnetz event it lands on (NOT the original Stage 4 pitch)

**Concrete example (Family 1):**
- Stage 4 entries have durations: [6, 9, 7, 6, 6, 4, 3, 10]
- Entry 1.1: Zeitnetz event index 0 (position 11, pitch cis)
- Entry 1.2: index 0 + 6 = 6 (lands on a different Zeitnetz event, takes its pitch)
- Entry 1.3: index 6 + 9 = 15
- Entry 1.4: index 15 + 7 = 22
- ...and so on

This transformation dramatically spreads out the families over the time-grid, since counting 6 events forward covers far more grid positions than 6 thirty-second notes.

### 8.3 Zeitnetz Extension

The spreading effect means the Zeitnetz must be long enough to accommodate all final family entries. The pipeline computes the maximum event index needed across all 75 families and extends the cyclic Zeitnetz accordingly. With the default inputs, 3 extra cycles (576 total events) suffice — the maximum index needed is 547.

### 8.4 Greedy Staff Assignment

Unlike Stage 4's fixed round-robin assignment, the final version uses a **greedy interval scheduler** to minimise the number of staves:

1. Compute each family's time span (first entry position → last entry position)
2. Sort families by start position
3. For each family, assign it to the first staff whose last family ends before this family starts
4. If no staff has room, create a new one

This is the classic interval scheduling algorithm guaranteeing the minimum number of staves for non-overlapping spans.

### 8.5 Event Labelling

Every note in the family staves carries a lyric in the format **"F.E"** where F is the family number and E is the event number within that family (1-based). For example: "1.1" for the first event of Family 1, "35.6" for the sixth event of Family 35.

### 8.6 Results Summary

- **14 total staves** (1 Zeitnetz + 13 family staves — only 1 more than Stage 4)
- **313 bars**
- **75/75 families** placed, all entries computed
- Maximum grid position: 3,745
- The greedy scheduler packed 75 families into just 13 staves (Staff 1 holds 10 families; Staff 13 holds just 1)
- Variable time signatures from the V2 cyclic sequence are applied throughout
- The output matches the final pages of Pena's Diplomarbeit, confirming the correctness of the entire pipeline

### 8.7 Family Spread Comparison (Selected Examples)

| Family | Stage 4 Span | Final Span | Entries |
|---|---|---|---|
| F1 | pos 11 → 62 | pos 11 → 334 | 9 |
| F7 | pos 300 → 381 | pos 300 → 883 | 14 |
| F38 | pos 1632 → 1757 | pos 1632 → 2478 | 15 |
| F75 | pos 3172 → 3258 | pos 3172 → 3745 | 18 |

---

## 9. Output Files

All output files are generated in the repository's working directory:

| File | Stage | Staves | Bars | Description |
|---|---|---|---|---|
| `zeitnetz_stage1.musicxml` | 1 | 12 | 2 each | Pitch & rhythm permutations |
| `zeitnetz_stage2.musicxml` | 2 | 1 | ~83 | Zeitnetz V1 (12 rows, 3/8) |
| `zeitnetz_stage3_1a_rows.musicxml` | 3.1 | 1 | 12 | Klangfamilien by row order |
| `zeitnetz_stage3_1b_families.musicxml` | 3.1 | 1 | 12 | Klangfamilien by family order |
| `zeitnetz_stage3_2.musicxml` | 3.2 | 1 | 8 | 75 start→end bi-chords |
| `zeitnetz_stage4_score.musicxml` | 4 | 13 | 329 | Full score, uniform 3/8 |
| `zeitnetz_v2.musicxml` | V2 | 13 | 329 | Variable time signatures |
| `zeitnetz_final.musicxml` | Final | 14 | 313 | Duration-as-count, variable TS |

---

## 10. Technical Architecture

### 10.1 Single-File Pipeline

The entire system is contained in `zeitnetz_pipeline.py`, structured as:

1. **Shared pitch utilities** — conversion tables, parsers
2. **Stage functions** — `run_stage1()` through `run_stage5()`, plus `run_stage3_2()`
3. **Export functions** — one per output file, including `export_stage4_score()`, `export_zeitnetz_v2()`, `export_zeitnetz_final()`
4. **Console print functions** — formatted summaries per stage
5. **Main entry point** — argument parsing and sequential execution

### 10.2 Key Design Decisions

**Integer arithmetic throughout.** All grid positions are computed as integers (32nd-note units). MusicXML offsets use Python's `Fraction` type to avoid floating-point drift. This was essential — early implementations suffered from cumulative rounding errors over 329+ bars.

**Manual measure construction.** Rather than relying on music21's automatic measure filling (which introduced positioning errors), all measures are constructed manually with explicit `m.insert(offset, element)` calls.

**Cyclic extension with termination test.** The Zeitnetz is extended one cycle at a time, with a full sequential scan test (`_test_all_families_done()`) after each cycle to determine when all 75 families can complete. A safety cap of 10 cycles prevents infinite loops.

**Self-contained export functions.** Each export function regenerates its own data from the Stage 2 and Stage 3.2 inputs, rather than depending on mutable shared state. This ensures correctness and allows independent re-generation.

### 10.3 Algorithms

| Algorithm | Stage | Purpose |
|---|---|---|
| Permutation matrix construction | 1 | Generate 12×12 transformation matrix |
| Onset address computation | 1 | Map duration list to matrix addresses |
| Circular forward scanning | 2 | Derive durations from pitch distances |
| Target-based row reading | 3.1 | Extract 75 family starting pitches |
| Reverse complementary pairing | 3.2 | Assign end pitches to families |
| Sequential activation scan | 4 | Activate/deactivate families over Zeitnetz |
| Same-pitch deactivation rule | 4 | Handle families with identical start/end PC |
| Cyclic Zeitnetz extension | 4, Final | Extend time-grid until all families complete |
| Tuplet grouping (3 per beat) | V2, Final | Proper bracket notation for triplet bars |
| Duration-as-count transformation | Final | Convert durations to event-skip counts |
| Greedy interval scheduling | Final | Minimise family staves |

---

## 11. Usage

### Command Line

```bash
# Run full pipeline with default Lachenmann values, export all MusicXML files
python3 zeitnetz_pipeline.py --export

# Custom pitch row (German names)
python3 zeitnetz_pipeline.py --pitches "cis h c gis a dis fis e d ais f g" --export

# Custom pitch row (integers)
python3 zeitnetz_pipeline.py --pitches "0 1 2 3 4 5 6 7 8 9 10 11" --export
```

### Arguments

| Argument | Default | Description |
|---|---|---|
| `--pitches` | "1 11 0 8 9 3 6 4 2 10 5 7" | 12 pitch classes (integers 0–11 or German names) |
| `--perm` | "1 5 0 6 2 7 11 8 3 10 4 9" | Permutation pattern (12 integers, 0-indexed) |
| `--durations` | "−11 6 9 7 6 6 4 3 10 6 3 1 10" | Duration list (13 integers; first may be negative) |
| `--axis` | pitch_row[0] | Symmetry axis pitch class 0–11 |
| `--export` | off | Write MusicXML files for all stages |

---

## 12. Conclusion

The ten stages documented above reconstruct, in full algorithmic detail, the generative program behind Lachenmann's *Mouvement*. From three inputs — a pitch row, a permutation pattern, and a duration list — the pipeline produces, through strictly deterministic transformations, a complete Zeitnetz with 75 sound families, variable time signatures, and the final duration-as-count expansion. Every intermediate result has been verified against Pena's analysis; the output matches the final pages of his Diplomarbeit.

Yet this reconstruction, precisely because it is complete, makes visible the distance between the grid and the composition it enables. The Zeitnetz is the unhewn stone, not the sculpture. Its deterministic rigour — the very quality that makes it algorithmically reproducible — is what Lachenmann's compositional work progressively dissolves. The grid provides the resistance; the music emerges from the struggle against it.

As a first prototype within the Creative Lab of the ERC *PostHuman Music* project, this study establishes a concrete, operational model for the dialectic of automatism and freedom in process-based composition. It also yields a reusable tool: the [generalised Zeitnetz Generator](https://github.com/MetamusicX/zeitnetz-generator) accepts arbitrary inputs and can serve as a platform for further compositional and analytical experimentation — opening the question of what other stones might be found, and what other sculptures might be carved from them.

---

## Appendix: Development History

This pipeline was developed across multiple collaborative sessions between Paulo de Assis and Claude (Anthropic) in March 2026:

- **Session 1 (March 17):** Stages 1–3 implemented and verified against Pena's analysis. Initial standalone scripts per stage.
- **Session 2 (March 18–19):** Consolidation into single pipeline file. Stage 4 (Netz-Familien) and Stage 5 (Final Netz) implemented following Pena's OpenMusic patch descriptions.
- **Session 3 (March 20):** Complete rewrite of Stage 4 as Full Score with cyclic Zeitnetz extension, sequential scan family activation, same-pitch deactivation rule, and round-robin staff assignment. Resolved the critical 25/75 activation problem through cyclic extension. Cleanup of outdated files.
- **Session 4 (March 21):** Zeitnetz Version 2 with variable time signatures (7 types, 105-bar cyclic sequence, tuplet notation). Zeitnetz Final with duration-as-count transformation, greedy staff assignment, and event labelling. Final verification against Pena's Diplomarbeit confirmed correctness.

---

*Report generated: 21 March 2026*
*Pipeline version: zeitnetz_pipeline.py (single source, ~2270 lines)*
*Validation: Output matches final pages of Pena's bachelor thesis*
