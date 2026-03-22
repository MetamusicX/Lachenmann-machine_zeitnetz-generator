#!/usr/bin/env python3
"""Generate PDF from the Zeitnetz report markdown."""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm, cm
from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib import colors
import re

OUTPUT = "REPORT_Zeitnetz_Generator.pdf"

# ── Styles ───────────────────────────────────────────────────────────
styles = getSampleStyleSheet()

styles.add(ParagraphStyle(
    name='ReportTitle',
    fontName='Helvetica-Bold',
    fontSize=18,
    leading=22,
    spaceAfter=6,
    alignment=TA_LEFT,
    textColor=HexColor('#1a1a2e'),
))
styles.add(ParagraphStyle(
    name='Subtitle',
    fontName='Helvetica-Oblique',
    fontSize=12,
    leading=16,
    spaceAfter=4,
    textColor=HexColor('#333355'),
))
styles.add(ParagraphStyle(
    name='MetaInfo',
    fontName='Helvetica',
    fontSize=9,
    leading=13,
    spaceAfter=2,
    textColor=HexColor('#444444'),
))
styles.add(ParagraphStyle(
    name='H1',
    fontName='Helvetica-Bold',
    fontSize=15,
    leading=20,
    spaceBefore=18,
    spaceAfter=8,
    textColor=HexColor('#1a1a2e'),
))
styles.add(ParagraphStyle(
    name='H2',
    fontName='Helvetica-Bold',
    fontSize=12,
    leading=16,
    spaceBefore=14,
    spaceAfter=6,
    textColor=HexColor('#2d2d5e'),
))
styles.add(ParagraphStyle(
    name='H3',
    fontName='Helvetica-Bold',
    fontSize=10,
    leading=14,
    spaceBefore=10,
    spaceAfter=4,
    textColor=HexColor('#3a3a6e'),
))
styles.add(ParagraphStyle(
    name='BodyText2',
    fontName='Helvetica',
    fontSize=9.5,
    leading=13.5,
    spaceAfter=6,
    alignment=TA_JUSTIFY,
    textColor=HexColor('#1a1a1a'),
))
styles.add(ParagraphStyle(
    name='CodeBlock',
    fontName='Courier',
    fontSize=8,
    leading=11,
    spaceAfter=6,
    spaceBefore=4,
    leftIndent=12,
    backColor=HexColor('#f4f4f8'),
    borderColor=HexColor('#ccccdd'),
    borderWidth=0.5,
    borderPadding=6,
    textColor=HexColor('#222222'),
))
styles.add(ParagraphStyle(
    name='Quote',
    fontName='Helvetica-Oblique',
    fontSize=9,
    leading=13,
    leftIndent=20,
    rightIndent=20,
    spaceAfter=8,
    spaceBefore=4,
    textColor=HexColor('#333355'),
))
styles.add(ParagraphStyle(
    name='BulletItem',
    fontName='Helvetica',
    fontSize=9.5,
    leading=13.5,
    spaceAfter=3,
    leftIndent=20,
    bulletIndent=8,
    textColor=HexColor('#1a1a1a'),
))
styles.add(ParagraphStyle(
    name='NumberedItem',
    fontName='Helvetica',
    fontSize=9.5,
    leading=13.5,
    spaceAfter=3,
    leftIndent=20,
    bulletIndent=8,
    textColor=HexColor('#1a1a1a'),
))
styles.add(ParagraphStyle(
    name='Footer',
    fontName='Helvetica-Oblique',
    fontSize=8,
    leading=11,
    alignment=TA_CENTER,
    textColor=HexColor('#888888'),
))


def fmt(text):
    """Convert markdown inline formatting to reportlab XML."""
    # Bold + italic
    text = re.sub(r'\*\*\*(.+?)\*\*\*', r'<b><i>\1</i></b>', text)
    # Bold
    text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text)
    # Italic (only single *)
    text = re.sub(r'(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)', r'<i>\1</i>', text)
    # Inline code
    text = re.sub(r'`([^`]+)`', r'<font name="Courier" size="8.5">\1</font>', text)
    # Em dash
    text = text.replace('—', '\u2014')
    # Arrows
    text = text.replace('→', '\u2192')
    # Handle special XML chars (but not our tags)
    # Already handled by reportlab mostly
    return text


def make_table(headers, rows, col_widths=None):
    """Build a styled Table from header + row lists."""
    data = [headers] + rows
    if col_widths is None:
        n = len(headers)
        col_widths = [None] * n

    t = Table(data, colWidths=col_widths, repeatRows=1)
    t.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('LEADING', (0, 0), (-1, -1), 11),
        ('BACKGROUND', (0, 0), (-1, 0), HexColor('#e8e8f0')),
        ('TEXTCOLOR', (0, 0), (-1, -1), HexColor('#1a1a1a')),
        ('GRID', (0, 0), (-1, -1), 0.4, HexColor('#bbbbcc')),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4),
    ]))
    return t


