# Paper Revision — Changes after Feedback Session with Adam Lukawski

**Date:** 2026-03-30 (Zoom session)
**Paper:** Vibe Coding the Zeitnetz
**Status:** Working document — to guide rewriting after Switzerland trip

---

## CHANGES — Clear and Actionable

### 1. Reframe the paper's identity
- **From:** software development / technical report
- **To:** artistic research — the generative gesture, the concept of "machine" (Deleuze/Guattari machinic assemblage), the philosophical implications of reversing Pena's analytical direction into a generative one

### 2. Modular structure
- Separate the paper into distinct modules for distinct readers:
  - **Aesthetic/methodological layer** — artistic research framing, the gesture, the machine concept, faith in combinatorial organization
  - **Compositional procedures** — the 5 stages, Lachenmann's method, Pena's analysis
  - **Technical documentation** — Python code, music21, MusicXML specifics
- These can be sections, or the technical part can migrate to a separate document (GitHub README / technical report)

### 3. Add web app link prominently
- Place a working link to the Netlify web application (the "Lachenmann Zeitnetz Generator") at the **beginning** of the paper, so the reader can immediately see and interact with the output

### 4. New section: Heuristic search and validation
- Dedicated section on the discovery/validation mode — the fact that reversing Pena's analysis into a generator revealed that not all input combinations work, requiring heuristic search (collision-free duration lists, testing rotations and transpositions)
- This is a **critical differentiator** from Pena's work and a genuine research finding

### 5. Correct the Pena/Cavallotti attribution
- Acknowledge that Pena built upon Cavallotti's foundational research (*Differenzen*, 2006; and the 2004 Italian chapter)
- Integrate Cavallotti into the paper's narrative, not just the references

### 6. Remove unnecessary technical details
- Cut things like "approximately 2,000 lines of code" — line count says nothing about complexity or quality
- Review for other developer-speak that doesn't serve the paper's readers

### 7. Clarify the gesture for unfamiliar readers
- Add a passage early on that "takes the reader by the hand" — explains what this paper actually *does* and *why*, before diving into stages
- Currently the paper assumes too much context

### 8. Distinguish from set theory tradition
- Make explicit that Lachenmann's method is **not** pitch-class set theory (Forte, Lewin, Babbitt). He borrows only the 0–11 numbering; the permutations are simpler and serve a different purpose (temporal scaffolding, not pitch-class analysis)

### 9. GitHub repository cleanup
- Organize examples into a separate subfolder
- Consider a standalone technical report in the repo (separate from the paper)

---

## CHANGES — To Be Decided

### 10. Journal target
- **Open question:** Is there an appropriate venue for this interdisciplinary work (musicology + software + artistic research)?
- The repository itself is a valid output regardless of publication

### 11. AI acknowledgment / vibe coding disclosure
- **Tension:** honesty about Claude's role vs. academic vulnerability
- Vibe coding is increasingly accepted in programming, but academia may be hostile
- **Decision needed:** How explicit to be? Current draft is very open about it

### 12. Max Bense reference
- Adam's suggestion (via Martin?) to reference Max Bense — to be evaluated for relevance to the combinatorial/aesthetic argument

### 13. Separate paper for the Epilogue material?
- The "combinatorial faith" / philosophy of listening discussion — does it stay as an Epilogue in this paper or become its own paper?

---

## NOT CHANGES — Confirmed Strengths

- The algorithmic explanation is **better than Pena's original** — clearer sequence, better notation examples
- The web application works and is a real output
- The generative reversal (analysis → generator) is a genuine contribution
- The code and repository stand as valid research outputs independent of the paper

---

## Timeline

- **Next step:** Review after Switzerland trip (Wednesday/Thursday)
- **Adam:** Will provide text-level edits on next version
