"""
Zeitnetz Complete Pipeline
Replicating all OpenMusic patches from Pen-Lachenmann-PATCHES.pdf
Based on Luís Antunes Pena's analysis of Lachenmann's Mouvement (– vor der Erstarrung)

Stages
──────
  Stage 1 — Row Generation          (OM patch: "1-erzeugt-reihe")
  Stage 2 — Zeitnetz Version 1      (OM patch: "2 - Zeitnetz Version 1")
  Stage 3 — Klangfamilien           (OM patch: "3 – Klangfamilien")
  Stage 4 — Netz-Familien           (OM patch: "4-Netz-Familien")
  Stage 5 — Final Netz              (OM patch: "5-Netz / Zeitnetz 3")

Usage
──────
  python3 zeitnetz_pipeline.py                    # default Lachenmann values
  python3 zeitnetz_pipeline.py --export           # also write MusicXML per stage
  python3 zeitnetz_pipeline.py --pitches "0 1 2 3 4 5 6 7 8 9 10 11" --export
"""

import argparse
import sys
from music21 import stream, note, meter, clef, bar, metadata
from music21.note import Rest as m21Rest

# ═══════════════════════════════════════════════════════════════════════════════
# SHARED PITCH UTILITIES
# ═══════════════════════════════════════════════════════════════════════════════

GERMAN_TO_PC = {
    "c": 0, "cis": 1, "d": 2, "dis": 3, "e": 4, "f": 5,
    "fis": 6, "g": 7, "gis": 8, "a": 9, "ais": 10, "b": 10,
    "h": 11, "his": 0, "ces": 11, "des": 1, "es": 3, "ges": 6, "as": 8,
}
PC_TO_GERMAN = {
    0: "c", 1: "cis", 2: "d", 3: "dis", 4: "e", 5: "f",
    6: "fis", 7: "g", 8: "gis", 9: "a", 10: "ais", 11: "h",
}
PC_TO_MUSIC21 = {
    0: "C4", 1: "C#4", 2: "D4", 3: "D#4", 4: "E4", 5: "F4",
    6: "F#4", 7: "G4", 8: "G#4", 9: "A4", 10: "A#4", 11: "B4",
}
# OpenMusic midicent: MIDI × 100.  Middle C (C4) = MIDI 60 = 6000 mc.
# All pitch classes assigned to octave 4 by default.
PC_TO_MIDICENT = {pc: (60 + pc) * 100 for pc in range(12)}

def pc_name(pc):
    return PC_TO_GERMAN[pc % 12]

def parse_pitch_input(s):
    tokens = s.strip().split()
    if len(tokens) != 12:
        raise ValueError(f"Pitch row must have 12 values, got {len(tokens)}")
    result = []
    for t in tokens:
        try:
            v = int(t)
            if not 0 <= v <= 11:
                raise ValueError(f"PC {v} out of range")
            result.append(v)
        except ValueError:
            tl = t.lower()
            if tl in GERMAN_TO_PC:
                result.append(GERMAN_TO_PC[tl])
            else:
                raise ValueError(f"Unknown pitch name: '{t}'")
    if set(result) != set(range(12)):
        raise ValueError("Pitch row must contain each class 0–11 exactly once")
    return result

def parse_int_list(s, expected, name):
    tokens = s.strip().split()
    if len(tokens) != expected:
        raise ValueError(f"{name} must have {expected} values, got {len(tokens)}")
    return [int(t) for t in tokens]


# ═══════════════════════════════════════════════════════════════════════════════
# STAGE 1 — ROW GENERATION
# OM patch: "1-erzeugt-reihe"
#
# Sub-patches replicated:
#   permutation  → build_permutation_matrix()
#   ^algo        → (inner step of build_permutation_matrix)
#   Find-Index   → compute_onsets()
#   Chord-Seq-Poly → generate_permutations()
# ═══════════════════════════════════════════════════════════════════════════════

def build_permutation_matrix(perm_pattern):
    """
    Build a 12×12 permutation matrix.
    Row 0 = identity [0..11].
    Row k = Row k-1 re-indexed by perm_pattern  (the '^algo' sub-patch).
    """
    matrix = [list(range(12))]
    for k in range(1, 12):
        prev = matrix[k - 1]
        matrix.append([prev[perm_pattern[i]] for i in range(12)])
    return matrix


def compute_onsets(duration_list):
    """
    Cumulative onset positions in the flattened matrix (the 'Find-Index' patch).
    duration_list[0] may be negative (rest); its absolute value is the first onset.
    Returns 12 integers: the addresses used to look up positions in concat.
    """
    onsets = [abs(duration_list[0])]
    for j in range(1, 12):
        onsets.append(onsets[-1] + duration_list[j])
    return onsets


def derive_rhythm_row(pitch_row, perm_matrix, onsets):
    """
    Flatten the permutation matrix into a 144-element list (concat).
    For each onset[i]: address = concat[onset[i]].
    Place pitch_row[i] at rhythm_row[address].
    Raises ValueError on collision or incomplete fill.
    """
    concat = [val for row in perm_matrix for val in row]
    rhythm_row = [None] * 12
    for i in range(12):
        address = concat[onsets[i]]
        if rhythm_row[address] is not None:
            raise ValueError(
                f"Collision at slot {address}: "
                f"{pc_name(rhythm_row[address])} vs {pc_name(pitch_row[i])}"
            )
        rhythm_row[address] = pitch_row[i]
    if None in rhythm_row:
        missing = [j for j, x in enumerate(rhythm_row) if x is None]
        raise ValueError(f"Rhythm row incomplete — empty slots: {missing}")
    return rhythm_row


def generate_permutations(source_row, perm_matrix):
    """
    Apply all 12 matrix rows to source_row → 12 permutations.
    Replicates the 'Chord-Seq-Poly' output structure.
    """
    return [
        [source_row[perm_matrix[k][i]] for i in range(12)]
        for k in range(12)
    ]


def run_stage1(pitch_row, perm_pattern, duration_list):
    """
    Returns
    -------
    dict with keys:
      pitch_row, rhythm_row, perm_matrix, onsets,
      pitch_perms [12×12], rhythm_perms [12×12]
    """
    matrix       = build_permutation_matrix(perm_pattern)
    onsets       = compute_onsets(duration_list)
    rhythm_row   = derive_rhythm_row(pitch_row, matrix, onsets)
    pitch_perms  = generate_permutations(pitch_row,  matrix)
    rhythm_perms = generate_permutations(rhythm_row, matrix)
    return dict(
        pitch_row    = pitch_row,
        rhythm_row   = rhythm_row,
        perm_matrix  = matrix,
        onsets       = onsets,
        pitch_perms  = pitch_perms,
        rhythm_perms = rhythm_perms,
    )


# ═══════════════════════════════════════════════════════════════════════════════
# STAGE 2 — ZEITNETZ VERSION 1  (circular scanning)
# OM patch: "2 - Zeitnetz Version 1"
#
# Principle
# ─────────
# Concatenate all 12 rhythm-row permutations into one 144-element circular tape.
# Concatenate all 12 pitch-row permutations into a 144-element target sequence.
# A single cursor scans the rhythm tape forward (mod 144) to locate each target
# pitch class in turn.  The step count = duration in 32nd-note units.
#
# flat[0]     = initial rest (scan to find the very first pitch)
# flat[1:13]  = Row 0's 12 inter-note durations
# flat[13:25] = Row 1's 12 durations  …  etc.
#
# Because the tape is 144 elements long (not 12), durations can exceed 12.
# ═══════════════════════════════════════════════════════════════════════════════

def r_limit(value, lo, hi):
    """Clamp value to [lo, hi]. Replicates the 'r-limit' sub-patch."""
    return max(lo, min(hi, value))


def run_stage2(s1):
    """
    Zeitnetz circular scanning on the full 144-element rhythm tape.

    Returns
    -------
    list of 12 dicts, each with:
      voice_index, pitch_perm, rhythm_perm,
      initial_rest_32nds, notes [(pc, dur_32), ...]
    """
    # Build 144-element tapes from all 12 permutations
    rhythm_tape = []
    pitch_targets = []
    for k in range(12):
        rhythm_tape.extend(s1["rhythm_perms"][k])
        pitch_targets.extend(s1["pitch_perms"][k])

    tape_len = len(rhythm_tape)  # 144

    # Scan the rhythm tape for every target pitch class
    cursor = 0
    flat = []
    for i in range(tape_len):
        target_pc = pitch_targets[i]
        count = 0
        scan = cursor
        while True:
            scan = (scan + 1) % tape_len
            count += 1
            if rhythm_tape[scan] == target_pc:
                break
        flat.append(count)
        cursor = scan

    # flat[0] = initial rest; flat[1:] grouped in 12s = per-row durations
    initial_rest = flat[0]

    voices = []
    for k in range(12):
        start = 1 + k * 12
        durs = flat[start : start + 12]

        # Last row may be 1 short (143 remaining values / 12 = 11 r 11).
        # Compute the missing 12th duration with one extra scan.
        if len(durs) < 12:
            target_pc = pitch_targets[(k * 12 + len(durs)) % tape_len]
            count = 0
            scan = cursor
            while True:
                scan = (scan + 1) % tape_len
                count += 1
                if rhythm_tape[scan] == target_pc:
                    break
            durs.append(count)
            cursor = scan

        pitches = s1["pitch_perms"][k]
        notes = [(pitches[i], durs[i]) for i in range(12)]

        voices.append(dict(
            voice_index        = k,
            pitch_perm         = pitches,
            rhythm_perm        = s1["rhythm_perms"][k],
            initial_rest_32nds = initial_rest if k == 0 else 0,
            notes              = notes,
        ))

    return voices


# ═══════════════════════════════════════════════════════════════════════════════
# STAGE 3.1 — KLANGFAMILIEN STARTING POINTS
# OM patch: "3 – Klangfamilien"
#
# Principle
# ─────────
# For each rhythm row i (0–11), read pitch by pitch until finding
# the i-th element of pitch permutation 10 (the control row).
# All pitches read (including the target) form the starting pitches
# of the sound families.  Total across all 12 rows = 75 pitches.
# ═══════════════════════════════════════════════════════════════════════════════

