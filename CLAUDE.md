## Agent skills

### Issue tracker

Issues are tracked in GitHub Issues for this repo (via the `gh` CLI). See `docs/agents/issue-tracker.md`.

### Triage labels

Default vocabulary: `needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `wontfix`. See `docs/agents/triage-labels.md`.

### Domain docs

Single-context: one `CONTEXT.md` and `docs/adr/` at the repo root. See `docs/agents/domain.md`.

### Modalità di risposta

- `/ponytail`: sempre attiva in ogni thread (livello full), salvo "stop ponytail".
- `/caveman`: spenta di default; si attiva solo quando l'utente la chiede ("caveman", "megacave"), e si spegne con "stop caveman".
