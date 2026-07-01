# tools/

Python scripts for deterministic execution (Layer 3 of the WAT framework).

- One script per task. Each script reads inputs, does the work, writes outputs.
- Read API keys and secrets from `../.env` (never hardcode).
- Intermediate files belong in `../.tmp/`. Final deliverables go to cloud services.
- When a script fails: fix the script, retest, then update the related workflow in `../workflows/` with what you learned.