def run_stage3(s1):
    """
    Stage 3.1 — determine the starting pitches of all 75 sound families.

    For each rhythm row i, scan pitch by pitch until the i-th element
    of pitch permutation 10 (control row) is found.  All pitches read
    (including the target) are collected.

    Returns
    -------
    list of 12 dicts, each with:
      row_index : int
      target_pc : int          — the pitch class searched for
      pitches   : list[int]    — pitch classes read (including target)
      rhythm_row: list[int]    — the full rhythm row (for reference)
    """
    control_row = s1["pitch_perms"][10]
    result = []
    for i in range(12):
        rr = s1["rhythm_perms"][i]
        target = control_row[i]
        pitches = []
        for pc in rr:
            pitches.append(pc)
            if pc == target:
                break
        result.append(dict(
            row_index  = i,
            target_pc  = target,
            pitches    = pitches,
            rhythm_row = rr,
        ))
    return result


# ═══════════════════════════════════════════════════════════════════════════════
# STAGE 3.2 — KLANGFAMILIEN END PITCHES
#
# Principle
# ─────────
# Build an "end-pitch tape" by reading the rows in reverse circular order
# starting from Row 6: [6, 5, 4, 3, 2, 1, 0, 11, 10, 9, 8, 7],
# each row's pitches reversed (last to first).
# This produces exactly 75 end-pitches, paired 1-to-1 with the 75 families.
# ═══════════════════════════════════════════════════════════════════════════════

# Circular reading order for family numbering (start pitches)
FAMILY_ROW_ORDER = [7, 8, 9, 10, 11, 0, 1, 2, 3, 4, 5, 6]
# Reverse circular order for end pitches
END_PITCH_ROW_ORDER = [6, 5, 4, 3, 2, 1, 0, 11, 10, 9, 8, 7]


def run_stage3_2(s3_1):
    """
    Stage 3.2 — determine the end pitch of each of the 75 sound families.

    Builds an end-pitch tape by reading rows in reverse circular order
    (6, 5, 4, 3, 2, 1, 0, 11, 10, 9, 8, 7), each row reversed.
    Pairs each family's start pitch with its end pitch.

    Returns
    -------
    list of 75 dicts, each with:
      family   : int (1–75)
      start_pc : int
      end_pc   : int
      row      : int   — row index where the start pitch lives
    """
    by_row = {rd["row_index"]: rd for rd in s3_1}

    # Build start-pitch list in family order
    start_pitches = []
    for ri in FAMILY_ROW_ORDER:
        for pc in by_row[ri]["pitches"]:
            start_pitches.append((ri, pc))

    # Build end-pitch tape
    end_tape = []
    for ri in END_PITCH_ROW_ORDER:
        for pc in reversed(by_row[ri]["pitches"]):
            end_tape.append(pc)

    # Pair them
    families = []
    for i in range(len(start_pitches)):
        row_idx, spc = start_pitches[i]
        families.append(dict(
            family   = i + 1,
            start_pc = spc,
            end_pc   = end_tape[i],
            row      = row_idx,
        ))
    return families


# ═══════════════════════════════════════════════════════════════════════════════
# STAGE 4 — NETZ-FAMILIEN  (network families)
# OM patch: "4-Netz-Familien"
#
# Sub-patches replicated:
#   read-this-poly / Poly-Familie-Start-End → get_family_endpoints()
#   r-limit-midicent (range [6800,7100], tol 200mc) → r_limit_midicent()
#   Count-Between-List / Count-Between-2-Notes      → count_between_notes()
#   Loop-Count-Until-Note-1/2                       → count_until_note()
#   Loop-Dauer (thresholds 25 / 425 / 725)          → loop_dauer_s4()
#   make-poly-familien / make-voice-familien        → make_voice_family()
# ═══════════════════════════════════════════════════════════════════════════════

# Midicent limits from 'Loop-Familie-anfang-end-note' patch [6800, 7100]
MC_LOW      = 6800
MC_HIGH     = 7100
MC_TOLERANCE = 200      # ± 2 semitones tolerance band

# Duration thresholds from 'Loop-Dauer' patch constants
DUR_SHORT   = 25
DUR_MEDIUM  = 425
DUR_LONG    = 725


def r_limit_midicent(mc, lo=MC_LOW, hi=MC_HIGH, tol=MC_TOLERANCE):
    """
    Constrain a midicent value to [lo, hi], with tolerance.
    Values within ±tol of the boundaries pass through unchanged.
    Replicates the 'r-limit-midicent' sub-patch.
    """
    if mc < lo - tol:
        return lo
    if mc > hi + tol:
        return hi
    return mc


def get_family_endpoints(family):
    """
    Return (start_pc, end_pc) of a family.
    Replicates 'Poly-Familie-Start-End' → 'familie-anfang-ende-note'.
    """
    return family[0][0], family[-1][0]


def count_until_note(row, start_pc, target_pc):
    """
    Forward circular step count from start_pc to target_pc in row.
    Replicates 'Loop-Count-Until-Note-1' and 'Count-Until'.
    """
    n   = len(row)
    p1  = row.index(start_pc)
    p2  = row.index(target_pc)
    return (p2 - p1) % n


def count_between_notes(row, pc1, pc2):
    """
    Return (forward_count, backward_count) between two pitch classes.
    Replicates 'Count-Between-2-Notes' which produces count1, count2.
    """
    n   = len(row)
    p1  = row.index(pc1)
    p2  = row.index(pc2)
    fwd = (p2 - p1) % n
    bwd = (p1 - p2) % n
    return fwd, bwd


def loop_dauer_s4(family, scale=100):
    """
    Assign a duration category to each note in a family.
    Replicates 'Loop-Dauer' with threshold constants 25 / 425 / 725.

    Duration in 32nds is scaled to a comparable unit (×100 by default),
    then classified:
      < DUR_SHORT   → category 0  (very short)
      < DUR_MEDIUM  → category 1  (short)
      < DUR_LONG    → category 2  (medium)
      else          → category 3  (long)

    Returns list of dicts with keys: pc, midicent, duration_32nds, dur_category
    """
    result = []
    for pc, dur, *_ in family:
        mc        = PC_TO_MIDICENT[pc]
        mc_c      = r_limit_midicent(mc)
        dur_scaled = dur * scale
        if   dur_scaled < DUR_SHORT:   cat = 0
        elif dur_scaled < DUR_MEDIUM:  cat = 1
        elif dur_scaled < DUR_LONG:    cat = 2
        else:                           cat = 3
        result.append(dict(pc=pc, midicent=mc_c, duration_32nds=dur, dur_category=cat))
    return result


def make_voice_family(fam_idx, processed_notes, pitch_row):
    """
    Build a voice-ready note list for one family.
    Replicates 'make-voice-familien':
      - arithe-per (arithmetic progression through pitch-row indices)
      - nth-list (look up positions)
      - write-voice-from-middur-list (package midi + duration)
    """
    voice_notes = []
    for note_data in processed_notes:
        pc  = note_data["pc"]
        idx = pitch_row.index(pc) if pc in pitch_row else -1
        voice_notes.append({
            **note_data,
            "family_index":     fam_idx,
            "pitch_row_index":  idx,
        })
    return voice_notes


def run_stage4(s3, s1):
    """
    Assign network positions to families, compute inter-family distances
    and duration categories.

    Each voice gains key 'net_families': list of dicts with keys:
      family_index, start_pc, end_pc,
      count_forward, count_backward, inter_distance,
      notes (voice-ready), forward, mirror
    """
    pitch_row = s1["pitch_row"]
    result    = []

    for voice in s3:
        rrow    = voice["rhythm_perm"]
        fams    = voice["families"]
        net_fams = []

        for i, fam_data in enumerate(fams):
            orig               = fam_data["original"]
            start_pc, end_pc   = get_family_endpoints(orig)
            fwd, bwd           = count_between_notes(rrow, start_pc, end_pc)

            # Distance to next family's first note
            if i + 1 < len(fams):
                next_pc      = fams[i + 1]["original"][0][0]
                inter_dist   = count_until_note(rrow, end_pc, next_pc)
            else:
                inter_dist   = 0

            processed    = loop_dauer_s4(orig)
            voice_notes  = make_voice_family(i, processed, pitch_row)

            net_fams.append(dict(
                family_index   = i,
                start_pc       = start_pc,
                end_pc         = end_pc,
                count_forward  = fwd,
                count_backward = bwd,
                inter_distance = inter_dist,
                notes          = voice_notes,
                forward        = fam_data["forward"],
                mirror         = fam_data["mirror"],
            ))

        result.append({**voice, "net_families": net_fams})
    return result


# ═══════════════════════════════════════════════════════════════════════════════
# STAGE 5 — FINAL NETZ
# OM patch: "5-Netz / Zeitnetz 3"
#
# Sub-patches replicated:
#   faktoren / faktoren-from-list / Loop-FAKTOREN → apply_faktoren()
#   r-get / Loop-Count-While-a=b                 → r_get()
#   Loop-Expand-3-Gruppe (ref constant 288)       → expand_3_gruppe()
#   Loop-Compress / Loop-Compress-Seq             → loop_compress_seq()
#   Loop-Correct-Number>1                        → correct_gt1()
#   Loop-Dauer (extended, same thresholds)        → loop_dauer_s5()
#   write-voice-from-middur-list                  → (final note list)
# ═══════════════════════════════════════════════════════════════════════════════

# Reference constant from 'Loop-Expand-3-Gruppe' (patch value: 288 midicent)
# Used as a transposition step when expanding groups of 3 notes.
EXPAND_REF_MC = 288


def r_get(row, start_idx=0):
    """
    Count a run of equal elements starting at start_idx.
    Replicates 'r-get' + 'Loop-Count-While-a=b' (count while a == b).
    Returns run length (minimum 1).
    """
    if not row or start_idx >= len(row):
        return 1
    target = row[start_idx]
    count  = 0
    for v in row[start_idx:]:
        if v == target:
            count += 1
        else:
            break
    return max(1, count)


def expand_3_gruppe(group):
    """
    Expand a group of 3 notes across a wider pitch space.
    Replicates 'Loop-Expand-3-Gruppe': uses nth with midicent ref 288.
    Each note is offset by (EXPAND_REF_MC / 100) semitones × its position index.
    """
    expanded = []
    step_semitones = EXPAND_REF_MC // 100   # 288mc ≈ 3 semitones
    for i, (pc, dur) in enumerate(group):
        new_pc = (pc + i * step_semitones) % 12
        expanded.append((new_pc, dur))
    return expanded


