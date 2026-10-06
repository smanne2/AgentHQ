# Stack Detection (ambiguous cases)

Load this when the manifest files are missing, conflicting, or unfamiliar.

## Order of evidence
1. **Manifest files** — the strongest signal. `package.json` → node/ts;
   `pyproject.toml`/`setup.py`/`requirements.txt` → python; `go.mod` → go;
   `Cargo.toml` → rust; `pom.xml`/`build.gradle` → java; `composer.json` → php.
2. **File extensions** — a cluster of `.ts`/`.tsx` → typescript even without a
   devDependency on `typescript`; `.py` → python; etc.
3. **Config files** — `tsconfig.json`, `Dockerfile`, `.eslintrc`, `ruff.toml`
   narrow the language; CI config (`.github/workflows`) often names the toolchain.
4. **README / intent docs** — weakest; treat as a claim to verify, not a fact.

## Multiple stacks
If two or more stacks are genuinely present (polyglot, monorepo workspaces, a
server + client in one repo), document **both** and name which owns which
directory. Never collapse a polyglot repo into a single language.

## Still ambiguous
State exactly what you found and what is missing, mark the gap `[TODO]`, and add
an `[ASK USER]` question asking the owner to confirm the intended stack.
