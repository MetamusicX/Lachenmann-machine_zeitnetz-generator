# Vibe Coding the Zeitnetz: Reconstructing Helmut Lachenmann's Serial Time-Grid with AI-Assisted Programming

**Paulo de Assis**
Orpheus Institute, Ghent / ERC Advanced Grant *PostHuman Music*

---

## Abstract

This paper presents the complete algorithmic reconstruction of the Zeitnetz (time-net) — the serial temporal scaffold underlying Helmut Lachenmann's orchestral work *Mouvement (– vor der Erstarrung)* (1982–84). Drawing on Luís Antunes Pena's musicological reverse-engineering of Lachenmann's compositional sketches, a five-stage generative pipeline was implemented in Python, producing the full time-grid with 75 sound families, variable time signatures, and the final duration-as-count transformation. All outputs were verified against Pena's analysis and exported as MusicXML scores. The reconstruction reveals how a deterministic serial mechanism — built from a 12-note pitch row, a permutation matrix, and a duration list — generates the invisible temporal infrastructure that Lachenmann then progressively deforms, overwrites, and dissolves through compositional work. The Zeitnetz is shown to function not as a template to be realised but as a generative constraint to be overcome: the unhewn stone from which the sculpture is carved. A generalised version of the tool, accepting arbitrary inputs with validation and discovery modes, extends the method beyond the single work into a platform for compositional and analytical experimentation. Methodologically, the entire implementation was developed through *vibe coding* — a paradigm of AI-assisted programming in which the author, a composer and musicologist with no software engineering background, directed an AI assistant through natural-language descriptions of the musical logic, mathematical transformations, and desired outputs. The paper argues that this mode of human-machine collaboration offers a productive new model for computational musicology, one in which domain expertise and algorithmic implementation can be separated without loss of analytical rigour.

**Keywords:** Zeitnetz, Helmut Lachenmann, *Mouvement*, serial composition, temporal structuralism, algorithmic analysis, vibe coding, AI-assisted programming, computational musicology, musique concrète instrumentale

---

## 1. Introduction

This paper documents the first project and prototype developed within Research Strand 4 — Creative Lab of the ERC Advanced Grant *PostHuman Music*. At the outset of the project, questions about the relation between automatism and freedom of choice, between structure and expressivity, are crucial and need to be investigated very concretely — by making music or music-generating objects. The project pursues different approaches to composition and creativity; the early experimental prototypes, such as this one, aim at establishing problems, limits, questions, and possible avenues for future research and creative outcomes.

The choice of Helmut Lachenmann's *Mouvement (– vor der Erstarrung)* (1982–84) as a first case study derives from two considerations. First, Lachenmann's reflection on the relation between structure and expressivity — his conviction that "structure is the last possibility for being expressive," understood as the necessary condition to challenge and overcome the dominant aesthetic apparatus, the whole set of acquired habits of notation, scoring, instrumental choice, and modes of playing — culminates with problems central to the questions *PostHuman Music* wishes to address. Second, the author of this study and PI of the project is highly acquainted with Lachenmann's music, aesthetics, and compositional system, making this a natural starting point for investigation.

### 1.1 The dialectic of structure and subjectivity

The dialectic of structure and subjectivity, so crucial for Lachenmann, positions *Mouvement* within the composer's core tension: the struggle between strict serial automatism — the grid — and creative subjectivity — the realisation of the grid. Lachenmann himself describes the relationship:

> "The time grid is a temporal scaffold. I relate to such a serial plan as a sculptor relates to a rough, uncarved stone found by chance." (Lachenmann, cited in Pena, 2004, p. [PAGE TBD])

The **Zeitnetz** (time-net) is precisely this temporal scaffold: a pre-determined serial structure serving as a neutral time skeleton. It is a polyphony of arrangements — a multi-dimensional grid organising abstract layers, managing density and flow across the composition. It determines entries and durations before any specific instrumentation. The grid has no intrinsic meaning; it gains sense only through the subjective decisions of the composer — what exactly will become the sonic event at a specific moment in the score.

The serial plan is thus treated like a found object, an unhewn stone: a generated mechanism devoid of inherent meaning until the composer works against it. Meaning emerges only through interpretation, deformation, and layering. Lachenmann actively distorts the grid to serve musical speech, creating a dialectic between strict rule and intuition.