def apply_faktoren(note_pairs):
    """
    Scan a list of (pc, dur) pairs.
    Replicates 'faktoren' patch logic (cross-product with conditionals):
      - If two or more consecutive notes share the same pitch class → compress
        (combine their durations into one note: first × second).
      - Groups of exactly 3 distinct notes → expand via expand_3_gruppe.
      - Otherwise pass through unchanged.
    Also replicates 'Loop-FAKTOREN' (the outer loop) and
    'faktoren-from-list' (input unpacking).
    """
    result = []
    i = 0
    while i < len(note_pairs):
        pc, dur = note_pairs[i]

        # Count run of same pc (Loop-Count-While-a=b)
        run = r_get([p for p, _ in note_pairs], start_idx=i)

        if run >= 2:
            # Compress: Loop-Compress → first × second (sum durations here)
            combined_dur = sum(note_pairs[i + j][1] for j in range(run))
            result.append((pc, combined_dur))
            i += run
        elif i + 2 < len(note_pairs):
            # Peek at next 3 notes for possible group-of-3 expansion
            group = note_pairs[i:i + 3]
            distinct_pcs = {p for p, _ in group}
            if len(distinct_pcs) == 3:
                result.extend(expand_3_gruppe(group))
                i += 3
            else:
                result.append((pc, dur))
                i += 1
        else:
            result.append((pc, dur))
            i += 1

    return result


def loop_compress_seq(sequence):
    """
    Compress a list of (a, b) pairs by multiplying each pair.
    Replicates 'Loop-Compress-Seq' → 'Loop-Compress' (LISP first × second).
    """
    return [a * b for a, b in sequence]


def correct_gt1(value):
    """
    Ensure value ≥ 1.
    Replicates 'Loop-Correct-Number>1' (omif + create-list → flat).
    """
    return value if value >= 1 else 1


def loop_dauer_s5(notes, dur_32_to_unit=50):
    """
    Extended duration loop for Stage 5.
    Replicates the longer 'Loop-Dauer' in "5 - Zeitnetz 3" (Bild 52):
    same DUR_SHORT/MEDIUM/LONG thresholds but adds:
      - correct_gt1 on every duration
      - midicent constraint via r_limit_midicent
      - 'duration_ms' approximation (1 32nd ≈ dur_32_to_unit ms)

    Returns enriched note dicts adding keys: duration_ms, duration_32nds_corrected
    """
    result = []
    for nd in notes:
        dur_raw  = nd["duration_32nds"]
        dur_corr = correct_gt1(dur_raw)
        dur_ms   = dur_corr * dur_32_to_unit

        # Clamp to [DUR_SHORT, DUR_LONG]
        dur_ms = r_limit(dur_ms, DUR_SHORT, DUR_LONG)
        dur_ms = correct_gt1(dur_ms)

        mc_c = r_limit_midicent(nd["midicent"])

        result.append({
            **nd,
            "midicent":               mc_c,
            "duration_32nds_corrected": dur_corr,
            "duration_ms":            dur_ms,
        })
    return result


def run_stage5(s4, s1):
    """
    Apply faktoren (expand/compress), correct durations,
    and produce final voice objects ready for export.

    Each voice gains key 'final_families': list of dicts adding:
      'final_notes' — fully processed note list (from loop_dauer_s5)
    """
    pitch_row = s1["pitch_row"]
    result    = []

    for voice in s4:
        final_fams = []

        for fam_data in voice["net_families"]:
            # Extract (pc, dur) pairs from Stage-4 notes
            pairs = [(n["pc"], n["duration_32nds"]) for n in fam_data["notes"]]

            # Apply faktoren (expand/compress)
            processed = apply_faktoren(pairs)

            # Correct all durations to ≥ 1
            corrected = [(pc, correct_gt1(dur)) for pc, dur in processed]

            # Build enriched note dicts
            enriched = [
                dict(pc=pc, midicent=PC_TO_MIDICENT[pc], duration_32nds=dur)
                for pc, dur in corrected
            ]

            # Extended Loop-Dauer
            final_notes = loop_dauer_s5(enriched)

            final_fams.append({**fam_data, "final_notes": final_notes})

        result.append({**voice, "final_families": final_fams})
    return result


# ═══════════════════════════════════════════════════════════════════════════════
# MUSICXML EXPORT (one file per stage)
# ═══════════════════════════════════════════════════════════════════════════════

def _make_score(title):
    sc = stream.Score()
    sc.metadata = metadata.Metadata()
    sc.metadata.title = title
    sc.metadata.composer = "after Lachenmann / Mouvement (– vor der Erstarrung)"
    return sc


def export_stage1(s1, filename="zeitnetz_stage1.musicxml"):
    """
    Stage 1 MusicXML — layout matching Pena's analysis diagram.

    12 parts (Row 0 – Row 11), each with 2 measures:
      Measure 1 = pitch permutation   (header: "Pitch row")
      Measure 2 = rhythm permutation   (header: "Rhythm row")
    Lyrics = sequential note index (0–143).
    A system break between the two measures forces Sibelius to render
    them as two separate systems (left = pitch, right = rhythm).
    """
    from music21 import expressions, layout

    sc = _make_score("Stage 1 — Pitch & Rhythm Row Permutations")
    ts = meter.TimeSignature("12/4")

    for k in range(12):
        part = stream.Part()
        part.partName = f"Row {k}"

        # ── Measure 1: pitch permutation ─────────────────────────────────
        m1 = stream.Measure(number=1)
        m1.append(ts)
        m1.append(clef.TrebleClef())

        if k == 0:
            te = expressions.TextExpression("Pitch row")
            te.placement = "above"
            te.style.fontStyle = "bold"
            te.style.fontSize = 14
            m1.insert(0, te)

        for i, pc in enumerate(s1["pitch_perms"][k]):
            n = note.Note(PC_TO_MUSIC21[pc])
            n.quarterLength = 1.0
            n.lyric = str(k * 12 + i)
            m1.append(n)

        m1.rightBarline = bar.Barline("double")
        part.append(m1)

        # ── Measure 2: rhythm permutation ────────────────────────────────
        m2 = stream.Measure(number=2)
        m2.append(ts)
        m2.append(clef.TrebleClef())

        # Force a new system so pitch & rhythm appear on separate lines
        sl = layout.SystemLayout(isNew=True)
        m2.insert(0, sl)

        if k == 0:
            te2 = expressions.TextExpression("Rhythm row")
            te2.placement = "above"
            te2.style.fontStyle = "bold"
            te2.style.fontSize = 14
            m2.insert(0, te2)

        for i, pc in enumerate(s1["rhythm_perms"][k]):
            n = note.Note(PC_TO_MUSIC21[pc])
            n.quarterLength = 1.0
            n.lyric = str(k * 12 + i)
            m2.append(n)

        m2.rightBarline = bar.Barline("final")
        part.append(m2)

        sc.insert(0, part)

    sc.write("musicxml", fp=filename)
    return filename


def export_stage2(s2, filename="zeitnetz_stage2.musicxml"):
    """
    Stage 2 MusicXML — time-scaffold score.

    Single part.  All 12 rows concatenated horizontally.
    Time signature 3/8 (unit = thirty-second note).
    Each pitch = one thirty-second note; remaining duration filled with rests.
    Durations come from the 144-element circular scanning algorithm.
    Text expression "Row 0"–"Row 11" marks the start of each row.
    Each pitch carries its duration value as a lyric.

    All positions computed with INTEGER arithmetic (32nd-note units)
    to guarantee exact placement.
    """
    from music21 import expressions
    from fractions import Fraction

    sc = _make_score("Stage 2 — Zeitnetz Version 1 (Circular Scanning)")

    # ── Collect all events as (absolute_pos_in_32nds, element) ────────
    #    Using integers avoids any floating-point drift.
    events = []       # (pos_32: int, music21_element)
    row_starts = {}   # pos_32 → row index (for text labels)

    pos = 0  # absolute position in 32nd-note units (integer)

    for v in s2:
        k = v["voice_index"]
        row_starts[pos] = k

        # Initial rest — only for Row 0
        ir = v["initial_rest_32nds"]
        if ir > 0:
            r = m21Rest()
            r.quarterLength = Fraction(ir, 8)
            r.lyric = str(-ir)
            events.append((pos, r))
            pos += ir

        # 12 pitches with scanning durations
        for pc, dur_32 in v["notes"]:
            # Pitched 32nd note
            n = note.Note(PC_TO_MUSIC21[pc])
            n.quarterLength = Fraction(1, 8)
            n.lyric = str(dur_32)
            events.append((pos, n))
            pos += 1

            # Remaining duration as rest
            rest_32 = dur_32 - 1
            if rest_32 > 0:
                r = m21Rest()
                r.quarterLength = Fraction(rest_32, 8)
                events.append((pos, r))
                pos += rest_32

    # ── Build measures manually (3/8 = 12 thirty-second notes each) ───
    BAR = 12  # thirty-second notes per bar
    total_32 = pos
    n_bars = (total_32 + BAR - 1) // BAR  # ceiling division

    part = stream.Part()
    part.partName = "Zeitnetz V1"

    ts = meter.TimeSignature("3/8")

    for b in range(n_bars):
        m = stream.Measure(number=b + 1)
        if b == 0:
            m.append(ts)
            m.append(clef.TrebleClef())

        bar_start = b * BAR
        bar_end = bar_start + BAR

        # Insert row labels that fall in this bar
        for rs_pos, rs_k in row_starts.items():
            if bar_start <= rs_pos < bar_end:
                te = expressions.TextExpression(f"Row {rs_k}")
                te.placement = "above"
                m.insert(Fraction(rs_pos - bar_start, 8), te)

        # Collect events that START in this bar
        bar_events = [(p, e) for p, e in events if bar_start <= p < bar_end]

        # Fill the bar: walk through 32nd positions, placing events
        # and filling gaps with rests
        filled_to = bar_start  # how far we've filled (in absolute 32nds)

        for ev_pos, ev_elem in bar_events:
            # Gap before this event?
            if ev_pos > filled_to:
                gap = ev_pos - filled_to
                gr = m21Rest()
                gr.quarterLength = Fraction(gap, 8)
                m.insert(Fraction(filled_to - bar_start, 8), gr)
                filled_to = ev_pos

            # How much of this event fits in the current bar?
            ev_end = ev_pos + int(ev_elem.quarterLength * 8)
            fits = min(ev_end, bar_end) - ev_pos

            if fits == int(ev_elem.quarterLength * 8):
                # Entire event fits in this bar
                m.insert(Fraction(ev_pos - bar_start, 8), ev_elem)
            else:
                # Event spans into next bar — split it
                if ev_elem.isNote:
                    # Note portion in this bar
                    n_copy = note.Note(ev_elem.pitch)
                    n_copy.quarterLength = Fraction(fits, 8)
                    n_copy.lyric = ev_elem.lyric
                    m.insert(Fraction(ev_pos - bar_start, 8), n_copy)
                else:
                    # Rest portion in this bar
                    r_copy = m21Rest()
                    r_copy.quarterLength = Fraction(fits, 8)
                    m.insert(Fraction(ev_pos - bar_start, 8), r_copy)

                # Remainder goes into future bars as a new event
                remainder = int(ev_elem.quarterLength * 8) - fits
                if remainder > 0:
                    if ev_elem.isNote:
                        rem_elem = m21Rest()  # tied remainder becomes rest
                    else:
                        rem_elem = m21Rest()
                    rem_elem.quarterLength = Fraction(remainder, 8)
                    events.append((bar_end, rem_elem))
                    events.sort(key=lambda x: x[0])

            filled_to = ev_pos + fits

        # Fill remaining bar space with rest
        if filled_to < bar_end and filled_to < total_32:
            gap = min(bar_end, total_32) - filled_to
            if gap > 0:
                gr = m21Rest()
                gr.quarterLength = Fraction(gap, 8)
                m.insert(Fraction(filled_to - bar_start, 8), gr)

        part.append(m)

    # Final barline
    measures = part.getElementsByClass(stream.Measure)
    if measures:
        measures[-1].rightBarline = bar.Barline("final")

    sc.insert(0, part)
    sc.write("musicxml", fp=filename)
    return filename


