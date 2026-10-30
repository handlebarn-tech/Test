# REVIEW-W1 — Independent review of wave 1 (REF-001, MIG-001, BUILD-001)

**Role:** REVIEW · **Priority:** P0 · **Branch:** check out `review/wave-1` in its own worktree. Read-only, except your review file and the fixes listed below.

## Goal
Decide GO / NO-GO for merging `review/wave-1` into `main`. Give your own independent read: check the work against the packets and sources, not against the workers' summaries.

## Inputs
- Packets: `Docs/Tasks/Review/{REF-001,MIG-001,BUILD-001}.md` (the acceptance criteria).
- Handoffs: `Docs/Handoffs/*.md`, `Docs/BUILD_STATUS.md`.
- Deliverables: `Docs/REFERENCES_INDEX.md`, `References/Index/`, `Docs/Reconstruction/*`, `Docs/KNOWN_GAPS.md`, `UnityProject/`, `Tools/Studio/studio.ps1`, `.gitattributes`, `.gitignore`.
- Sources for spot checks: `References/Floor Plan.pdf` and the CCTV/BAND images; `C:/Users/handl/Downloads/tfs-budtender/deploy/2026-10-30-v7114/site/index.html`. That folder is **read-only and belongs to another live project**; no PII (DEC-006).

## Checks
1. **REF-001:**
   - Every reference file is indexed and every plan room is in the coverage matrix.
   - Re-derive the plan scale and 3 room dimensions yourself from the PDF.
   - Spot-check 4 CCTV tile mappings and 3 photo rows.
   - No personal identification of staff.
2. **MIG-001:**
   - Pick 10 constants/coefficients from RECONSTRUCTION_CONTRACT.md; confirm each at its cited line in index.html.
   - Re-run the golden harness (from the GOLDEN_CASES.md appendix, in your temp dir); confirm `golden_cases.json` reproduces byte-identically or explain the diff.
   - Check the triage for any PII/CRM feature that wasn't dropped.
   - Check that the slice subset is enough for GAME-001.
3. **BUILD-001:**
   - Run `powershell -NoProfile -ExecutionPolicy Bypass -File Tools/Studio/studio.ps1 doctor`, then `unity-compile`, then `unity-test-edit`. Run `unity-build` too if time allows; it takes about 7 min.
   - Confirm `Dispo.Domain` has `noEngineReferences: true`.
   - Confirm `Library/`, `Temp/` and `UserSettings/` are not tracked.
   - Run only one Unity instance at a time.
4. **Repo hygiene:** no PII, no secrets, no files over 10 MB, no tfs-budtender files copied in.

## Owns
- `Docs/Reviews/REVIEW-W1.md`: verdict, findings by severity, evidence.
- You may fix trivial doc errors on `review/wave-1` and commit them there. Send anything bigger back as a finding.

## Done when
`Docs/Reviews/REVIEW-W1.md` is committed on `review/wave-1` with a GO / GO-with-notes / NO-GO verdict. Report the verdict and a ≤15-line summary to the Studio Hub. The Hub merges.