def build_story():
    """Build the PDF story (list of flowables)."""
    story = []

    # ── Title page ──
    story.append(Spacer(1, 30*mm))
    story.append(Paragraph("Zeitnetz Generator", styles['ReportTitle']))
    story.append(Spacer(1, 4*mm))
    story.append(Paragraph(
        "Full Technical Report", styles['ReportTitle']))
    story.append(Spacer(1, 8*mm))
    story.append(Paragraph(
        "Algorithmic Replication of Lachenmann\u2019s <i>Mouvement (\u2013 vor der Erstarrung)</i> Time-Grid Generation",
        styles['Subtitle']))
    story.append(Spacer(1, 12*mm))
    story.append(HRFlowable(width="60%", thickness=0.5, color=HexColor('#888899')))
    story.append(Spacer(1, 8*mm))

    meta = [
        ("Based on:", "Lu\u00eds Antunes Pena, <i>Klangnetz und Klangfarbe in Helmut Lachenmanns Mouvement (\u2013 vor der Erstarrung)</i>, Diplomarbeit, 2004"),
        ("Implementation by:", "Paulo de Assis, in collaboration with Claude (Anthropic), March 2026"),
        ("Source file:", '<font name="Courier" size="9">zeitnetz_pipeline.py</font> (~2270 lines of Python)'),
        ("Dependencies:", "Python 3.9, music21"),
    ]
    for label, value in meta:
        story.append(Paragraph(f"<b>{label}</b> {value}", styles['MetaInfo']))
    story.append(Spacer(1, 15*mm))

    # TOC
    story.append(Paragraph("Table of Contents", styles['H2']))
    toc_items = [
        "1. Project Overview",
        "2. Stage 1 \u2014 Row Generation",
        "3. Stage 2 \u2014 Zeitnetz Version 1 (Circular Reading)",
        "4. Stage 3 \u2014 Klangfamilien (Sound Families)",
        "5. Stage 4 \u2014 Full Score (Cyclic Zeitnetz + 75 Families)",
        "6. Zeitnetz Version 2 \u2014 Variable Time Signatures",
        "7. Zeitnetz Final \u2014 Duration as Count",
        "8. Output Files",
        "9. Technical Architecture",
        "10. Usage",
        "Appendix: Development History",
    ]
    for item in toc_items:
        story.append(Paragraph(item, styles['BulletItem']))

    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════════
    # 1. PROJECT OVERVIEW
    # ══════════════════════════════════════════════════════════════════
    story.append(Paragraph("1. Project Overview", styles['H1']))
    story.append(Paragraph(fmt(
        "This project replicates, in a single Python pipeline, the complete algorithmic process by which "
        "Helmut Lachenmann generated the temporal structure (Zeitnetz \u2014 \"time-net\") of his orchestral "
        "work *Mouvement (\u2013 vor der Erstarrung)* (1982\u201384). The reconstruction follows Lu\u00eds Antunes "
        "Pena\u2019s detailed musicological analysis, which reverse-engineered Lachenmann\u2019s process from the "
        "sketches and identified five compositional stages, originally realised in IRCAM\u2019s OpenMusic environment."
    ), styles['BodyText2']))
    story.append(Paragraph(fmt(
        "The pipeline takes three inputs \u2014 a 12-note pitch row, a permutation pattern, and a duration "
        "list \u2014 and produces, through a chain of deterministic transformations, the complete Zeitnetz "
        "with 75 sound families, variable time signatures, and the final duration-as-count transformation. "
        "All intermediate and final results are exported as MusicXML files for verification in standard "
        "notation software."
    ), styles['BodyText2']))

    story.append(Paragraph("Default Inputs (Lachenmann\u2019s <i>Mouvement</i>)", styles['H3']))
    story.append(make_table(
        ["Parameter", "Values"],
        [
            ["Pitch row", "1 11 0 8 9 3 6 4 2 10 5 7 (cis h c gis a dis fis e d ais f g)"],
            ["Permutation pattern", "1 5 0 6 2 7 11 8 3 10 4 9"],
            ["Duration list", "\u221211 6 9 7 6 6 4 3 10 6 3 1 10 (13 values; first is negative = initial rest)"],
        ],
        col_widths=[35*mm, 130*mm]
    ))
    story.append(Spacer(1, 4*mm))

    story.append(Paragraph("Pitch Naming Convention", styles['H3']))
    story.append(Paragraph(fmt(
        "The pipeline uses German pitch names throughout, following Pena\u2019s analysis:"
    ), styles['BodyText2']))
    story.append(make_table(
        ["PC", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11"],
        [["Name", "c", "cis", "d", "dis", "e", "f", "fis", "g", "gis", "a", "ais", "h"]],
        col_widths=[14*mm] + [12.5*mm]*12
    ))
    story.append(Spacer(1, 4*mm))

    # ══════════════════════════════════════════════════════════════════
    # 2. STAGE 1
    # ══════════════════════════════════════════════════════════════════
    story.append(PageBreak())
    story.append(Paragraph("2. Stage 1 \u2014 Row Generation", styles['H1']))
    story.append(Paragraph(fmt(
        '**OM patch:** "1-erzeugt-reihe" \u2014 **Function:** `run_stage1()` \u2014 **Export:** `zeitnetz_stage1.musicxml`'
    ), styles['MetaInfo']))
    story.append(Spacer(1, 3*mm))

    story.append(Paragraph("2.1 Permutation Matrix", styles['H2']))
    story.append(Paragraph(fmt(
        "The foundation of the entire system is a 12\u00d712 permutation matrix. Starting from the identity "
        "row [0, 1, 2, ..., 11], each subsequent row is generated by applying the permutation pattern "
        "as an index reordering of the previous row:"
    ), styles['BodyText2']))
    story.append(Paragraph(
        "Row 0 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]<br/>"
        "Row k = [Row<sub>k-1</sub>[perm[0]], Row<sub>k-1</sub>[perm[1]], ..., Row<sub>k-1</sub>[perm[11]]]",
        styles['CodeBlock']))
    story.append(Paragraph(fmt(
        "With the default permutation pattern [1, 5, 0, 6, 2, 7, 11, 8, 3, 10, 4, 9], this produces a "
        "144-element structure that encodes all pitch and rhythmic relationships in the piece."
    ), styles['BodyText2']))

    story.append(Paragraph("2.2 Onset Computation", styles['H2']))
    story.append(Paragraph(fmt(
        "The 13-element duration list is converted to 12 cumulative onset addresses. The first value "
        "(\u221211) indicates an initial rest of 11 units; its absolute value becomes the first onset. "
        "Subsequent onsets are cumulative sums:"
    ), styles['BodyText2']))
    story.append(Paragraph(
        "onsets[0] = |duration_list[0]| = 11<br/>"
        "onsets[i] = onsets[i-1] + duration_list[i] &nbsp;&nbsp;(for i = 1..11)<br/><br/>"
        "Result: [11, 17, 26, 33, 39, 45, 49, 52, 62, 68, 71, 72]",
        styles['CodeBlock']))

    story.append(Paragraph("2.3 Rhythm Row Derivation", styles['H2']))
    story.append(Paragraph(fmt(
        "The rhythm row is derived by mapping the pitch row through the flattened permutation matrix "
        "using the computed onsets as addresses: (1) Flatten the 12\u00d712 matrix into a 144-element "
        "sequence. (2) For each pitch `pitch_row[i]`, look up `flattened[onsets[i]]` to get the target "
        "position. (3) Place the pitch at that position in the rhythm row."
    ), styles['BodyText2']))
    story.append(Paragraph(fmt("**Result:** f c dis fis gis e g h d a ais cis"), styles['BodyText2']))

    story.append(Paragraph("2.4 Permutation Generation", styles['H2']))
    story.append(Paragraph(fmt(
        "Both the pitch row and the rhythm row are then permuted 12 times using the permutation matrix, "
        "yielding **12 pitch permutations** (12\u00d712 = 144 pitch values) and **12 rhythm permutations** "
        "(12\u00d712 = 144 rhythm values). These two 144-element sequences form the raw material for Stage 2."
    ), styles['BodyText2']))

    # ══════════════════════════════════════════════════════════════════
    # 3. STAGE 2
    # ══════════════════════════════════════════════════════════════════
    story.append(Paragraph("3. Stage 2 \u2014 Zeitnetz Version 1", styles['H1']))
    story.append(Paragraph(fmt(
        '**OM patch:** "2 - Zeitnetz Version 1" \u2014 **Function:** `run_stage2()` \u2014 **Export:** `zeitnetz_stage2.musicxml`'
    ), styles['MetaInfo']))
    story.append(Spacer(1, 3*mm))

    story.append(Paragraph("3.1 Circular Scanning Algorithm", styles['H2']))
    story.append(Paragraph(fmt(
        "Stage 2 produces the Zeitnetz\u2019s temporal structure through a circular scanning process:"
    ), styles['BodyText2']))
    steps = [
        "**Concatenate** all 12 rhythm permutations into a single 144-element \"rhythm tape\"",
        "**Concatenate** all 12 pitch permutations into a 144-element \"pitch target\" sequence",
        "For each target pitch in sequence: scan the rhythm tape **circularly forward** from the current cursor position, counting steps until a match is found",
        "The **step count** becomes the **duration** of that note in 32nd-note units",
    ]
    for i, s in enumerate(steps):
        story.append(Paragraph(fmt(f"{i+1}. {s}"), styles['NumberedItem']))
    story.append(Paragraph(fmt(
        "The cursor position persists between scans \u2014 it does not reset. This circular reading creates "
        "the distinctive duration patterns that define the Zeitnetz\u2019s rhythmic profile."
    ), styles['BodyText2']))

    story.append(Paragraph("3.2 Example: Row 0 (Voice 1)", styles['H2']))
    story.append(Paragraph(
        "Rest: 11 thirty-second notes<br/>"
        "cis(6) &nbsp;h(9) &nbsp;c(7) &nbsp;gis(6) &nbsp;a(6) &nbsp;dis(4) &nbsp;fis(3) &nbsp;e(10) &nbsp;d(6) &nbsp;ais(3) &nbsp;f(1) &nbsp;g(10)",
        styles['CodeBlock']))
    story.append(Paragraph(fmt(
        "Each row contains exactly 12 notes. The durations vary from 1 to 17 thirty-second notes, "
        "determined entirely by the circular scanning distances."
    ), styles['BodyText2']))

    # ══════════════════════════════════════════════════════════════════
    # 4. STAGE 3
    # ══════════════════════════════════════════════════════════════════
    story.append(PageBreak())
    story.append(Paragraph("4. Stage 3 \u2014 Klangfamilien (Sound Families)", styles['H1']))

    story.append(Paragraph("4.1 Stage 3.1 \u2014 Starting Pitches", styles['H2']))
    story.append(Paragraph(fmt(
        '**Function:** `run_stage3()` \u2014 **Export:** `zeitnetz_stage3_1a_rows.musicxml`, `zeitnetz_stage3_1b_families.musicxml`'
    ), styles['MetaInfo']))
    story.append(Paragraph(fmt(
        "The 75 sound families are derived by reading the rhythm permutation rows in a specific circular "
        "order: **[7, 8, 9, 10, 11, 0, 1, 2, 3, 4, 5, 6]**. For each row, pitches are read left-to-right "
        "until a \"target pitch\" (determined by pitch permutation 10, the \"control row\") is reached, inclusive."
    ), styles['BodyText2']))

    story.append(make_table(
        ["Row", "Families", "Count"],
        [
            ["Row 7", "F1\u2013F10", "10"],
            ["Row 8", "F11\u2013F18", "8"],
            ["Row 9", "F19\u2013F28", "10"],
            ["Row 10", "F29\u2013F38", "10"],
            ["Row 11", "F39\u2013F41", "3"],
            ["Row 0", "F42\u2013F51", "10"],
            ["Row 1", "F52", "1"],
            ["Row 2", "F53\u2013F57", "5"],
            ["Row 3", "F58\u2013F60", "3"],
            ["Row 4", "F61\u2013F64", "4"],
            ["Row 5", "F65\u2013F70", "6"],
            ["Row 6", "F71\u2013F75", "5"],
            ["Total", "", "75"],
        ],
        col_widths=[25*mm, 35*mm, 20*mm]
    ))
    story.append(Spacer(1, 4*mm))

    story.append(Paragraph("4.2 Stage 3.2 \u2014 End Pitches", styles['H2']))
    story.append(Paragraph(fmt(
        '**Function:** `run_stage3_2()` \u2014 **Export:** `zeitnetz_stage3_2.musicxml`'
    ), styles['MetaInfo']))
    story.append(Paragraph(fmt(
        "Each family receives an end pitch through a complementary reading process: "
        "(1) Build an \"end-pitch tape\" by reading the same rows in **reverse order** [6, 5, 4, 3, 2, 1, 0, 11, 10, 9, 8, 7], "
        "**reversing each row\u2019s pitches**. (2) Pair start pitch *i* with end-tape pitch *i*."
    ), styles['BodyText2']))
    story.append(Paragraph(fmt(
        "This yields 75 families, each defined by a `(start_pc, end_pc)` pair. Notable special cases: "
        "**Families 8, 12, 34, 42, 45, 64, and 68** have identical start and end pitches (e.g., F8: gis\u2192gis). "
        "These require special handling in Stage 4."
    ), styles['BodyText2']))

    # ══════════════════════════════════════════════════════════════════
    # 5. STAGE 4
    # ══════════════════════════════════════════════════════════════════
    story.append(Paragraph("5. Stage 4 \u2014 Full Score", styles['H1']))
    story.append(Paragraph(fmt(
        '**Function:** `export_stage4_score()` \u2014 **Export:** `zeitnetz_stage4_score.musicxml`'
    ), styles['MetaInfo']))
    story.append(Paragraph(fmt(
        "This is the central stage: the complete Zeitnetz time-grid with all 75 sound families placed on a 13-staff score."
    ), styles['BodyText2']))

    story.append(Paragraph("5.1 Cyclic Zeitnetz Extension", styles['H2']))
    story.append(Paragraph(fmt(
        "The original 12 rows of the Zeitnetz (from Stage 2) contain only 144 events \u2014 insufficient "
        "to activate all 75 families through sequential scanning. Lachenmann\u2019s solution: **cyclically extend** "
        "the Zeitnetz. After the original 12 rows (Row 0\u2013Row 11), the rows restart as \"Row 0b\", \"Row 1b\", "
        "\"Row 2b\", etc., preserving the same durations but without initial rests (continuous concatenation)."
    ), styles['BodyText2']))
    story.append(Paragraph(fmt(
        "The pipeline adds cyclic extensions until all 75 families have activated and deactivated. With the "
        "default inputs, **3 extra cycles** are required, producing **576 total Zeitnetz events** "
        "(144 original + 3 \u00d7 144 cyclic), **3,947 thirty-second-note grid positions**, and **329 bars** in 3/8 time."
    ), styles['BodyText2']))

    story.append(Paragraph("5.2 Sequential Scan \u2014 Family Activation", styles['H2']))
    story.append(Paragraph(fmt(
        "A single left-to-right scan of all Zeitnetz events determines when each family activates and deactivates:"
    ), styles['BodyText2']))
    scan_steps = [
        "**Queue:** Families are queued in order F1\u2192F75",
        "**Activation:** The next queued family activates when its `start_pc` matches the current Zeitnetz event\u2019s pitch class",
        "**Event reception:** Every currently active family receives every Zeitnetz event",
        "**Deactivation:** A family deactivates (inclusive) when its `end_pc` matches the current event",
    ]
    for i, s in enumerate(scan_steps):
        story.append(Paragraph(fmt(f"{i+1}. {s}"), styles['NumberedItem']))
    story.append(Paragraph(fmt(
        "**Same-pitch deactivation rule:** For families where `start_pc == end_pc` (F8, F12, F34, F42, F45, "
        "F64, F68), the family activates on the first occurrence and deactivates on the **next** occurrence "
        "of that same pitch \u2014 it must receive at least 2 events before deactivation."
    ), styles['BodyText2']))

    story.append(Paragraph("5.3 Staff Assignment", styles['H2']))
    story.append(Paragraph(fmt(
        "Families are assigned to 12 staves below the Zeitnetz using round-robin: "
        "**Family N \u2192 Staff ((N \u2212 1) mod 12) + 1**. "
        "This distributes families evenly: Staves 1\u20133 receive 7 families each; Staves 4\u201312 receive 6 each."
    ), styles['BodyText2']))

    story.append(Paragraph("5.4 Results Summary", styles['H2']))
    results4 = [
        "**329 bars**, 3,947 grid positions",
        "**3 cyclic extensions** beyond the original 12 rows",
        "**75/75 families** activated via sequential scan",
        "Family spans range from F2 (2 events, pos 39\u219245) to F75 (18 events, pos 3172\u21923258)",
    ]
    for r in results4:
        story.append(Paragraph(fmt(f"\u2022 {r}"), styles['BulletItem']))

    # ══════════════════════════════════════════════════════════════════
    # 6. ZEITNETZ V2
    # ══════════════════════════════════════════════════════════════════
    story.append(PageBreak())
    story.append(Paragraph("6. Zeitnetz Version 2 \u2014 Variable Time Signatures", styles['H1']))
    story.append(Paragraph(fmt(
        '**Function:** `export_zeitnetz_v2()` \u2014 **Export:** `zeitnetz_v2.musicxml`'
    ), styles['MetaInfo']))

    story.append(Paragraph("6.1 Concept", styles['H2']))
    story.append(Paragraph(fmt(
        "Every bar from Version 1 (uniform 3/8) is transformed by assigning one of 7 time signature types. "
        "The crucial principle: **each bar retains exactly 12 internal grid positions**, but the basic rhythmic "
        "unit changes proportionally to the bar\u2019s total duration."
    ), styles['BodyText2']))

    story.append(Paragraph("6.2 The Seven Time Signature Types", styles['H2']))
    story.append(make_table(
        ["Type", "Time Sig.", "Unit (bar / 12)", "Notation"],
        [
            ["1", "3/8", "1/32 (thirty-second note)", "Standard \u2014 unchanged from V1"],
            ["2", "4/8", "1/24 (sixteenth-note triplet)", "Tuplet: 3:2 sixteenths per beat"],
            ["3", "3/4", "1/16 (sixteenth note)", "Standard \u2014 double V1 durations"],
            ["4", "4/4", "1/12 (eighth-note triplet)", "Tuplet: 3:2 eighths per beat"],
            ["5", "3/2", "1/8 (eighth note)", "Standard"],
            ["6", "4/2", "1/6 (quarter-note triplet)", "Tuplet: 3:2 quarters per beat"],
            ["7", "12/4", "1/4 (quarter note)", "Standard \u2014 8\u00d7 V1 durations"],
        ],
        col_widths=[12*mm, 18*mm, 45*mm, 90*mm]
    ))
    story.append(Spacer(1, 4*mm))

    story.append(Paragraph("6.3 The 105-Bar Cyclic Sequence", styles['H2']))
    story.append(Paragraph(fmt(
        "The time signatures follow a 105-bar pattern applied cyclically to all 329 bars:"
    ), styles['BodyText2']))
    story.append(Paragraph(
        "7,6,6,5,5,5,4,4,4,4,3,3,3,3,3,2,2,2,2,2,2,<br/>"
        "1,1,1,1,1,1,1,1,1,1,1,1,1,1,<br/>"
        "2,2,2,2,2,2,2,3,3,3,3,3,3,3,4,4,4,4,4,4,4,<br/>"
        "5,5,5,5,5,5,5,6,6,6,6,6,6,6,<br/>"
        "7,7,7,7,7,7,7,7,7,7,7,7,7,7,<br/>"
        "6,6,6,6,6,6,5,5,5,5,5,4,4,4,4,3,3,3,2,2,1",
        styles['CodeBlock']))
    story.append(Paragraph(fmt(
        "The pattern has a characteristic **wedge/arch shape**: (1) **Descent** (bars 1\u201335): From type 7 "
        "(slowest) down to type 1 (fastest), with increasing repetitions as types get smaller. "
        "(2) **Ascent** (bars 36\u201384): Back up from type 1 to type 7. "
        "(3) **Descent** (bars 85\u2013105): A shorter, accelerating contraction back to type 1."
    ), styles['BodyText2']))

    story.append(Paragraph("6.4 Tuplet Implementation", styles['H2']))
    story.append(Paragraph(fmt(
        "For types 2, 4, and 6, each bar\u2019s 12 grid positions are grouped into **4 groups of 3** (one per beat). "
        "Each group receives explicit tuplet brackets (3:2 ratio). When an entire group consists of rests, "
        "it is written as a standard beat-length rest without tuplet markup."
    ), styles['BodyText2']))

    story.append(Paragraph("6.5 Results Summary", styles['H2']))
    v2_results = [
        "**329 bars** (same count as V1, but with varied durations)",
        "**13 staves** (same structure as Stage 4)",
        "Bar type distribution: Type 1: 45, Type 2: 45, Type 3: 49, Type 4: 49, Type 5: 48, Type 6: 47, Type 7: 46",
        "Time signatures written only when they change",
    ]
    for r in v2_results:
        story.append(Paragraph(fmt(f"\u2022 {r}"), styles['BulletItem']))

    # ══════════════════════════════════════════════════════════════════
    # 7. ZEITNETZ FINAL
    # ══════════════════════════════════════════════════════════════════
    story.append(PageBreak())
    story.append(Paragraph("7. Zeitnetz Final \u2014 Duration as Count", styles['H1']))
    story.append(Paragraph(fmt(
        '**Function:** `export_zeitnetz_final()` \u2014 **Export:** `zeitnetz_final.musicxml`'
    ), styles['MetaInfo']))

    story.append(Paragraph("7.1 Concept", styles['H2']))
    story.append(Paragraph(fmt(
        "This is Lachenmann\u2019s final transformation of the time-grid, as described by Pena:"
    ), styles['BodyText2']))
    story.append(Paragraph(
        "\u201cLachenmann\u2019s final step in generating the time-grid consists in multiplying each sound family. "
        "The durations of the tones in each family are used to COUNT NOTES in the time-grid in terms of "
        "pitches; that is, for example, what previously lasted 6 thirty-second notes now corresponds to "
        "the duration of 6 notes of the time-grid.\u201d",
        styles['Quote']))

    story.append(Paragraph("7.2 Algorithm", styles['H2']))
    algo_steps = [
        "**Retrieve** the family\u2019s entries from the Stage 4 sequential scan, including the Zeitnetz event index and duration of each entry",
        "**First entry** remains at its original Zeitnetz event index",
        "**Subsequent entries:** from the current event index, advance forward by the previous entry\u2019s duration value (counting Zeitnetz events in staff 1)",
        "**Pitch:** each entry takes the pitch of the Zeitnetz event it lands on (NOT the original Stage 4 pitch)",
    ]
    for i, s in enumerate(algo_steps):
        story.append(Paragraph(fmt(f"{i+1}. {s}"), styles['NumberedItem']))

    story.append(Paragraph(fmt("**Concrete example (Family 1):**"), styles['BodyText2']))
    story.append(Paragraph(
        "Stage 4 durations: [6, 9, 7, 6, 6, 4, 3, 10]<br/>"
        "Entry 1.1: Zeitnetz event index 0 (position 11, pitch cis)<br/>"
        "Entry 1.2: index 0 + 6 = 6<br/>"
        "Entry 1.3: index 6 + 9 = 15<br/>"
        "Entry 1.4: index 15 + 7 = 22<br/>"
        "...and so on",
        styles['CodeBlock']))

    story.append(Paragraph("7.3 Greedy Staff Assignment", styles['H2']))
    story.append(Paragraph(fmt(
        "Unlike Stage 4\u2019s fixed round-robin assignment, the final version uses a **greedy interval scheduler** "
        "to minimise the number of staves: (1) Compute each family\u2019s time span. (2) Sort families by start "
        "position. (3) For each family, assign it to the first staff whose last family ends before this family "
        "starts. (4) If no staff has room, create a new one. This is the classic interval scheduling algorithm "
        "guaranteeing the minimum number of staves for non-overlapping spans."
    ), styles['BodyText2']))

    story.append(Paragraph("7.4 Event Labelling", styles['H2']))
    story.append(Paragraph(fmt(
        'Every note in the family staves carries a lyric in the format **"F.E"** where F is the family number '
        'and E is the event number within that family (1-based). For example: "1.1" for the first event of '
        'Family 1, "35.6" for the sixth event of Family 35.'
    ), styles['BodyText2']))

    story.append(Paragraph("7.5 Results Summary", styles['H2']))
    final_results = [
        "**14 total staves** (1 Zeitnetz + 13 family staves \u2014 only 1 more than Stage 4)",
        "**313 bars**",
        "**75/75 families** placed, all entries computed",
        "Maximum grid position: 3,745",
        "The greedy scheduler packed 75 families into just 13 staves",
        "Variable time signatures from the V2 cyclic sequence applied throughout",
        "**The output matches the final pages of Pena\u2019s Diplomarbeit**, confirming the correctness of the entire pipeline",
    ]
    for r in final_results:
        story.append(Paragraph(fmt(f"\u2022 {r}"), styles['BulletItem']))

    story.append(Paragraph("7.6 Family Spread Comparison", styles['H2']))
    story.append(make_table(
        ["Family", "Stage 4 Span", "Final Span", "Entries"],
        [
            ["F1", "pos 11 \u2192 62", "pos 11 \u2192 334", "9"],
            ["F7", "pos 300 \u2192 381", "pos 300 \u2192 883", "14"],
            ["F38", "pos 1632 \u2192 1757", "pos 1632 \u2192 2478", "15"],
            ["F75", "pos 3172 \u2192 3258", "pos 3172 \u2192 3745", "18"],
        ],
        col_widths=[20*mm, 40*mm, 40*mm, 20*mm]
    ))

    # ══════════════════════════════════════════════════════════════════
    # 8. OUTPUT FILES
    # ══════════════════════════════════════════════════════════════════
    story.append(PageBreak())
    story.append(Paragraph("8. Output Files", styles['H1']))
    story.append(make_table(
        ["File", "Stage", "Staves", "Bars", "Description"],
        [
            ["zeitnetz_stage1.musicxml", "1", "12", "2 each", "Pitch & rhythm permutations"],
            ["zeitnetz_stage2.musicxml", "2", "1", "~83", "Zeitnetz V1 (12 rows, 3/8)"],
            ["zeitnetz_stage3_1a_rows.musicxml", "3.1", "1", "12", "Klangfamilien by row order"],
            ["zeitnetz_stage3_1b_families.musicxml", "3.1", "1", "12", "Klangfamilien by family order"],
            ["zeitnetz_stage3_2.musicxml", "3.2", "1", "8", "75 start\u2192end bi-chords"],
            ["zeitnetz_stage4_score.musicxml", "4", "13", "329", "Full score, uniform 3/8"],
            ["zeitnetz_v2.musicxml", "V2", "13", "329", "Variable time signatures"],
            ["zeitnetz_final.musicxml", "Final", "14", "313", "Duration-as-count, variable TS"],
        ],
        col_widths=[55*mm, 12*mm, 14*mm, 14*mm, 70*mm]
    ))

    # ══════════════════════════════════════════════════════════════════
    # 9. TECHNICAL ARCHITECTURE
    # ══════════════════════════════════════════════════════════════════
    story.append(Spacer(1, 6*mm))
    story.append(Paragraph("9. Technical Architecture", styles['H1']))

    story.append(Paragraph("9.1 Single-File Pipeline", styles['H2']))
    story.append(Paragraph(fmt(
        'The entire system is contained in `zeitnetz_pipeline.py`, structured as: '
        '(1) Shared pitch utilities \u2014 conversion tables, parsers. '
        '(2) Stage functions \u2014 `run_stage1()` through `run_stage5()`, plus `run_stage3_2()`. '
        '(3) Export functions \u2014 one per output file. '
        '(4) Console print functions \u2014 formatted summaries per stage. '
        '(5) Main entry point \u2014 argument parsing and sequential execution.'
    ), styles['BodyText2']))

    story.append(Paragraph("9.2 Key Design Decisions", styles['H2']))
    decisions = [
        "**Integer arithmetic throughout.** All grid positions are computed as integers (32nd-note units). "
        "MusicXML offsets use Python\u2019s `Fraction` type to avoid floating-point drift. This was essential \u2014 "
        "early implementations suffered from cumulative rounding errors over 329+ bars.",
        "**Manual measure construction.** Rather than relying on music21\u2019s automatic measure filling (which "
        "introduced positioning errors), all measures are constructed manually with explicit `m.insert(offset, element)` calls.",
        "**Cyclic extension with termination test.** The Zeitnetz is extended one cycle at a time, with a "
        "full sequential scan test (`_test_all_families_done()`) after each cycle. A safety cap of 10 cycles prevents infinite loops.",
        "**Self-contained export functions.** Each export function regenerates its own data from the Stage 2 "
        "and Stage 3.2 inputs, rather than depending on mutable shared state.",
    ]
    for d in decisions:
        story.append(Paragraph(fmt(f"\u2022 {d}"), styles['BulletItem']))

    story.append(Paragraph("9.3 Algorithms Summary", styles['H2']))
    story.append(make_table(
        ["Algorithm", "Stage", "Purpose"],
        [
            ["Permutation matrix construction", "1", "Generate 12\u00d712 transformation matrix"],
            ["Onset address computation", "1", "Map duration list to matrix addresses"],
            ["Circular forward scanning", "2", "Derive durations from pitch distances"],
            ["Target-based row reading", "3.1", "Extract 75 family starting pitches"],
            ["Reverse complementary pairing", "3.2", "Assign end pitches to families"],
            ["Sequential activation scan", "4", "Activate/deactivate families over Zeitnetz"],
            ["Same-pitch deactivation rule", "4", "Handle families with identical start/end PC"],
            ["Cyclic Zeitnetz extension", "4, Final", "Extend time-grid until all families complete"],
            ["Tuplet grouping (3 per beat)", "V2, Final", "Proper bracket notation for triplet bars"],
            ["Duration-as-count transformation", "Final", "Convert durations to event-skip counts"],
            ["Greedy interval scheduling", "Final", "Minimise family staves"],
        ],
        col_widths=[55*mm, 18*mm, 92*mm]
    ))

    # ══════════════════════════════════════════════════════════════════
    # 10. USAGE
    # ══════════════════════════════════════════════════════════════════
    story.append(PageBreak())
    story.append(Paragraph("10. Usage", styles['H1']))
    story.append(Paragraph(
        "# Run full pipeline with default Lachenmann values<br/>"
        "python3 zeitnetz_pipeline.py --export<br/><br/>"
        "# Custom pitch row (German names)<br/>"
        'python3 zeitnetz_pipeline.py --pitches "cis h c gis a dis fis e d ais f g" --export<br/><br/>'
        "# Custom pitch row (integers)<br/>"
        'python3 zeitnetz_pipeline.py --pitches "0 1 2 3 4 5 6 7 8 9 10 11" --export',
        styles['CodeBlock']))

    story.append(Paragraph("Arguments", styles['H2']))
    story.append(make_table(
        ["Argument", "Default", "Description"],
        [
            ["--pitches", '"1 11 0 8 9 3 6 4 2 10 5 7"', "12 pitch classes (integers or German names)"],
            ["--perm", '"1 5 0 6 2 7 11 8 3 10 4 9"', "Permutation pattern (12 integers, 0-indexed)"],
            ["--durations", '"\u221211 6 9 7 6 6 4 3 10 6 3 1 10"', "Duration list (13 integers; first may be negative)"],
            ["--axis", "pitch_row[0]", "Symmetry axis pitch class 0\u201311"],
            ["--export", "off", "Write MusicXML files for all stages"],
        ],
        col_widths=[25*mm, 55*mm, 85*mm]
    ))

    # ══════════════════════════════════════════════════════════════════
    # APPENDIX
    # ══════════════════════════════════════════════════════════════════
    story.append(Spacer(1, 10*mm))
    story.append(HRFlowable(width="100%", thickness=0.5, color=HexColor('#888899')))
    story.append(Spacer(1, 4*mm))
    story.append(Paragraph("Appendix: Development History", styles['H1']))
    story.append(Paragraph(fmt(
        "This pipeline was developed across multiple collaborative sessions between Paulo de Assis "
        "and Claude (Anthropic) in March 2026:"
    ), styles['BodyText2']))
    sessions = [
        "**Session 1 (March 17):** Stages 1\u20133 implemented and verified against Pena\u2019s analysis. Initial standalone scripts per stage.",
        "**Session 2 (March 18\u201319):** Consolidation into single pipeline file. Stage 4 (Netz-Familien) and Stage 5 (Final Netz) implemented following Pena\u2019s OpenMusic patch descriptions.",
        "**Session 3 (March 20):** Complete rewrite of Stage 4 as Full Score with cyclic Zeitnetz extension, sequential scan family activation, same-pitch deactivation rule, and round-robin staff assignment. Resolved the critical 25/75 activation problem through cyclic extension. Cleanup of outdated files.",
        "**Session 4 (March 21):** Zeitnetz Version 2 with variable time signatures (7 types, 105-bar cyclic sequence, tuplet notation). Zeitnetz Final with duration-as-count transformation, greedy staff assignment, and event labelling. Final verification against Pena\u2019s Diplomarbeit confirmed correctness.",
    ]
    for s in sessions:
        story.append(Paragraph(fmt(f"\u2022 {s}"), styles['BulletItem']))

    story.append(Spacer(1, 15*mm))
    story.append(HRFlowable(width="40%", thickness=0.3, color=HexColor('#aaaabb')))
    story.append(Spacer(1, 4*mm))
    story.append(Paragraph("Report generated: 21 March 2026", styles['Footer']))
    story.append(Paragraph(
        "Pipeline version: zeitnetz_pipeline.py (single source, ~2270 lines)", styles['Footer']))
    story.append(Paragraph(
        "Validation: Output matches final pages of Pena\u2019s bachelor thesis", styles['Footer']))

    return story


def main():
    doc = SimpleDocTemplate(
        OUTPUT,
        pagesize=A4,
        leftMargin=20*mm,
        rightMargin=20*mm,
        topMargin=18*mm,
        bottomMargin=18*mm,
        title="Zeitnetz Generator \u2014 Full Technical Report",
        author="Paulo de Assis & Claude (Anthropic)",
    )
    story = build_story()
    doc.build(story)
    print(f"PDF saved: {OUTPUT}")


if __name__ == "__main__":
    main()