def export_stage3(s3):
    """
    Stage 3.1 — Two MusicXML files:
      (a) Original row order (Row 0–11), pitch names as lyrics.
      (b) Reordered (Row 7, 8, …, 6), family numbers (1–75) as lyrics.
    Returns tuple of two filenames.
    """
    by_row = {rd["row_index"]: rd for rd in s3}
    ROW_ORDER = [7, 8, 9, 10, 11, 0, 1, 2, 3, 4, 5, 6]

    # Assign family numbers in circular reading order
    family_numbers = {}
    fam = 1
    for ri in ROW_ORDER:
        for j in range(len(by_row[ri]["pitches"])):
            family_numbers[(ri, j)] = fam
            fam += 1

    # ── File A: original order (Row 0–11), pitch names ───────────────────
    fn_a = "zeitnetz_stage3_1a_rows.musicxml"
    sc_a = _make_score("Stage 3.1a — Rhythm Rows (original order)")
    for ri in range(12):
        pitches = by_row[ri]["pitches"]
        part = stream.Part()
        part.partName = f"Row {ri}"
        n_notes = len(pitches)
        ts = meter.TimeSignature(f"{n_notes}/4")
        m = stream.Measure(number=1)
        m.append(ts)
        m.append(clef.TrebleClef())
        for pc in pitches:
            n = note.Note(PC_TO_MUSIC21[pc % 12])
            n.quarterLength = 1.0
            n.lyric = pc_name(pc % 12)
            m.append(n)
        m.rightBarline = bar.Barline("final")
        part.append(m)
        sc_a.append(part)
    sc_a.write("musicxml", fp=fn_a)

    # ── File B: reordered (Row 7, 8, …, 6), family numbers ──────────────
    fn_b = "zeitnetz_stage3_1b_families.musicxml"
    sc_b = _make_score("Stage 3.1b — Family Numbering (1–75)")
    for ri in ROW_ORDER:
        pitches = by_row[ri]["pitches"]
        part = stream.Part()
        part.partName = f"Row {ri}"
        n_notes = len(pitches)
        ts = meter.TimeSignature(f"{n_notes}/4")
        m = stream.Measure(number=1)
        m.append(ts)
        m.append(clef.TrebleClef())
        for j, pc in enumerate(pitches):
            n = note.Note(PC_TO_MUSIC21[pc % 12])
            n.quarterLength = 1.0
            n.lyric = str(family_numbers[(ri, j)])
            m.append(n)
        m.rightBarline = bar.Barline("final")
        part.append(m)
        sc_b.append(part)
    sc_b.write("musicxml", fp=fn_b)

    return fn_a, fn_b


def export_stage3_2(s3_2, filename="zeitnetz_stage3_2.musicxml"):
    """
    Stage 3.2 — 75 bi-chords (start + end pitch of each sound family).
    Single staff, 10/4 time, lower note = start pitch, upper note = end pitch.
    Family number as lyric.
    """
    from music21 import chord as m21chord

    sc = _make_score("Stage 3.2 — Klangfamilien (Start + End)")
    part = stream.Part()
    part.partName = "Families"

    measure_num = 1
    idx = 0
    while idx < len(s3_2):
        # 10 chords per bar (10/4 time), last bar may be shorter
        batch = s3_2[idx : idx + 10]
        n = len(batch)
        ts = meter.TimeSignature(f"{n}/4")
        m = stream.Measure(number=measure_num)
        m.append(ts)
        if measure_num == 1:
            m.append(clef.TrebleClef())

        for fam in batch:
            spc = fam["start_pc"]
            epc = fam["end_pc"]
            # Lower = start, upper = end; put start in octave 4, end in octave 5
            # If they are the same pc, use octave 4 and 5
            s_pitch = PC_TO_MUSIC21[spc % 12]             # e.g. "C#4"
            e_pitch = PC_TO_MUSIC21[epc % 12].replace("4", "5")  # e.g. "D5"
            c = m21chord.Chord([s_pitch, e_pitch])
            c.quarterLength = 1.0
            c.lyric = str(fam["family"])
            m.append(c)

        if idx + 10 >= len(s3_2):
            m.rightBarline = bar.Barline("final")
        part.append(m)
        measure_num += 1
        idx += 10

    sc.append(part)
    sc.write("musicxml", fp=filename)
    return filename


