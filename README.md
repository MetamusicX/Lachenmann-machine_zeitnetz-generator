# Lachenmann Machine — Zeitnetz Generator

**A complete algorithmic pipeline replicating and generalising the Zeitnetz (time-net) generation process underlying Helmut Lachenmann's *Mouvement (– vor der Erstarrung)* (1982–84).**

Based on Luís Antunes Pena's analytical reconstruction of Lachenmann's serial procedures (bachelor thesis, 2004), this pipeline translates the original OpenMusic patches into a standalone Python implementation using [music21](https://web.mit.edu/music21/). All outputs are exported as **MusicXML** files, ready for import into Sibelius, Dorico, MuseScore, or Finale.

---

## The Five-Stage Pipeline

The pipeline replicates each of Pena's original OpenMusic patches:

### Stage 1 — Row Generation
*OM patch: "1-erzeugt-reihe"*

Builds a 12×12 permutation matrix from the pitch row and permutation pattern. Derives the rhythm row via onset addresses computed from the duration list. Produces:
- The complete permutation matrix (12 rows of 12 pitch classes)
- The rhythm row

### Stage 2 — Zeitnetz Version 1 (Circular Reading)
*OM patch: "2 - Zeitnetz Version 1"*

Concatenates all permutations into tapes and performs a circular forward scan to derive durations. Produces 12 rows of 12 notes in 3/8 time — the core Zeitnetz.

### Stage 3 — Klangfamilien (Sound Families)
*OM patch: "3 – Klangfamilien"*

Reads the permutation rows in a specific circular order to extract family start pitches. End pitches are derived by a symmetrical mirror reading along the matrix's main diagonal. Lachenmann's inputs produce **75 sound families**, each defined by a start and end pitch class.

### Stage 4 — Full Score (Netz-Familien)
*OM patch: "4-Netz-Familien"*

Cyclically extends the Zeitnetz until all 75 families have both activated and deactivated. Produces a multi-staff score with the Zeitnetz on the top staff and families distributed below — the complete temporal scaffold.

### Stage 5 — Variable Time Signatures and Duration as Count
*OM patch: "5-Netz / Zeitnetz 3"*

Applies Lachenmann's cyclic sequence of seven time signature types (3/8, 4/8, 3/4, 4/4, 3/2, 4/2, 12/4) and reinterprets duration values as event counts. Each time signature maps 12 grid positions per bar at different proportional scales. Produces the final Zeitnetz with variable metres and the duration-as-count transformation.

---

## Inputs

The pipeline uses Lachenmann's original *Mouvement* values by default. All three inputs can be overridden via command-line arguments.

| Parameter | Format | Default (*Mouvement*) |
|---|---|---|
| **Pitch row** | 12 integers (0–11) or German names | `1 11 0 8 9 3 6 4 2 10 5 7` |
| **Permutation** | 12 integers (0–11), each appearing once | `1 5 0 6 2 7 11 8 3 10 4 9` |
| **Durations** | 13 integers; first may be negative (initial rest) | `-11 6 9 7 6 6 4 3 10 6 3 1 10` |

Pitch classes follow Lachenmann's convention: 0 = C, 1 = C#, ... 11 = B. German note names are also accepted (`c cis d dis e f fis g gis a ais h`).

## Outputs

| File | Description |
|---|---|
| `zeitnetz_stage1.musicxml` | Stage 1 — Permutation matrix (12 rows of 12 pitch classes) |
| `zeitnetz_stage2.musicxml` | Stage 2 — Zeitnetz Version 1 (12×12 in 3/8) |
| `zeitnetz_stage3_1a_rows.musicxml` | Stage 3a — Family start pitches |
| `zeitnetz_stage3_1b_families.musicxml` | Stage 3b — Family end pitches |
| `zeitnetz_stage3_2.musicxml` | Stage 3 — Combined family overview |
| `zeitnetz_stage4_score.musicxml` | Stage 4 — Full score with all 75 families (uniform 3/8) |
| `zeitnetz_v2.musicxml` | Stage 5 — Full score with variable time signatures |
| `zeitnetz_final.musicxml` | Stage 5 — Duration-as-count transformation |

## Usage

### Requirements

- Python 3.8+
- [music21](https://web.mit.edu/music21/) (`pip install music21`)

### Running

```bash
# Default Lachenmann values — generate all stages
python3 zeitnetz_pipeline.py --export

# Custom inputs
python3 zeitnetz_pipeline.py \
  --pitches "0 1 2 3 4 5 6 7 8 9 10 11" \
  --permutation "1 5 0 6 2 7 11 8 3 10 4 9" \
  --durations "-11 6 9 7 6 6 4 3 10 6 3 1 10" \
  --export
```

The `--export` flag writes all MusicXML files to the current directory.

## Web App

A browser-based version of this generator (with additional features) is available at:

- **v1:** [lachenmann-machine-zeitnetz-generator.netlify.app](https://lachenmann-machine-zeitnetz-generator.netlify.app)
- **v2 (Extended Edition):** [lachenmann-machine-v2.netlify.app](https://lachenmann-machine-v2.netlify.app) — adds targeted family count discovery and custom time signatures

See also: [zeitnetz-generator](https://github.com/MetamusicX/zeitnetz-generator) — the generalised web app repository.

## Context

This tool was developed as part of the ERC Advanced Grant *Posthuman Music: Creative Practices after AI* (2026–2030) at the Orpheus Institute, Ghent. It is the first in a series of "compositional machines" — computational reconstructions of the algorithmic engines underlying major works of post-serial composition.

## References

- Pena, Luís Antunes. *Interlocking Rhythmic Structures in the Music of Helmut Lachenmann — Analysis of the Zeitnetz from Mouvement (– vor der Erstarrung)*. Bachelor thesis, Escola Superior de Música de Lisboa, 2004.
- Cavallotti, Pietro. *Differenzen. Poststrukturalistische Aspekte in der Musik der 1980er Jahre am Beispiel von Helmut Lachenmann, Brian Ferneyhough und Gérard Grisey*. Schliengen: Edition Argus, 2006.
- Lachenmann, Helmut. *Musik als existentielle Erfahrung: Schriften 1966–1995*. Edited by Josef Häusler. Wiesbaden: Breitkopf & Härtel, 1996.

## Author

**Paulo de Assis**
Orpheus Institute, Ghent

## License

MIT