### 1.2 Generative constraints

To be valid, the Zeitnetz must satisfy three conditions:

1. **Polyphony.** It must be polyphonic — a multi-layered temporal organisation, not a single line.
2. **Global span.** It must span the entire duration of the piece — a single coherent system covering the whole work.
3. **Durational differentiation.** It must contain strictly differentiated durations — precise diversity of proportions across all layers.

Under these constraints, the grid functions as an aid to invention. It provides the resistance necessary for the composer to discover new structural possibilities that pure intuition or feeling would miss. This is the productive core of Lachenmann's method: constraint as the condition of creativity.

### 1.3 From grid to score: temporal structuralism

Understanding the Zeitnetz enables the reconstruction of the compositional process, allowing us to reverse-engineer the work from the bottom up. It offers a precise, reusable model for analysing process-based composition, moving beyond pitch-class set theory into what can be called **temporal structuralism** — the study of how abstract temporal structures generate, constrain, and ultimately give way to concrete musical form.

The Zeitnetz functions as the invisible scaffolding that supports Lachenmann's *musique concrète instrumentale*, linking abstract algorithms to physical gesture. As the Zeitnetz is written and rewritten, notated and re-notated throughout the compositional process, what had been slots in the grid become concrete gestures in the score. The transformation unfolds across several dimensions:

- **From atomic time to varied metre.** The rigid, slot-based atomic time of the Zeitnetz, measured in thirty-second notes, gives way to a varied metre in the score. Bar multiplication creates irregular bars that obscure the original pulse.
- **From abstract polyphony to concrete gesture.** The layers of sound families — defined only by start points, end points, and density, not by specific timbre — become particular instrumental actions. Texture overrides grid.
- **From global span to local articulation.** Where the Zeitnetz provides a single coherent system spanning the entire duration of the work, the score shifts focus to immediate sonic events. The global grid recedes into a subliminal background force.

### 1.4 Beyond the Zeitnetz: the time-grid as generative disappearance

The present paper reconstructs the Zeitnetz in full — Sections 3 through 8 detail every algorithmic stage from row generation to the final duration-as-count transformation. But the reconstruction itself raises an essential question: what happens to the grid once the composer begins to compose?

What the pipeline reconstructs is, strictly speaking, a precondition — not the composition itself. The Zeitnetz operates as an infrastructural layer that initiates compositional thought but does not prescribe its outcomes. Its function is not that of a template to be realised but of a generative constraint to be progressively overcome.

A direct comparison between the reconstructed time-grid and the published score of *Mouvement* reveals a fundamental asymmetry: the temporal positions derived from the Zeitnetz do not map onto the actual entries of sound families or their constituent materials in the score. This non-correspondence is already structurally inscribed in the opening bars, where the extreme temporal expansion — from 3/8 to 12/4, 8/4, and 6/4 — produces bars so dilated that they can accommodate only one or two entries each. At this scale, the grid ceases to function either as an entry-framework or as a rhythmic scaffold; it belongs to the domain of formal proportions rather than to that of notated rhythm.

Crucially, the time-grid does not maintain a single, stable function throughout the work. At certain junctures — notably the entries of sound families 2 and 3 — the grid does coincide with perceptible formal articulations. The listener registers these as structural thresholds, even without access to the underlying temporal scheme. Elsewhere, however, the grid recedes entirely, operating (if at all) as a distant horizon rather than a proximate cause.

What decisively dissolves the legibility of the Zeitnetz is Lachenmann's method of successive rewriting. Each passage undergoes multiple versions, each new layer superimposed upon — and partially effacing — the previous one. The process is palimpsestic: the original temporal structure persists as a buried trace, but its specificity is progressively absorbed into a texture that obeys its own emergent logic. As Cavallotti (2006) has observed, the time-grid in *Mouvement* is respected only to a limited extent. With each renotation, the distance between the generative structure and its compositional realisation widens, until the grid becomes, in effect, unrecognisable.

The Zeitnetz, then, is not a deterministic blueprint but an initial condition — a structured point of departure whose productive force lies precisely in its capacity to be transformed, reinterpreted, and ultimately transcended by the compositional work it sets in motion.

### 1.5 A note on method: vibe coding