def export_stage4_score(s2, s3_2, filename="zeitnetz_stage4_score.musicxml"):
    """
    Stage 4 — Full Score: Zeitnetz (top staff) + 12 family staves below.

    Time signature 3/8 (unit = thirty-second note).
    The Zeitnetz is extended cyclically: after the original 12 rows (0–11),
    rows repeat as 0b, 1b, 2b… until all 75 families have activated and
    deactivated.  Durations are preserved from the original rows.

    Family activation — sequential scan:
      A single left-to-right scan of the (extended) Zeitnetz events.
      Families queue in order 1→75.  The next queued family activates
      when its start_pc matches the current event.  Every active family
      receives every event.  A family deactivates (inclusive) when its
      end_pc matches the current event.
      Special rule: families whose start_pc == end_pc (F8, F12, F34, F42,
      F45, F64, F68) deactivate on the NEXT occurrence of that pitch,
      not the activating event itself.

    Staff assignment — round-robin:
      Family N → staff ((N-1) % 12) + 1.

    All positions computed with integer arithmetic (32nd-note units).
    """
    from fractions import Fraction
    from music21 import expressions

    sc = _make_score("Full Score — Zeitnetz + Sound Families")

    # ── 1. Build original 12 rows as templates ─────────────────────────
    row_templates = []   # [(voice_index, initial_rest, [(pc, dur), ...])]
    for v in s2:
        row_templates.append((
            v["voice_index"],
            v["initial_rest_32nds"],
            list(v["notes"]),
        ))

    # ── 2. Flatten original Zeitnetz + cyclic extensions ───────────────
    zn_events = []          # (pos_32, pc, dur_32, row_label)
    row_start_pos = {}      # row_label → pos_32 of its first note

    # Pass 0: original rows (with initial rests)
    pos = 0
    for vi, ir, notes in row_templates:
        if ir > 0:
            pos += ir
        label = f"Row {vi}"
        row_start_pos[label] = pos
        for pc, dur_32 in notes:
            zn_events.append((pos, pc, dur_32, label))
            pos += dur_32

    # Cyclic extensions: keep adding rows until all 75 families done.
    # We do a preliminary scan to know how many cycles we need.
    # Safety: cap at 10 full cycles (120 extra rows) to avoid infinite loop.
    MAX_CYCLES = 10
    cycle = 1
    all_done = False
    while cycle <= MAX_CYCLES and not all_done:
        cycle_start_len = len(zn_events)
        suffix = chr(ord('a') + cycle - 1)  # b, c, d, ...
        for vi, _ir, notes in row_templates:
            # No initial rest on cyclic repeats — continuous
            label = f"Row {vi}{suffix}"
            row_start_pos[label] = pos
            for pc, dur_32 in notes:
                zn_events.append((pos, pc, dur_32, label))
                pos += dur_32

        # Test if all 75 families can finish with events so far
        all_done = _test_all_families_done(zn_events, s3_2)
        cycle += 1

    total_32 = pos
    n_cycles = cycle - 1

    # ── 3. Sequential scan — family activation ─────────────────────────
    family_queue = list(s3_2)
    active = []
    fam_events = {f["family"]: [] for f in s3_2}
    # Track event count per active family for same-pc deactivation rule
    fam_evt_count = {}

    for ev_pos, ev_pc, ev_dur, ev_label in zn_events:
        # activate next queued family if its start_pc matches
        if family_queue and family_queue[0]["start_pc"] == ev_pc:
            f = family_queue.pop(0)
            active.append(f)
            fam_evt_count[f["family"]] = 0

        # every active family receives this event
        for f in active:
            fam_events[f["family"]].append((ev_pos, ev_pc))
            fam_evt_count[f["family"]] += 1

        # deactivate families whose end_pc matches
        # Special: if start_pc == end_pc, only deactivate after ≥2 events
        new_active = []
        for f in active:
            if f["end_pc"] == ev_pc:
                if f["start_pc"] == f["end_pc"]:
                    # same start/end: need at least 2 events
                    if fam_evt_count[f["family"]] >= 2:
                        continue  # deactivate
                    else:
                        new_active.append(f)  # keep active
                else:
                    continue  # deactivate (normal case)
            else:
                new_active.append(f)  # end_pc doesn't match, keep
        active = new_active

        # Stop early if all families done
        if not family_queue and not active:
            break

    activated_fams = [f for f in s3_2 if len(fam_events[f["family"]]) > 0]
    activated = len(activated_fams)

    # ── 4. Round-robin staff assignment ─────────────────────────────────
    staff_assign = {}
    for f in activated_fams:
        fn = f["family"]
        staff_assign[fn] = ((fn - 1) % 12) + 1

    # ── 5. Build per-staff note lists ───────────────────────────────────
    staff_notes  = {s: [] for s in range(1, 13)}
    staff_labels = {s: {} for s in range(1, 13)}

    for f in activated_fams:
        fn = f["family"]
        s = staff_assign[fn]
        evts = fam_events[fn]
        for i, (p, pc) in enumerate(evts):
            staff_notes[s].append((p, pc))
            if i == 0:
                staff_labels[s][p] = f"F{fn}"

    for s in staff_notes:
        staff_notes[s].sort()

    # ── 6. Build measures (shared helper) ───────────────────────────────
    BAR    = 12
    n_bars = (total_32 + BAR - 1) // BAR

    def _build_part(name, notes_sorted, labels_dict=None, lyric_fn=None):
        part = stream.Part()
        part.partName = name
        ni = 0

        for b in range(n_bars):
            m = stream.Measure(number=b + 1)
            if b == 0:
                m.append(meter.TimeSignature("3/8"))
                m.append(clef.TrebleClef())

            bs = b * BAR
            be = bs + BAR

            if labels_dict:
                for lp, lt in labels_dict.items():
                    if bs <= lp < be:
                        te = expressions.TextExpression(lt)
                        te.placement = "above"
                        m.insert(Fraction(lp - bs, 8), te)

            cur = bs
            while cur < be:
                if ni < len(notes_sorted) and notes_sorted[ni][0] == cur:
                    entry = notes_sorted[ni]
                    n = note.Note(PC_TO_MUSIC21[entry[1]])
                    n.quarterLength = Fraction(1, 8)
                    if lyric_fn:
                        lyr = lyric_fn(entry)
                        if lyr is not None:
                            n.lyric = lyr
                    m.insert(Fraction(cur - bs, 8), n)
                    cur += 1
                    ni += 1
                else:
                    nxt = notes_sorted[ni][0] if ni < len(notes_sorted) else be
                    gap = min(nxt, be) - cur
                    if gap > 0:
                        r = m21Rest()
                        r.quarterLength = Fraction(gap, 8)
                        m.insert(Fraction(cur - bs, 8), r)
                        cur += gap

            part.append(m)

        ms = part.getElementsByClass(stream.Measure)
        if ms:
            ms[-1].rightBarline = bar.Barline("final")
        return part

    # ── Zeitnetz part (top staff) ───────────────────────────────────────
    zn_labels  = {pos: label for label, pos in row_start_pos.items()}
    zn_sorted  = [(p, pc, dur) for p, pc, dur, _ in zn_events]
    zn_part    = _build_part("Zeitnetz", zn_sorted, zn_labels,
                             lyric_fn=lambda e: str(e[2]))
    sc.append(zn_part)

    # ── 12 family staves ───────────────────────────────────────────────
    # Build position → duration lookup from Zeitnetz events
    pos_to_dur = {p: dur for p, pc, dur, _ in zn_events}
    n_used = sum(1 for s in range(1, 13) if staff_notes[s])
    for s in range(1, 13):
        p = _build_part(f"Staff {s}", staff_notes[s], staff_labels[s],
                        lyric_fn=lambda e: str(pos_to_dur.get(e[0], "")))
        sc.append(p)

    sc.write("musicxml", fp=filename)
    print(f"  13 staves ({n_used} used), {n_bars} bars, {total_32} thirty-second notes")
    print(f"  Cyclic extensions: {n_cycles} cycle(s) beyond original 12 rows")
    print(f"  Families activated: {activated}/75 (sequential scan)")
    if family_queue:
        nxt = family_queue[0]
        print(f"  ⚠ Unactivated: F{nxt['family']} "
              f"(needs {pc_name(nxt['start_pc'])})")

    # Summary per staff
    for s in range(1, 13):
        fams = sorted([fn for fn, st in staff_assign.items() if st == s],
                      key=lambda fn: fam_events[fn][0][0])
        if fams:
            print(f"    Staff {s:2d}: {', '.join(f'F{fn}' for fn in fams)}")

    # Family activation summary
    print("\n  Family activation positions:")
    for f in activated_fams:
        fn = f["family"]
        evts = fam_events[fn]
        start_pos = evts[0][0]
        end_pos = evts[-1][0]
        print(f"    F{fn:2d}: {pc_name(f['start_pc']):4s}@{start_pos} → "
              f"{pc_name(f['end_pc']):4s}@{end_pos}  ({len(evts)} events)")

    return filename


def _test_all_families_done(zn_events, s3_2):
    """Quick test: can all 75 families activate and deactivate?"""
    family_queue = list(s3_2)
    active = []
    fam_evt_count = {}

    for ev_pos, ev_pc, ev_dur, ev_label in zn_events:
        if family_queue and family_queue[0]["start_pc"] == ev_pc:
            f = family_queue.pop(0)
            active.append(f)
            fam_evt_count[f["family"]] = 0

        for f in active:
            fam_evt_count[f["family"]] += 1

        new_active = []
        for f in active:
            if f["end_pc"] == ev_pc:
                if f["start_pc"] == f["end_pc"]:
                    if fam_evt_count[f["family"]] >= 2:
                        continue
                    else:
                        new_active.append(f)
                else:
                    continue
            else:
                new_active.append(f)
        active = new_active

        if not family_queue and not active:
            return True

    return False


