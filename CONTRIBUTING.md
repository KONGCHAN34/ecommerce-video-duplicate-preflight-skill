# Contributing

Thank you for improving this project. The main rule is simple: keep the workflow useful, truthful, and safe for public repositories.

## Open An Issue

Use an issue when you want to:

- Report a bug in the scanner or validation workflow.
- Suggest a new duplicate-detection signal.
- Improve report wording or examples.
- Add setup notes for a new platform.

Do not attach private videos, credentials, cookies, tokens, customer material, platform screenshots with account data, or unpublished business data.

## Submit A Pull Request

Recommended branch names:

- `fix/report-risk-wording`
- `feat/perceptual-hash-sampling`
- `docs/windows-installation`
- `test/scanner-fixtures`

Commit message style:

```text
feat: add frame sampling plan
fix: handle unreadable video files
docs: clarify platform disclaimer
test: add repository validation case
```

## Review Standard

Pull requests should:

- Preserve read-only input media behavior.
- Avoid guaranteed platform approval or copyright claims.
- Update docs and examples when workflow behavior changes.
- Include validation output or a clear reason validation could not run.
- Avoid adding heavyweight dependencies without a clear reason.

## Local Validation

Run:

```bash
python3 scripts/validate_repository.py
python3 .agents/skills/ecommerce-video-preflight/scripts/scan_video_duplicates.py --help
```

If scanner behavior changes, run it against a non-private test folder and include the command used.