The entire pipeline documented in this paper — over two thousand lines of Python, MusicXML export routines, validation logic, and a generalised generator tool — was developed through a practice that has recently come to be known as *vibe coding*. The term was coined by Andrej Karpathy in February 2025 to describe a mode of programming in which a human operator directs an AI coding assistant through natural-language prompts, specifying intent, logic, and constraints in plain English while the AI generates, debugs, and refines the actual code (Karpathy, 2025). Since its naming, vibe coding has gained rapid traction across software engineering and is the subject of growing scholarly attention as a new paradigm of human-machine collaboration in code production.

In the present case, every algorithmic stage was specified by the author — an artist-researcher expert in musicology, music analysis, and composition, not a software engineer — through detailed verbal descriptions of the music-compositional logic, the mathematical transformations, and the desired outputs. The AI assistant (Anthropic's Claude) translated these specifications into functioning code, which was then iteratively tested, corrected, and refined through continued dialogue. The method proved particularly well-suited to this project: the domain knowledge (serial technique, Lachenmann's compositional system, Pena's analytical framework) resided entirely with the human author, while the implementation expertise (Python, MusicXML, algorithmic optimisation) was contributed by the AI. Neither party could have produced the result alone.

The parallel with the paper's own subject is worth noting. Just as Lachenmann treats the serial grid as a found object — a neutral structure to be shaped by compositional intelligence — vibe coding treats the AI's code generation as raw material to be directed by domain expertise and critical judgement. In both cases, the productive force lies not in the automatism itself but in the human capacity to work with and against it.

The technical reconstruction that follows should be read in this light: not as the anatomy of a finished composition, but as the archaeology of its generative ground.

---

## 2. Project overview

This project replicates, in a single Python pipeline, the complete algorithmic process by which Helmut Lachenmann generated the temporal structure (Zeitnetz — "time-net") of his orchestral work *Mouvement (– vor der Erstarrung)* (1982–84). The reconstruction follows Pena's (2004) detailed musicological analysis, which reverse-engineered Lachenmann's process from the sketches and identified five compositional stages, originally realised in IRCAM's OpenMusic environment.

The pipeline takes three inputs — a 12-note pitch row, a permutation pattern, and a duration list — and produces, through a chain of deterministic transformations, the complete Zeitnetz with 75 sound families, variable time signatures, and the final duration-as-count transformation. All intermediate and final results are exported as MusicXML files for verification in standard notation software.

### 2.1 Inputs

The three inputs for Lachenmann's *Mouvement* are:

| Parameter | Values |
|---|---|
| **Pitch row** | 1 11 0 8 9 3 6 4 2 10 5 7 (cis h c gis a dis fis e d ais f g) |
| **Permutation pattern** | 1 5 0 6 2 7 11 8 3 10 4 9 |
| **Duration list** | −11 6 9 7 6 6 4 3 10 6 3 1 10 (13 values; first is negative = initial rest) |

The pipeline uses German pitch names throughout, following Pena's analysis:

| PC | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **Name** | c | cis | d | dis | e | f | fis | g | gis | a | ais | h |

---

## 3. Stage 1 — Row generation

The first stage (corresponding to Pena's OM patch *"1-erzeugt-reihe"*) derives all pitch and rhythmic material from the three inputs.

### 3.1 Permutation matrix

The foundation of the entire system is a 12×12 permutation matrix. Starting from the identity row [0, 1, 2, ..., 11], each subsequent row is generated by applying the permutation pattern as an index reordering of the previous row:

Row 0 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
Row *k* = [Row*ₖ₋₁*[perm[0]], Row*ₖ₋₁*[perm[1]], ..., Row*ₖ₋₁*[perm[11]]]

With the default permutation pattern [1, 5, 0, 6, 2, 7, 11, 8, 3, 10, 4, 9], this produces a 144-element structure that encodes all pitch and rhythmic relationships in the piece.

### 3.2 Onset computation

The 13-element duration list is converted to 12 cumulative onset addresses. The first value (−11) indicates an initial rest of 11 units; its absolute value becomes the first onset. Subsequent onsets are cumulative sums:

onsets[0] = |duration_list[0]| = 11
onsets[*i*] = onsets[*i*−1] + duration_list[*i*] (for *i* = 1..11)

Result: [11, 17, 26, 33, 39, 45, 49, 52, 62, 68, 71, 72]

### 3.3 Rhythm row derivation

The rhythm row is derived by mapping the pitch row through the flattened permutation matrix using the computed onsets as addresses:

1. Flatten the 12×12 matrix into a 144-element sequence.
2. For each pitch pitch_row[*i*], look up flattened[onsets[*i*]] to get the target position.
3. Place the pitch at that position in the rhythm row.

Result: f c dis fis gis e g h d a ais cis

### 3.4 Permutation generation

Both the pitch row and the rhythm row are then permuted 12 times using the permutation matrix, yielding 12 pitch permutations (12×12 = 144 pitch values) and 12 rhythm permutations (12×12 = 144 rhythm values). These two 144-element sequences form the raw material for Stage 2.

> **[FIGURE 1]** Stage 1 — Permutation matrix output: 12-part score showing pitch permutations (left) and rhythm permutations (right), with sequential indices as lyrics. *(Insert Sibelius rendering of `zeitnetz_stage1.musicxml`)*

---

## 4. Stage 2 — Zeitnetz Version 1 (Circular Reading)

Stage 2 (Pena's *"2 - Zeitnetz Version 1"*) produces the Zeitnetz's temporal structure through a circular scanning process.

### 4.1 Circular scanning algorithm

1. **Concatenate** all 12 rhythm permutations into a single 144-element "rhythm tape."
2. **Concatenate** all 12 pitch permutations into a 144-element "pitch target" sequence.
3. For each target pitch in sequence: scan the rhythm tape **circularly forward** from the current cursor position, counting steps until a match is found.
4. The **step count** becomes the **duration** of that note in thirty-second-note units.

The cursor position persists between scans — it does not reset. This circular reading creates the distinctive duration patterns that define the Zeitnetz's rhythmic profile.

### 4.2 Data structure

The result is 12 voice dictionaries, each containing a voice index (0–11), an initial rest in thirty-second notes (Row 0 only: 11 units), and a list of (pitch_class, duration) tuples. Each row contains exactly 12 notes. The durations vary from 1 to 17 thirty-second notes, determined entirely by the circular scanning distances.

### 4.3 MusicXML export

The Stage 2 export creates a single-part score in 3/8 time (the fundamental time signature of the Zeitnetz). The basic unit is the thirty-second note. Each bar contains 12 thirty-second-note grid positions. The 12 rows are laid out sequentially, with each note placed at its exact grid position and duration values appearing as lyrics. All arithmetic uses Python's `Fraction` type to prevent floating-point drift in MusicXML positioning.

> **[FIGURE 2]** Stage 2 — Zeitnetz Version 1: excerpt showing the first rows of the circular reading in 3/8 time, with duration values as lyrics. *(Insert Sibelius rendering of `zeitnetz_stage2.musicxml`)*

---

## 5. Stage 3 — Klangfamilien (Sound Families)

Stage 3 (Pena's *"3 – Klangfamilien"*) derives the 75 sound families that will populate the Zeitnetz.

### 5.1 Starting pitches

The 75 sound families are derived by reading the rhythm permutation rows in a specific circular order: [7, 8, 9, 10, 11, 0, 1, 2, 3, 4, 5, 6]. For each row, pitches are read left-to-right until a "target pitch" (determined by pitch permutation 10, the "control row") is reached, inclusive. The number of pitches collected per row varies, yielding a total of exactly 75 starting pitches across all 12 rows.

The distribution is: Row 7 yields 10 families (F1–F10), Row 8 yields 8 (F11–F18), Row 9 yields 10 (F19–F28), Row 10 yields 10 (F29–F38), Row 11 yields 3 (F39–F41), Row 0 yields 10 (F42–F51), Row 1 yields 1 (F52), Row 2 yields 5 (F53–F57), Row 3 yields 3 (F58–F60), Row 4 yields 4 (F61–F64), Row 5 yields 6 (F65–F70), and Row 6 yields 5 (F71–F75).

### 5.2 End pitches

Each family receives an end pitch through a complementary reading process. The end-pitch tape reads the same rows in **reverse order** [6, 5, 4, 3, 2, 1, 0, 11, 10, 9, 8, 7], reversing each row's pitches. Start pitch *i* is then paired with end-tape pitch *i*.

This yields 75 families, each defined by a (start_pc, end_pc) pair. Notable special cases: Families 8, 12, 34, 42, 45, 64, and 68 have identical start and end pitches (e.g., F8: gis→gis). These require special handling in Stage 4.

> **[FIGURE 3a]** Stage 3.1 — Klangfamilien: rows in the family reading order [7, 8, ..., 6] with family numbers (F1–F75) as lyrics. *(Insert Sibelius rendering of `zeitnetz_stage3_1b_families.musicxml`)*

> **[FIGURE 3b]** Stage 3.2 — Start/end pitch pairs: 75 bi-chords showing each family's starting pitch (lower note) and ending pitch (upper note). *(Insert Sibelius rendering of `zeitnetz_stage3_2.musicxml`)*

---

## 6. Stage 4 — Full Score (Cyclic Zeitnetz + 75 Families)

This is the central stage: the complete Zeitnetz time-grid with all 75 sound families placed on a 13-staff score.

### 6.1 Cyclic Zeitnetz extension

The original 12 rows of the Zeitnetz (from Stage 2) contain only 144 events — insufficient to activate all 75 families through sequential scanning. Lachenmann's solution: **cyclically extend** the Zeitnetz. After the original 12 rows, the rows restart as cyclic continuations, preserving the same durations but without initial rests. The pipeline adds cyclic extensions until all 75 families have activated and deactivated. With the default inputs, 3 extra cycles are required, producing 576 total Zeitnetz events, 3,947 thirty-second-note grid positions, and 329 bars in 3/8 time.

### 6.2 Sequential scan — family activation

A single left-to-right scan of all Zeitnetz events determines when each family activates and deactivates:

1. **Queue:** Families are queued in order F1→F75.
2. **Activation:** The next queued family activates when its start_pc matches the current Zeitnetz event's pitch class.
3. **Event reception:** Every currently active family receives every Zeitnetz event.
4. **Deactivation:** A family deactivates (inclusive — it receives the deactivating event) when its end_pc matches the current event.

For families where start_pc equals end_pc (F8, F12, F34, F42, F45, F64, F68), the family activates on the first occurrence and deactivates on the **next** occurrence of that same pitch — it must receive at least 2 events before deactivation.

### 6.3 Staff assignment

Families are assigned to 12 staves below the Zeitnetz using round-robin: Family *N* → Staff ((*N* − 1) mod 12) + 1. This distributes families evenly: Staves 1–3 receive 7 families each; Staves 4–12 receive 6 each.

### 6.4 Results

The reconstruction produces 329 bars with 3,947 grid positions, requiring 3 cyclic extensions beyond the original 12 rows. All 75 out of 75 families are activated via sequential scan. Family spans range from F2 (2 events, position 39→45) to F75 (18 events, position 3172→3258).

> **[FIGURE 4a]** Stage 4 — Full score, opening bars: the 13-staff layout with the Zeitnetz on staff 1 and the first sound families entering on the lower staves. Duration values appear as lyrics. *(Insert Sibelius rendering of `zeitnetz_stage4_score.musicxml`, bars 1–~20)*

> **[FIGURE 4b]** Stage 4 — Full score, middle section: excerpt showing the density of overlapping families in the central portion of the Zeitnetz. *(Insert Sibelius rendering of `zeitnetz_stage4_score.musicxml`, selected bars from the middle region)*

---

## 7. Zeitnetz Version 2 — Variable Time Signatures

### 7.1 Concept

Every bar from Version 1 (uniform 3/8) is transformed by assigning one of seven time signature types. The crucial principle: each bar retains exactly 12 internal grid positions, but the basic rhythmic unit changes proportionally to the bar's total duration.

### 7.2 The seven time signature types

| Type | Time Sig. | Bar Duration | Unit (bar ÷ 12) | Notation |
|---|---|---|---|---|
| 1 | 3/8 | 3/8 | 1/32 (thirty-second note) | Standard — unchanged from V1 |
| 2 | 4/8 | 4/8 | 1/24 (sixteenth-note triplet) | Tuplet: 3:2 sixteenths per beat |
| 3 | 3/4 | 3/4 | 1/16 (sixteenth note) | Standard — double V1 durations |
| 4 | 4/4 | 4/4 | 1/12 (eighth-note triplet) | Tuplet: 3:2 eighths per beat |
| 5 | 3/2 | 3/2 | 1/8 (eighth note) | Standard |
| 6 | 4/2 | 4/2 | 1/6 (quarter-note triplet) | Tuplet: 3:2 quarters per beat |
| 7 | 12/4 | 12/4 | 1/4 (quarter note) | Standard — 8× V1 durations |

The types form a proportional series: each step roughly doubles the bar duration. Types 2, 4, and 6 require tuplet notation (groups of 3 per beat with explicit bracket markup).

### 7.3 The 105-bar cyclic sequence

The time signatures follow a 105-bar pattern applied cyclically to all 329 bars:

7,6,6,5,5,5,4,4,4,4,3,3,3,3,3,2,2,2,2,2,2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,2,2,2,2,2,2,3,3,3,3,3,3,3,4,4,4,4,4,4,4,5,5,5,5,5,5,5,6,6,6,6,6,6,6,7,7,7,7,7,7,7,7,7,7,7,7,7,7,6,6,6,6,6,6,5,5,5,5,5,4,4,4,4,3,3,3,2,2,1

The pattern has a characteristic **wedge/arch shape**: a descent from type 7 (slowest) to type 1 (fastest), an ascent back to type 7, and a shorter, accelerating contraction back to type 1. For 329 bars, this 105-bar sequence repeats cyclically (3 full cycles plus 14 bars into a fourth).

### 7.4 Tuplet implementation

For types 2, 4, and 6, each bar's 12 grid positions are grouped into 4 groups of 3 (one per beat). Each group receives explicit tuplet brackets (3:2 ratio). When an entire group consists of rests, it is written as a standard beat-length rest without tuplet markup.

### 7.5 Results

The output comprises 329 bars (same count as V1, but with varied durations), distributed across the seven types: Type 1: 45 bars, Type 2: 45, Type 3: 49, Type 4: 49, Type 5: 48, Type 6: 47, Type 7: 46.

> **[FIGURE 5a]** Zeitnetz V2 — Opening bars: the time signature descent from 12/4 (Type 7) through the progressively shorter bar types, showing how the same 12 grid positions are notated with different rhythmic units. *(Insert Sibelius rendering of `zeitnetz_v2.musicxml`, bars 1–~15)*

> **[FIGURE 5b]** Zeitnetz V2 — Tuplet notation: excerpt showing bars of Types 2, 4, or 6 with the 3:2 tuplet brackets. *(Insert Sibelius rendering of `zeitnetz_v2.musicxml`, selected tuplet bars)*

---

## 8. Zeitnetz Final — Duration as Count

### 8.1 Concept

This is Lachenmann's final transformation of the time-grid, as described by Pena:

> "Lachenmann's final step in generating the time-grid consists in multiplying each sound family. The durations of the tones in each family are used to COUNT NOTES in the time-grid in terms of pitches; that is, for example, what previously lasted 6 thirty-second notes now corresponds to the duration of 6 notes of the time-grid." (Pena, 2004, p. [PAGE TBD])

The duration values that previously defined how long a note lasted (in thirty-second-note units) now define how many Zeitnetz events to skip forward to reach the next family entry.

### 8.2 Algorithm

For each of the 75 families:

1. **Retrieve** the family's entries from the Stage 4 sequential scan, including the Zeitnetz event index and duration of each entry.
2. **First entry** remains at its original Zeitnetz event index.
3. **Subsequent entries:** from the current event index, advance forward by the previous entry's duration value (counting Zeitnetz events in the first staff).
4. **Pitch:** each entry takes the pitch of the Zeitnetz event it lands on (not the original Stage 4 pitch).

For example, Family 1's Stage 4 entries have durations [6, 9, 7, 6, 6, 4, 3, 10]. Entry 1.1 begins at Zeitnetz event index 0. Entry 1.2 lands at index 0 + 6 = 6. Entry 1.3 at index 6 + 9 = 15, and so on. This transformation dramatically spreads out the families over the time-grid, since counting 6 events forward covers far more grid positions than 6 thirty-second notes.

### 8.3 Zeitnetz extension

The spreading effect means the Zeitnetz must be long enough to accommodate all final family entries. The pipeline computes the maximum event index needed across all 75 families and extends the cyclic Zeitnetz accordingly. With the default inputs, 3 extra cycles (576 total events) suffice — the maximum index needed is 547.

### 8.4 Greedy staff assignment

Unlike Stage 4's fixed round-robin assignment, the final version uses a greedy interval scheduler to minimise the number of staves. Each family's time span is computed (first entry position to last entry position), families are sorted by start position, and each is assigned to the first staff whose last family ends before the new one starts. If no staff has room, a new one is created. This classic interval scheduling algorithm guarantees the minimum number of staves for non-overlapping spans.

### 8.5 Event labelling

Every note in the family staves carries a label in the format "F.E" where F is the family number and E is the event number within that family (1-based). For example: "1.1" for the first event of Family 1, "35.6" for the sixth event of Family 35.

### 8.6 Results

The final output produces 14 total staves (1 Zeitnetz + 13 family staves), 313 bars, with all 75 families placed and all entries computed. The maximum grid position reaches 3,745. The greedy scheduler packed 75 families into just 13 staves (Staff 1 holds 10 families; Staff 13 holds just 1). Variable time signatures from the V2 cyclic sequence are applied throughout.

### 8.7 Family spread comparison

The duration-as-count transformation dramatically extends each family's temporal span:

| Family | Stage 4 Span | Final Span | Entries |
|---|---|---|---|
| F1 | pos 11 → 62 | pos 11 → 334 | 9 |
| F7 | pos 300 → 381 | pos 300 → 883 | 14 |
| F38 | pos 1632 → 1757 | pos 1632 → 2478 | 15 |
| F75 | pos 3172 → 3258 | pos 3172 → 3745 | 18 |

The output matches the final pages of Pena's Diplomarbeit, confirming the correctness of the entire pipeline.

> **[FIGURE 6a]** Zeitnetz Final — Opening bars: the 14-staff score showing the duration-as-count transformation, with event labels (F.E format) on every note. Compare the wider family spans with Figure 4a. *(Insert Sibelius rendering of `zeitnetz_final.musicxml`, bars 1–~20)*

> **[FIGURE 6b]** Zeitnetz Final — Family spread: excerpt from the middle or late section showing how the duration-as-count transformation distributes families across a much wider temporal span than Stage 4. *(Insert Sibelius rendering of `zeitnetz_final.musicxml`, selected bars)*

> **[FIGURE 6c]** Zeitnetz Final — Comparison with Pena: side-by-side of the pipeline output and the corresponding page from Pena's Diplomarbeit (2004), demonstrating the match. *(Insert Sibelius rendering alongside scan/photo of Pena's original)*

---

## 9. Technical architecture

### 9.1 Design principles

The Mouvement-specific pipeline is contained in a single file (`zeitnetz_pipeline.py`, ~2,270 lines), structured as shared pitch utilities, stage functions, export functions, console summaries, and a main entry point with argument parsing.

Three design decisions proved critical:

**Integer arithmetic throughout.** All grid positions are computed as integers (thirty-second-note units). MusicXML offsets use Python's `Fraction` type to avoid floating-point drift. This was essential — early implementations suffered from cumulative rounding errors over 329+ bars.

**Manual measure construction.** Rather than relying on music21's automatic measure filling (which introduced positioning errors), all measures are constructed manually with explicit offset-based insertion.

**Cyclic extension with termination test.** The Zeitnetz is extended one cycle at a time, with a full sequential scan test after each cycle to determine when all 75 families can complete. A safety cap of 10 cycles prevents infinite loops.

### 9.2 Algorithms

The pipeline employs the following algorithms: permutation matrix construction (Stage 1), onset address computation (Stage 1), circular forward scanning (Stage 2), target-based row reading (Stage 3.1), reverse complementary pairing (Stage 3.2), sequential activation scan (Stage 4), same-pitch deactivation rule (Stage 4), cyclic Zeitnetz extension (Stages 4 and Final), tuplet grouping (V2, Final), duration-as-count transformation (Final), and greedy interval scheduling (Final).

### 9.3 Generalisation

A second, generalised version of the tool was developed as a modular Python package accepting arbitrary pitch rows, permutation patterns, and duration lists. Different inputs produce different numbers of families — experiments with random inputs yielded between 51 and 105 families (Lachenmann's *Mouvement* inputs produce exactly 75). The generalised version includes input validation with repair suggestions (testing duration rotations and pitch transpositions), a discovery mode for finding viable input combinations through smart search (building collision-free duration lists from the permutation matrix), and a browser-based web interface.

---

## 10. Output files

All output files are generated as MusicXML, readable in standard notation software (MuseScore, Sibelius, Finale, Dorico):

| File | Stage | Staves | Bars | Description |
|---|---|---|---|---|
| `zeitnetz_stage1.musicxml` | 1 | 12 | 2 each | Pitch and rhythm permutations |
| `zeitnetz_stage2.musicxml` | 2 | 1 | ~83 | Zeitnetz V1 (12 rows, 3/8) |
| `zeitnetz_stage3_1a_rows.musicxml` | 3.1 | 1 | 12 | Klangfamilien by row order |
| `zeitnetz_stage3_1b_families.musicxml` | 3.1 | 1 | 12 | Klangfamilien by family order |
| `zeitnetz_stage3_2.musicxml` | 3.2 | 1 | 8 | 75 start→end bi-chords |
| `zeitnetz_stage4_score.musicxml` | 4 | 13 | 329 | Full score, uniform 3/8 |
| `zeitnetz_v2.musicxml` | V2 | 13 | 329 | Variable time signatures |
| `zeitnetz_final.musicxml` | Final | 14 | 313 | Duration-as-count, variable TS |

---

## 11. Code availability

The full source code for this project is publicly available in two GitHub repositories.

The **Mouvement-specific pipeline** — a single-file implementation (`zeitnetz_pipeline.py`, ~2,270 lines) that replicates all five stages of Lachenmann's Zeitnetz generation as analysed by Pena — is hosted at:
https://github.com/MetamusicX/Lachenmann-machine_zeitnetz-generator

The **generalised Zeitnetz Generator** — a modular Python package that accepts arbitrary pitch rows, permutation patterns, and duration lists, with input validation, repair suggestions, and a discovery mode for finding viable input combinations — is hosted at:
https://github.com/MetamusicX/zeitnetz-generator

Both implementations require Python 3.9+ and the music21 library (version 9.0 or later). The generalised version includes a browser-based interface for users without command-line experience. All intermediate and final outputs are exported as MusicXML files, readable in standard notation software (MuseScore, Sibelius, Finale, Dorico).

---

## 12. Conclusion

The stages documented above reconstruct, in full algorithmic detail, the generative program behind Lachenmann's *Mouvement*. From three inputs — a pitch row, a permutation pattern, and a duration list — the pipeline produces, through strictly deterministic transformations, a complete Zeitnetz with 75 sound families, variable time signatures, and the final duration-as-count expansion. Every intermediate result has been verified against Pena's (2004) analysis; the output matches the final pages of his Diplomarbeit.

Yet this reconstruction, precisely because it is complete, makes visible the distance between the grid and the composition it enables. The Zeitnetz is the unhewn stone, not the sculpture. Its deterministic rigour — the very quality that makes it algorithmically reproducible — is what Lachenmann's compositional work progressively dissolves. The grid provides the resistance; the music emerges from the struggle against it.

As a first prototype within the Creative Lab of the ERC *PostHuman Music* project, this study establishes a concrete, operational model for the dialectic of automatism and freedom in process-based composition. It also yields a reusable tool: the generalised Zeitnetz Generator accepts arbitrary inputs and can serve as a platform for further compositional and analytical experimentation — opening the question of what other stones might be found, and what other sculptures might be carved from them.

---

## References

Cavallotti, P. (2006). *Differenzen. Poststrukturalistische Aspekte in der Musik der 1980er Jahre am Beispiel von Helmut Lachenmann, Brian Ferneyhough und Gérard Grisey*. Schliengen: Edition Argus.

Karpathy, A. (2025, February 2). Vibe coding [Post]. X (formerly Twitter). https://x.com/kaborsky/status/1886192184808149383

Lachenmann, H. (YEAR). [SOURCE TBD — quote on the time grid as temporal scaffold, cited in Pena 2004, p. PAGE TBD].

Pena, L. A. (2004). *Klangnetz und Klangfarbe in Helmut Lachenmanns Mouvement (– vor der Erstarrung)*. Diplomarbeit, [INSTITUTION TBD].