def export_zeitnetz_final(s2, s3_2, filename="zeitnetz_final.musicxml"):
    """
    Zeitnetz Final — Duration-as-count transformation.

    Each family's note-durations from Stage 4 become EVENT COUNTS in the
    Zeitnetz time-grid.  For example, a duration of 6 means: the next
    family entry appears 6 Zeitnetz events later.  Pitches are taken from
    the Zeitnetz event each entry lands on (not from Stage 4).

    The Zeitnetz is extended cyclically as many times as needed.
    Staff assignment uses a greedy interval scheduler to minimise staves.
    Time signatures follow the V2 cyclic sequence.
    """
    from fractions import Fraction
    from music21 import expressions, duration as m21duration

    sc = _make_score("Zeitnetz Final — Duration as Count")

    # ── Time-signature configuration (same as V2) ────────────────────
    TS_SEQ = [
        7,6,6,5,5,5,4,4,4,4,3,3,3,3,3,2,2,2,2,2,2,
        1,1,1,1,1,1,1,1,1,1,1,1,1,1,
        2,2,2,2,2,2,2,3,3,3,3,3,3,3,4,4,4,4,4,4,4,
        5,5,5,5,5,5,5,6,6,6,6,6,6,6,
        7,7,7,7,7,7,7,7,7,7,7,7,7,7,
        6,6,6,6,6,6,5,5,5,5,5,4,4,4,4,3,3,3,2,2,1,
    ]

    TS_DEFS = {
        1: {"ts": "3/8",  "unit_ql": Fraction(1, 8),  "is_tuplet": False},
        2: {"ts": "4/8",  "unit_ql": Fraction(1, 6),  "is_tuplet": True,
            "tup_written": "16th",    "tup_actual": 3, "tup_normal": 2},
        3: {"ts": "3/4",  "unit_ql": Fraction(1, 4),  "is_tuplet": False},
        4: {"ts": "4/4",  "unit_ql": Fraction(1, 3),  "is_tuplet": True,
            "tup_written": "eighth",  "tup_actual": 3, "tup_normal": 2},
        5: {"ts": "3/2",  "unit_ql": Fraction(1, 2),  "is_tuplet": False},
        6: {"ts": "4/2",  "unit_ql": Fraction(2, 3),  "is_tuplet": True,
            "tup_written": "quarter", "tup_actual": 3, "tup_normal": 2},
        7: {"ts": "12/4", "unit_ql": Fraction(1, 1),  "is_tuplet": False},
    }

    # ── 1. Build row templates ───────────────────────────────────────
    row_templates = []
    for v in s2:
        row_templates.append((
            v["voice_index"],
            v["initial_rest_32nds"],
            list(v["notes"]),
        ))

    # ── Helper: build Zeitnetz with N extra cycles ───────────────────
    def _build_zn(n_extra):
        evts = []
        rsp  = {}
        p = 0
        for vi, ir, notes in row_templates:
            if ir > 0:
                p += ir
            label = f"Row {vi}"
            rsp[label] = p
            for pc, dur_32 in notes:
                evts.append((p, pc, dur_32, label))
                p += dur_32
        for cyc in range(1, n_extra + 1):
            suffix = chr(ord('a') + cyc - 1)
            for vi, _ir, notes in row_templates:
                label = f"Row {vi}{suffix}"
                rsp[label] = p
                for pc, dur_32 in notes:
                    evts.append((p, pc, dur_32, label))
                    p += dur_32
        return evts, rsp, p

    # ── 2. Stage 4 scan — family entries with indices & durations ────
    def _stage4_scan(zn_events):
        fq = list(s3_2)
        active = []
        fe = {f["family"]: [] for f in s3_2}
        fec = {}
        for zi, (ep, epc, ed, el) in enumerate(zn_events):
            if fq and fq[0]["start_pc"] == epc:
                f = fq.pop(0)
                active.append(f)
                fec[f["family"]] = 0
            for f in active:
                fe[f["family"]].append((zi, ep, epc, ed))
                fec[f["family"]] += 1
            na = []
            for f in active:
                if f["end_pc"] == epc:
                    if f["start_pc"] == f["end_pc"]:
                        if fec[f["family"]] >= 2:
                            continue
                        else:
                            na.append(f)
                    else:
                        continue
                else:
                    na.append(f)
            active = na
            if not fq and not active:
                break
        return fe

    # ── 3. Initial Zeitnetz + scan ───────────────────────────────────
    zn_events, row_start_pos, total_32 = _build_zn(3)
    fam_entries = _stage4_scan(zn_events)

    # ── 4. Compute max Zeitnetz event index needed ───────────────────
    max_idx_needed = 0
    for f in s3_2:
        fn = f["family"]
        entries = fam_entries[fn]
        if len(entries) < 2:
            continue
        start_idx = entries[0][0]
        durations = [e[3] for e in entries]
        # N entries → N-1 forward jumps (last duration not used)
        idx = start_idx + sum(durations[:-1])
        max_idx_needed = max(max_idx_needed, idx)

    # ── 5. Extend Zeitnetz until we have enough events ───────────────
    n_extra = 3
    while max_idx_needed >= len(zn_events):
        n_extra += 5
        zn_events, row_start_pos, total_32 = _build_zn(n_extra)

    print(f"  Zeitnetz Final: {len(zn_events)} events "
          f"({n_extra} extra cycles), max index needed = {max_idx_needed}")

    # ── 6. Compute final family positions ─────────────────────────────
    final_fam = {}         # family → [(pos, pc, dur), ...]
    max_final_pos = 0

    for f in s3_2:
        fn = f["family"]
        entries = fam_entries[fn]
        if not entries:
            continue
        start_idx = entries[0][0]
        durations = [e[3] for e in entries]

        result = []
        idx = start_idx
        for i in range(len(entries)):
            if idx >= len(zn_events):
                print(f"  ⚠ F{fn} entry {i}: index {idx} out of range")
                break
            ev_pos, ev_pc, ev_dur, _ = zn_events[idx]
            result.append((ev_pos, ev_pc, ev_dur))
            max_final_pos = max(max_final_pos, ev_pos)
            if i < len(entries) - 1:
                idx += durations[i]
        final_fam[fn] = result

    # ── 7. Greedy staff assignment (minimise staves) ──────────────────
    fam_spans = []
    for fn, entries in final_fam.items():
        if entries:
            fam_spans.append((fn, entries[0][0], entries[-1][0]))
    fam_spans.sort(key=lambda x: x[1])   # sort by start position

    staff_ends   = []   # end position of last family on each staff
    staff_assign = {}
    for fn, start, end in fam_spans:
        placed = False
        for si in range(len(staff_ends)):
            if start > staff_ends[si]:
                staff_ends[si] = end
                staff_assign[fn] = si + 1
                placed = True
                break
        if not placed:
            staff_ends.append(end)
            staff_assign[fn] = len(staff_ends)

    n_staves = len(staff_ends)

    # ── 8. Build per-staff note lists ─────────────────────────────────
    BAR = 12
    n_bars = (max_final_pos + BAR) // BAR

    staff_notes  = {s: [] for s in range(1, n_staves + 1)}
    staff_labels = {s: {} for s in range(1, n_staves + 1)}

    for fn, entries in final_fam.items():
        if not entries:
            continue
        s = staff_assign[fn]
        for i, (pos, pc, dur) in enumerate(entries):
            # (pos, pc, dur, family_number, event_index_1based)
            staff_notes[s].append((pos, pc, dur, fn, i + 1))
            if i == 0:
                staff_labels[s][pos] = f"F{fn}"
    for s in staff_notes:
        staff_notes[s].sort()

    # ── 9. Build V2 measures ──────────────────────────────────────────
    def _build_part_final(name, notes_sorted, labels_dict=None, lyric_fn=None):
        part = stream.Part()
        part.partName = name
        ni = 0
        prev_ts_str = None

        for b in range(n_bars):
            ts_idx  = TS_SEQ[b % len(TS_SEQ)]
            td      = TS_DEFS[ts_idx]
            ts_str  = td["ts"]
            unit_ql = td["unit_ql"]
            is_tup  = td["is_tuplet"]

            m = stream.Measure(number=b + 1)
            if ts_str != prev_ts_str:
                m.append(meter.TimeSignature(ts_str))
                if prev_ts_str is None:
                    m.append(clef.TrebleClef())
                prev_ts_str = ts_str

            bs = b * BAR

            if labels_dict:
                for lp, lt in labels_dict.items():
                    if bs <= lp < bs + BAR:
                        te = expressions.TextExpression(lt)
                        te.placement = "above"
                        m.insert((lp - bs) * unit_ql, te)

            slots = []
            for g in range(BAR):
                gpos = bs + g
                if ni < len(notes_sorted) and notes_sorted[ni][0] == gpos:
                    slots.append(notes_sorted[ni])
                    ni += 1
                else:
                    slots.append(None)

            offset = Fraction(0)

            if not is_tup:
                i = 0
                while i < BAR:
                    if slots[i] is not None:
                        entry = slots[i]
                        n = note.Note(PC_TO_MUSIC21[entry[1]])
                        n.quarterLength = unit_ql
                        if lyric_fn:
                            lyr = lyric_fn(entry)
                            if lyr is not None:
                                n.lyric = lyr
                        m.insert(offset, n)
                        offset += unit_ql
                        i += 1
                    else:
                        count = 0
                        while i < BAR and slots[i] is None:
                            count += 1
                            i += 1
                        r = m21Rest()
                        r.quarterLength = count * unit_ql
                        m.insert(offset, r)
                        offset += count * unit_ql
            else:
                tw = td["tup_written"]
                ta = td["tup_actual"]
                tn = td["tup_normal"]
                for g_start in range(0, BAR, 3):
                    group = slots[g_start:g_start + 3]
                    if all(s is None for s in group):
                        r = m21Rest()
                        r.quarterLength = 3 * unit_ql
                        m.insert(offset, r)
                        offset += 3 * unit_ql
                        continue
                    elements = []
                    j = 0
                    while j < 3:
                        if group[j] is not None:
                            entry = group[j]
                            n = note.Note(PC_TO_MUSIC21[entry[1]])
                            n.quarterLength = unit_ql
                            if lyric_fn:
                                lyr = lyric_fn(entry)
                                if lyr is not None:
                                    n.lyric = lyr
                            elements.append(n)
                            j += 1
                        else:
                            rc = 0
                            while j < 3 and group[j] is None:
                                rc += 1
                                j += 1
                            r = m21Rest()
                            r.quarterLength = rc * unit_ql
                            elements.append(r)
                    for idx, el in enumerate(elements):
                        tup = m21duration.Tuplet(ta, tn, tw)
                        tup.bracket = True
                        if idx == 0:
                            tup.type = 'start'
                        if idx == len(elements) - 1:
                            tup.type = 'stop'
                        el.duration.tuplets = (tup,)
                        m.insert(offset, el)
                        offset += el.quarterLength

            part.append(m)

        ms = part.getElementsByClass(stream.Measure)
        if ms:
            ms[-1].rightBarline = bar.Barline("final")
        return part

    # ── Zeitnetz part (staff 1) ───────────────────────────────────────
    zn_labels = {pos: label for label, pos in row_start_pos.items()}
    zn_sorted = [(p, pc, dur) for p, pc, dur, _ in zn_events
                 if p < n_bars * BAR]
    zn_part   = _build_part_final("Zeitnetz", zn_sorted, zn_labels,
                                  lyric_fn=lambda e: str(e[2]))
    sc.append(zn_part)

    # ── Family staves ─────────────────────────────────────────────────
    n_used = sum(1 for s in range(1, n_staves + 1) if staff_notes[s])
    for s in range(1, n_staves + 1):
        p = _build_part_final(
            f"Staff {s}", staff_notes[s], staff_labels[s],
            lyric_fn=lambda e: f"{e[3]}.{e[4]}")
        sc.append(p)

    sc.write("musicxml", fp=filename)

    # ── Summary ───────────────────────────────────────────────────────
    print(f"  {1 + n_staves} staves (1 Zeitnetz + {n_staves} family, "
          f"{n_used} used), {n_bars} bars")
    print(f"  Families placed: {len(final_fam)}/75")
    print(f"  Max grid position: {max_final_pos}")

    # Per-staff summary
    for s in range(1, n_staves + 1):
        fams_on = sorted([fn for fn, st in staff_assign.items() if st == s],
                         key=lambda fn: final_fam[fn][0][0] if final_fam[fn] else 0)
        if fams_on:
            print(f"    Staff {s:2d}: {', '.join(f'F{fn}' for fn in fams_on)}")

    # Family detail
    print(f"\n  Family final positions (first → last):")
    for f in s3_2:
        fn = f["family"]
        ents = final_fam.get(fn, [])
        if ents:
            print(f"    F{fn:2d}: {pc_name(ents[0][1])}@{ents[0][0]} → "
                  f"{pc_name(ents[-1][1])}@{ents[-1][0]}  "
                  f"({len(ents)} entries, staff {staff_assign[fn]})")

    return filename


