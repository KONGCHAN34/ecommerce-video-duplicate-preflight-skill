# Initial Issue Backlog

## 1. Add perceptual frame hashing for near-duplicate detection

Background: v0.1 uses exact hashes and conservative metadata signals. It cannot detect many cropped, watermarked, or re-encoded variants.

Goal: Add optional frame sampling and perceptual hash comparison.

Acceptance criteria:

- Sampling interval is documented.
- Thresholds are configurable.
- Reports explain frame-hash limitations.
- Existing read-only behavior is preserved.

Labels: `enhancement`, `detection`
Milestone: `v0.2.0`

## 2. Add side-by-side thumbnail contact sheets

Background: Human reviewers need quick visual evidence for candidate groups.

Goal: Generate optional contact sheets for near-duplicate groups.

Acceptance criteria:

- Contact sheets are opt-in.
- No source media is modified.
- Report links to generated images.

Labels: `enhancement`, `reporting`
Milestone: `v0.2.0`

## 3. Improve risk scoring explanation

Background: Content teams need plain-language explanations for risk levels.

Goal: Make report recommendations easier for non-technical reviewers.

Acceptance criteria:

- README and report format define risk levels.
- Expected outputs include clear examples.
- No platform approval guarantees are introduced.

Labels: `documentation`, `reporting`
Milestone: `v0.1.1`

## 4. Add JSON schema for results.json

Background: Teams may want to feed report output into dashboards or spreadsheets.

Goal: Document the JSON format with a simple schema.

Acceptance criteria:

- Schema is committed under `docs/`.
- Validation script checks required top-level fields.
- Usage docs link to the schema.

Labels: `documentation`, `tooling`
Milestone: `v0.2.0`

## 5. Add Windows setup notes

Background: Editing and e-commerce teams may run the tool on Windows machines.

Goal: Document Python and FFmpeg setup on Windows.

Acceptance criteria:

- Installation docs include Windows notes.
- Common path quoting issues are covered.
- Validation command is included.

Labels: `documentation`, `windows`
Milestone: `v0.1.1`

## 6. Add ffprobe diagnostics

Background: Missing or failing ffprobe can confuse users.

Goal: Make dependency warnings more actionable.

Acceptance criteria:

- Report says whether ffprobe was missing or failed per file.
- Usage docs explain how to verify ffprobe.
- Scanner keeps working without ffprobe.

Labels: `bug`, `usability`
Milestone: `v0.1.1`

## 7. Add editing-team threshold guidance

Background: Editing teams need guidance on when a version is meaningfully different.

Goal: Add a practical review checklist for re-edits.

Acceptance criteria:

- Docs include questions for scene, angle, script, audio, and structure changes.
- Example output references the checklist.

Labels: `documentation`, `workflow`
Milestone: `v0.2.0`

## 8. Add optional CSV export

Background: Content operators often review assets in spreadsheets.

Goal: Export recommendations as CSV.

Acceptance criteria:

- CLI flag writes `recommendations.csv`.
- CSV contains file, risk, action, reason.
- Docs include example command.

Labels: `enhancement`, `reporting`
Milestone: `v0.2.0`

## 9. Collect feedback from content and editing teams

Background: The workflow needs real-world validation.

Goal: Gather public-safe feedback without sharing private media.

Acceptance criteria:

- Feedback template exists.
- At least three public-safe feedback issues are linked in release notes before claiming external feedback.

Labels: `feedback`, `maintenance`
Milestone: `v0.2.0`

## 10. Prepare v0.2.0 release

Background: The first release establishes the repository; the next should improve detection depth.

Goal: Plan and ship the first detection improvement release.

Acceptance criteria:

- Milestone scope is finalized.
- Changelog is updated.
- Validation passes.
- Release notes include limitations.

Labels: `release`, `maintenance`
Milestone: `v0.2.0`