def export_zeitnetz_v2(s2, s3_2, filename="zeitnetz_v2.musicxml"):
    """
    Zeitnetz Version 2 — Variable time signatures.

    Same content as Stage 4 (cyclic Zeitnetz + 75 sound families on 12 staves),
    but each bar's time signature follows a cyclic 105-bar sequence of 7 types.
    The 12 grid positions per bar are preserved; only the unit duration changes:

        Type 1: 3/8   unit = 32nd note
        Type 2: 4/8   unit = 16th-note triplet
        Type 3: 3/4   unit = 16th note
        Type 4: 4/4   unit = 8th-note triplet
        Type 5: 3/2   unit = 8th note
        Type 6: 4/2   unit = quarter-note triplet
        Type 7: 12/4  unit = quarter note
    """
    from fractions import Fraction
    from music21 import expressions, duration as m21duration

    sc = _make_score("Zeitnetz Version 2 — Variable Time Signatures")

    # ── Time-signature sequence (105 entries, applied cyclically) ─────
    TS_SEQ = [
        7,6,6,5,5,5,4,4,4,4,3,3,3,3,3,2,2,2,2,2,2,
        1,1,1,1,1,1,1,1,1,1,1,1,1,1,
        2,2,2,2,2,2,2,3,3,3,3,3,3,3,4,4,4,4,4,4,4,
        5,5,5,5,5,5,5,6,6,6,6,6,6,6,
        7,7,7,7,7,7,7,7,7,7,7,7,7,7,
        6,6,6,6,6,6,5,5,5,5,5,4,4,4,4,3,3,3,2,2,1,
    ]

    TS_DEFS = {
        1: {"ts": "3/8",  "unit_ql": Fraction(1, 8),  "is_tuplet": False},
        2: {"ts": "4/8",  "unit_ql": Fraction(1, 6),  "is_tuplet": True,
            "tup_written": "16th",    "tup_actual": 3, "tup_normal": 2},
        3: {"ts": "3/4",  "unit_ql": Fraction(1, 4),  "is_tuplet": False},
        4: {"ts": "4/4",  "unit_ql": Fraction(1, 3),  "is_tuplet": True,
            "tup_written": "eighth",  "tup_actual": 3, "tup_normal": 2},
        5: {"ts": "3/2",  "unit_ql": Fraction(1, 2),  "is_tuplet": False},
        6: {"ts": "4/2",  "unit_ql": Fraction(2, 3),  "is_tuplet": True,
            "tup_written": "quarter", "tup_actual": 3, "tup_normal": 2},
        7: {"ts": "12/4", "unit_ql": Fraction(1, 1),  "is_tuplet": False},
    }

    # ── 1. Build original 12 rows as templates ───────────────────────
    row_templates = []
    for v in s2:
        row_templates.append((
            v["voice_index"],
            v["initial_rest_32nds"],
            list(v["notes"]),
        ))

    # ── 2. Flatten original Zeitnetz + cyclic extensions ─────────────
    zn_events = []
    row_start_pos = {}

    pos = 0
    for vi, ir, notes in row_templates:
        if ir > 0:
            pos += ir
        label = f"Row {vi}"
        row_start_pos[label] = pos
        for pc, dur_32 in notes:
            zn_events.append((pos, pc, dur_32, label))
            pos += dur_32

    MAX_CYCLES = 10
    cycle = 1
    all_done = False
    while cycle <= MAX_CYCLES and not all_done:
        suffix = chr(ord('a') + cycle - 1)
        for vi, _ir, notes in row_templates:
            label = f"Row {vi}{suffix}"
            row_start_pos[label] = pos
            for pc, dur_32 in notes:
                zn_events.append((pos, pc, dur_32, label))
                pos += dur_32
        all_done = _test_all_families_done(zn_events, s3_2)
        cycle += 1

    total_32 = pos

    # ── 3. Sequential scan — family activation ───────────────────────
    family_queue = list(s3_2)
    active = []
    fam_events = {f["family"]: [] for f in s3_2}
    fam_evt_count = {}

    for ev_pos, ev_pc, ev_dur, ev_label in zn_events:
        if family_queue and family_queue[0]["start_pc"] == ev_pc:
            f = family_queue.pop(0)
            active.append(f)
            fam_evt_count[f["family"]] = 0
        for f in active:
            fam_events[f["family"]].append((ev_pos, ev_pc))
            fam_evt_count[f["family"]] += 1
        new_active = []
        for f in active:
            if f["end_pc"] == ev_pc:
                if f["start_pc"] == f["end_pc"]:
                    if fam_evt_count[f["family"]] >= 2:
                        continue
                    else:
                        new_active.append(f)
                else:
                    continue
            else:
                new_active.append(f)
        active = new_active
        if not family_queue and not active:
            break

    activated_fams = [f for f in s3_2 if len(fam_events[f["family"]]) > 0]

    # ── 4. Round-robin staff assignment ───────────────────────────────
    staff_assign = {}
    for f in activated_fams:
        fn = f["family"]
        staff_assign[fn] = ((fn - 1) % 12) + 1

    # ── 5. Build per-staff note lists ─────────────────────────────────
    staff_notes  = {s: [] for s in range(1, 13)}
    staff_labels = {s: {} for s in range(1, 13)}
    for f in activated_fams:
        fn = f["family"]
        s = staff_assign[fn]
        evts = fam_events[fn]
        for i, (p, pc) in enumerate(evts):
            staff_notes[s].append((p, pc))
            if i == 0:
                staff_labels[s][p] = f"F{fn}"
    for s in staff_notes:
        staff_notes[s].sort()

    # ── 6. Build V2 measures ──────────────────────────────────────────
    BAR    = 12
    n_bars = (total_32 + BAR - 1) // BAR

    def _build_part_v2(name, notes_sorted, labels_dict=None, lyric_fn=None):
        part = stream.Part()
        part.partName = name
        ni = 0
        prev_ts_str = None

        for b in range(n_bars):
            ts_idx = TS_SEQ[b % len(TS_SEQ)]
            td     = TS_DEFS[ts_idx]
            ts_str = td["ts"]
            unit_ql = td["unit_ql"]
            is_tup  = td["is_tuplet"]

            m = stream.Measure(number=b + 1)

            # Time signature (only when it changes)
            if ts_str != prev_ts_str:
                m.append(meter.TimeSignature(ts_str))
                if prev_ts_str is None:
                    m.append(clef.TrebleClef())
                prev_ts_str = ts_str

            bs = b * BAR   # bar start in grid units

            # Text labels (row names, family names)
            if labels_dict:
                for lp, lt in labels_dict.items():
                    if bs <= lp < bs + BAR:
                        te = expressions.TextExpression(lt)
                        te.placement = "above"
                        m.insert((lp - bs) * unit_ql, te)

            # Collect 12 slots: note entry or None (rest)
            slots = []
            for g in range(BAR):
                gpos = bs + g
                if ni < len(notes_sorted) and notes_sorted[ni][0] == gpos:
                    slots.append(notes_sorted[ni])
                    ni += 1
                else:
                    slots.append(None)

            offset = Fraction(0)

            if not is_tup:
                # ── Non-tuplet bar: simple placement, merge rests ────
                i = 0
                while i < BAR:
                    if slots[i] is not None:
                        entry = slots[i]
                        n = note.Note(PC_TO_MUSIC21[entry[1]])
                        n.quarterLength = unit_ql
                        if lyric_fn:
                            lyr = lyric_fn(entry)
                            if lyr is not None:
                                n.lyric = lyr
                        m.insert(offset, n)
                        offset += unit_ql
                        i += 1
                    else:
                        count = 0
                        while i < BAR and slots[i] is None:
                            count += 1
                            i += 1
                        r = m21Rest()
                        r.quarterLength = count * unit_ql
                        m.insert(offset, r)
                        offset += count * unit_ql
            else:
                # ── Tuplet bar: groups of 3 with explicit brackets ───
                tw = td["tup_written"]
                ta = td["tup_actual"]
                tn = td["tup_normal"]

                for g_start in range(0, BAR, 3):
                    group = slots[g_start:g_start + 3]

                    # Full-beat rest → standard duration, no tuplet
                    if all(s is None for s in group):
                        r = m21Rest()
                        r.quarterLength = 3 * unit_ql
                        m.insert(offset, r)
                        offset += 3 * unit_ql
                        continue

                    # Build elements within this 3-slot group
                    elements = []
                    j = 0
                    while j < 3:
                        if group[j] is not None:
                            entry = group[j]
                            n = note.Note(PC_TO_MUSIC21[entry[1]])
                            n.quarterLength = unit_ql
                            if lyric_fn:
                                lyr = lyric_fn(entry)
                                if lyr is not None:
                                    n.lyric = lyr
                            elements.append(n)
                            j += 1
                        else:
                            rcount = 0
                            while j < 3 and group[j] is None:
                                rcount += 1
                                j += 1
                            r = m21Rest()
                            r.quarterLength = rcount * unit_ql
                            elements.append(r)

                    # Attach tuplet to every element in the group
                    for idx, el in enumerate(elements):
                        tup = m21duration.Tuplet(ta, tn, tw)
                        tup.bracket = True
                        if idx == 0:
                            tup.type = 'start'
                        if idx == len(elements) - 1:
                            tup.type = 'stop'
                        el.duration.tuplets = (tup,)
                        m.insert(offset, el)
                        offset += el.quarterLength

            part.append(m)

        ms = part.getElementsByClass(stream.Measure)
        if ms:
            ms[-1].rightBarline = bar.Barline("final")
        return part

    # ── Zeitnetz part (top staff) ─────────────────────────────────────
    zn_labels = {pos: label for label, pos in row_start_pos.items()}
    zn_sorted = [(p, pc, dur) for p, pc, dur, _ in zn_events]
    zn_part   = _build_part_v2("Zeitnetz", zn_sorted, zn_labels,
                               lyric_fn=lambda e: str(e[2]))
    sc.append(zn_part)

    # ── 12 family staves ─────────────────────────────────────────────
    pos_to_dur = {p: dur for p, pc, dur, _ in zn_events}
    n_used = sum(1 for s in range(1, 13) if staff_notes[s])
    for s in range(1, 13):
        p = _build_part_v2(f"Staff {s}", staff_notes[s], staff_labels[s],
                           lyric_fn=lambda e: str(pos_to_dur.get(e[0], "")))
        sc.append(p)

    sc.write("musicxml", fp=filename)

    # ── Summary ───────────────────────────────────────────────────────
    activated = len(activated_fams)
    n_cycles = cycle - 1
    print(f"\n  Zeitnetz V2: {n_bars} bars, {total_32} grid positions")
    print(f"  13 staves ({n_used} used), {activated}/75 families")
    print(f"  Cyclic TS sequence: {len(TS_SEQ)} entries, applied cyclically")

    # Count bars per type
    type_count = {t: 0 for t in range(1, 8)}
    for b in range(n_bars):
        type_count[TS_SEQ[b % len(TS_SEQ)]] += 1
    ts_names = {1:"3/8", 2:"4/8", 3:"3/4", 4:"4/4", 5:"3/2", 6:"4/2", 7:"12/4"}
    for t in range(1, 8):
        if type_count[t]:
            print(f"    Type {t} ({ts_names[t]:>4}): {type_count[t]} bars")

    return filename


def _old_export_stage4(s4, filename="zeitnetz_stage4.musicxml"):
    """
    Stage 4 — Netz-Familien.
    12 parts (one per voice).  Each Klangfamilie = one measure.
    Notes are written with their actual 32nd-note durations (converted to quarters).
    Lyrics show:  pitch-name / duration-category (0–3).
    A separator rest of one quarter is inserted between families.
    Inter-family distance appears as a lyric on the separator rest.
    A double barline closes each family; final barline after the last.
    """
    sc = _make_score("Stage 4 — Netz-Familien")

    for voice in s4:
        k    = voice["voice_index"]
        part = stream.Part()
        part.partName = f"Voice {k + 1}"
        net_fams = voice["net_families"]

        measure_num = 1
        for f_idx, fam_data in enumerate(net_fams):
            notes_data = fam_data["notes"]   # list of voice-note dicts
            inter      = fam_data["inter_distance"]

            # Total duration: notes + optional 1-quarter separator
            total_quarters = sum(
                max(0.125, nd["duration_32nds"] / 8.0) for nd in notes_data
            )
            sep_quarters = 1.0 if f_idx < len(net_fams) - 1 else 0.0
            beat_count   = total_quarters + sep_quarters

            # Use a simple N/4 time signature (rounded up to nearest beat)
            import math
            beats = max(1, math.ceil(beat_count))
            ts    = meter.TimeSignature(f"{beats}/4")

            m = stream.Measure(number=measure_num)
            m.append(ts)
            m.append(clef.TrebleClef())

            for nd in notes_data:
                pc  = nd["pc"]
                dur = max(0.125, nd["duration_32nds"] / 8.0)
                cat = nd["dur_category"]
                n   = note.Note(PC_TO_MUSIC21[pc])
                n.quarterLength = dur
                n.lyric = f"{pc_name(pc)}/{cat}"
                m.append(n)

            # Separator rest carrying inter-family distance as lyric
            if sep_quarters > 0:
                r = m21Rest()
                r.quarterLength = sep_quarters
                r.lyric = f"inter={inter}"
                m.append(r)

            if f_idx < len(net_fams) - 1:
                m.rightBarline = bar.Barline("double")
            else:
                m.rightBarline = bar.Barline("final")

            part.append(m)
            measure_num += 1

        sc.insert(0, part)

    sc.write("musicxml", fp=filename)
    return filename


def export_stage5(s5, filename="zeitnetz_stage5.musicxml"):
    """Final netz: all families concatenated per voice, durations corrected."""
    sc = _make_score("Stage 5 — Final Netz")
    for v in s5:
        part = stream.Part()
        part.partName = f"Voice {v['voice_index'] + 1}"
        m = stream.Measure(number=1)
        m.append(clef.TrebleClef())
        for fam in v["final_families"]:
            for nd in fam["final_notes"]:
                n = note.Note(PC_TO_MUSIC21[nd["pc"]])
                n.quarterLength = max(0.125, nd["duration_32nds_corrected"] / 8.0)
                n.lyric = pc_name(nd["pc"])
                m.append(n)
        m.rightBarline = bar.Barline("final")
        part.append(m)
        sc.insert(0, part)
    sc.write("musicxml", fp=filename)
    return filename


# ═══════════════════════════════════════════════════════════════════════════════
# CONSOLE SUMMARIES
# ═══════════════════════════════════════════════════════════════════════════════

def _hr(title=""):
    w = 80
    bar_str = "═" * w
    if title:
        pad = (w - len(title) - 2) // 2
        print(f"\n{'═'*pad} {title} {'═'*(w - pad - len(title) - 2)}")
    else:
        print(f"\n{bar_str}")


def print_stage1(s1):
    _hr("STAGE 1 — ROW GENERATION")
    print(f"  Pitch row  : {' '.join(pc_name(p) for p in s1['pitch_row'])}")
    print(f"  Rhythm row : {' '.join(pc_name(p) for p in s1['rhythm_row'])}")
    print(f"  Onsets     : {s1['onsets']}")
    print()
    print(f"  {'k':>3}  {'PITCH PERMUTATION':^46}  {'RHYTHM PERMUTATION':^46}")
    print(f"  {'─'*3}  {'─'*46}  {'─'*46}")
    for k in range(12):
        l = ' '.join(f"{pc_name(p):>4}" for p in s1['pitch_perms'][k])
        r = ' '.join(f"{pc_name(p):>4}" for p in s1['rhythm_perms'][k])
        print(f"  {k+1:>3}  {l}  {r}")


def print_stage2(s2):
    _hr("STAGE 2 — ZEITNETZ VERSION 1")
    print(f"  {'Voice':>5}  {'Rest':>5}  Notes  (name / duration in 32nds)")
    print(f"  {'─'*5}  {'─'*5}  {'─'*60}")
    for v in s2:
        notes_str = "  ".join(f"{pc_name(pc)}({d})" for pc, d in v["notes"])
        print(f"  {v['voice_index']+1:>5}  {v['initial_rest_32nds']:>5}  {notes_str}")


def print_stage3(s3):
    _hr("STAGE 3.1 — KLANGFAMILIEN STARTING PITCHES")
    by_row = {rd["row_index"]: rd for rd in s3}
    ROW_ORDER = [7, 8, 9, 10, 11, 0, 1, 2, 3, 4, 5, 6]
    fam = 1
    total = 0
    for ri in ROW_ORDER:
        rd = by_row[ri]
        pitches = rd["pitches"]
        n = len(pitches)
        total += n
        labels = [f"{pc_name(p)}({fam + j})" for j, p in enumerate(pitches)]
        print(f"  Row {ri:2d} │ Families {fam:2d}–{fam+n-1:2d} │ {' '.join(labels)}")
        fam += n
    print(f"\n  Total starting pitches: {total}")


def print_stage3_2(s3_2):
    _hr("STAGE 3.2 — KLANGFAMILIEN (START → END)")
    for fam in s3_2:
        print(f"  Family {fam['family']:2d}  "
              f"{pc_name(fam['start_pc']):4s} → {pc_name(fam['end_pc']):4s}  "
              f"(Row {fam['row']})")


def print_stage4(s4):
    _hr("STAGE 4 — NETZ-FAMILIEN")
    for v in s4:
        k = v["voice_index"]
        print(f"\n  Voice {k+1}")
        for fam in v["net_families"]:
            cats = ' '.join(str(n["dur_category"]) for n in fam["notes"])
            print(f"    Family {fam['family_index']+1}: "
                  f"{pc_name(fam['start_pc'])}→{pc_name(fam['end_pc'])}  "
                  f"fwd={fam['count_forward']}  inter={fam['inter_distance']}  "
                  f"dur-cats=[{cats}]")


def print_stage5(s5):
    _hr("STAGE 5 — FINAL NETZ")
    for v in s5:
        k = v["voice_index"]
        print(f"\n  Voice {k+1}")
        for fam in v["final_families"]:
            notes_str = ' '.join(
                f"{pc_name(n['pc'])}({n['duration_32nds_corrected']})"
                for n in fam["final_notes"]
            )
            print(f"    Family {fam['family_index']+1}: {notes_str}")


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════

DEFAULT_PITCHES   = "1 11 0 8 9 3 6 4 2 10 5 7"
DEFAULT_PERM      = "1 5 0 6 2 7 11 8 3 10 4 9"
DEFAULT_DURATIONS = "-11 6 9 7 6 6 4 3 10 6 3 1 10"


def main():
    parser = argparse.ArgumentParser(
        description="Zeitnetz Complete Pipeline — all 5 stages.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 zeitnetz_pipeline.py
  python3 zeitnetz_pipeline.py --export
  python3 zeitnetz_pipeline.py --pitches "cis h c gis a dis fis e d ais f g" --export
        """,
    )
    parser.add_argument("--pitches",   type=str, default=DEFAULT_PITCHES,
                        help="12 pitch classes (integers 0–11 or German names)")
    parser.add_argument("--perm",      type=str, default=DEFAULT_PERM,
                        help="Permutation pattern (12 integers, 0-indexed)")
    parser.add_argument("--durations", type=str, default=DEFAULT_DURATIONS,
                        help="Duration list (13 integers; first may be negative)")
    parser.add_argument("--axis",      type=int, default=None,
                        help="Symmetry axis pitch class 0–11 (default: pitch_row[0])")
    parser.add_argument("--export",    action="store_true",
                        help="Write one MusicXML file per stage (stages 1–5)")
    args = parser.parse_args()

    try:
        pitch_row     = parse_pitch_input(args.pitches)
        perm_pattern  = parse_int_list(args.perm,      12, "Permutation pattern")
        duration_list = parse_int_list(args.durations, 13, "Duration list")
    except ValueError as e:
        print(f"Input error: {e}", file=sys.stderr)
        sys.exit(1)

    axis_pc = args.axis if args.axis is not None else pitch_row[0]

    print("\nRunning Zeitnetz Pipeline...")
    print(f"  Pitch row    : {' '.join(pc_name(p) for p in pitch_row)}")
    print(f"  Perm pattern : {perm_pattern}")
    print(f"  Durations    : {duration_list}")
    print(f"  Symmetry axis: {pc_name(axis_pc)}")

    # ── STAGE 1 ──────────────────────────────────────────────────────────────
    try:
        s1 = run_stage1(pitch_row, perm_pattern, duration_list)
    except ValueError as e:
        print(f"Stage 1 error: {e}", file=sys.stderr)
        sys.exit(1)
    print_stage1(s1)
    if args.export:
        f = export_stage1(s1)
        print(f"\n  ✓ Saved: {f}")

    # ── STAGE 2 ──────────────────────────────────────────────────────────────
    s2 = run_stage2(s1)
    print_stage2(s2)
    if args.export:
        f = export_stage2(s2)
        print(f"  ✓ Saved: {f}")

    # ── STAGE 3.1 ────────────────────────────────────────────────────────────
    s3 = run_stage3(s1)
    print_stage3(s3)
    if args.export:
        fa, fb = export_stage3(s3)
        print(f"  ✓ Saved: {fa}")
        print(f"  ✓ Saved: {fb}")

    # ── STAGE 3.2 ────────────────────────────────────────────────────────────
    s3_2 = run_stage3_2(s3)
    print_stage3_2(s3_2)
    if args.export:
        f = export_stage3_2(s3_2)
        print(f"  ✓ Saved: {f}")

    # ── STAGE 4 — FULL SCORE ──────────────────────────────────────────────
    if args.export:
        f = export_stage4_score(s2, s3_2)
        print(f"  ✓ Saved: {f}")

    # ── ZEITNETZ VERSION 2 — VARIABLE TIME SIGNATURES ─────────────────
    if args.export:
        f = export_zeitnetz_v2(s2, s3_2)
        print(f"  ✓ Saved: {f}")

    # ── ZEITNETZ FINAL — DURATION AS COUNT ────────────────────────────
    if args.export:
        f = export_zeitnetz_final(s2, s3_2)
        print(f"  ✓ Saved: {f}")

    print("\n✓ Done.\n")


if __name__ == "__main__":
    main()
