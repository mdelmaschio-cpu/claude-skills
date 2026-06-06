---
name: personal-workflow
description: "Workflow personale del maintainer di claude-skills. Contiene preferenze operative, regole git, convenzioni del repository e stile di interazione. Carica questo skill all'inizio di ogni sessione sul repository claude-skills per evitare di ridefinire il contesto ogni volta. Use when starting work on the claude-skills repository, when creating or editing skills/plugins, or when performing repository maintenance."
license: MIT
argument-hint: "Attività specifica per cui caricare il contesto"
metadata:
  version: 1.0.0
  maintainer: "M. Delmaschio <m.delmaschio@eureka-market.com>"
  repo: "mdelmaschio-cpu/claude-skills"
  last_updated: "2026-06-06"
---

# Personal Workflow — claude-skills

Questo skill documenta le preferenze operative del maintainer per il lavoro sul repository `claude-skills`. Quando è attivo, Claude deve applicare tutte le regole seguenti senza che vengano ripetute ogni sessione.

---

## Lingua e comunicazione

- **Rispondo sempre in italiano**, anche se il codice, i commit, i file e i comandi sono in inglese.
- Risposte **concise**: frasi brevi, niente spiegazioni ridondanti. Una frase per aggiornamento è sufficiente.
- Niente emoji salvo richiesta esplicita.
- Quando è necessario proporre un piano, farlo in 2-3 frasi con raccomandazione e trade-off principale — poi aspettare conferma prima di implementare.

---

## Regole git — non negoziabili

### Branch strategy

```
feature/* → dev → main  (solo via PR)
```

- **Mai push diretto su `main`** — main è protetto, richiede PR con approvazione.
- **Sempre partire da `dev`** per creare nuovi branch: `git checkout dev && git pull origin dev && git checkout -b feature/<nome>`.
- Naming convention branch: `feature/<domain>-<nome>` (es. `feature/personal-workflow`, `feature/agents-cs-new-skill`).

### Conventional commits (obbligatori)

```
feat(<scope>): descrizione
fix(<scope>): descrizione
docs(<scope>): descrizione
refactor(<scope>): descrizione
chore(<scope>): descrizione
```

Scope = cartella/dominio principale modificato (es. `agents`, `engineering`, `personal`, `scripts`).

### PR verso dev

Dopo il push, aprire sempre una **PR verso `dev`** (mai verso `main`). Il flusso periodico `dev → main` è gestito separatamente.

---

## Prima di azioni rischiose: chiedere conferma

Richiedere conferma esplicita prima di:

- Qualsiasi `git reset --hard`, `git push --force`, `git branch -D`
- Cancellazione di file o cartelle
- Modifiche a `.gitignore`, `CLAUDE.md`, `marketplace.json`, `settings.json`
- Push su branch già aperti come PR
- Operazioni che toccano più di 10 file contemporaneamente

**Non chiedere conferma per**: lettura di file, ricerche, grep, script `--help`, commit standard.

---

## Ruolo e contesto

- **Solo maintainer** — non ci sono altri collaboratori attivi. Non serve coordinamento con altri.
- Il repository è una **libreria di skill pubbliche** per Claude Code, non un'applicazione tradizionale.
- Versione corrente: **v2.9.0 + unreleased** (vedi CLAUDE.md per dettagli).
- 63 plugin nel marketplace, 339 skill su 16 domini.

---

## Convenzioni del repository

### Struttura skill (Path-B, 11 file)

```
<domain>/<plugin-name>/
├── .claude-plugin/plugin.json    # manifesto plugin
├── README.md
├── agents/cs-<name>.md           # agente cs-*
├── commands/cs-<name>.md         # slash command
└── skills/<skill-name>/
    ├── SKILL.md                  # YAML frontmatter + corpo skill
    ├── references/               # 3+ doc di riferimento (5-7 fonti ciascuno)
    ├── assets/                   # template e esempi
    └── scripts/                  # 3 strumenti Python stdlib-only
```

### plugin.json — regole obbligatorie

- `skills` deve sempre usare il prefisso `./` (es. `["./skills/skill-name"]`)
- Nessuna dipendenza da servizi a pagamento senza BYOK esplicito
- Versione allineata al repo (attuale: `2.9.0`)

### Script Python

- Solo stdlib (niente pip install obbligatorio)
- Sempre supporto `--help` e `--sample`
- Zero chiamate LLM nei tool
- Exit 0 su `--help`, exit 1 su errore

### Agenti (`agents/cs-*.md`)

- Prefix obbligatorio `cs-`
- Frontmatter YAML: `name`, `description`, `tools`
- Path relativi (non assoluti) per `skills:` nelle reference

---

## Flusso tipico di lavoro

1. `git checkout dev && git pull origin dev`
2. `git checkout -b feature/<scope>-<nome>`
3. Lavoro: crea/modifica file
4. `git add <file specifici>` (mai `git add -A` senza revisione)
5. Commit conventional: `feat(<scope>): <descrizione>`
6. `git push -u origin feature/<scope>-<nome>`
7. PR verso `dev` con titolo < 70 caratteri

---

## Comandi utili del repository

```bash
# Audit plugin (8 fasi)
python scripts/check_plugin_json.py --all

# Sincronizzazione Codex
python scripts/sync-codex-skills.py

# Sincronizzazione Vibe (Mistral)
python scripts/sync-vibe-skills.py

# Audit skill
python scripts/audit_skills.py
```

---

## Riferimenti

- [CLAUDE.md](../../../../CLAUDE.md) — guida principale del repository
- [standards/git/git-workflow-standards.md](../../../../standards/git/git-workflow-standards.md) — standard commit e branch
- [.claude-plugin/marketplace.json](../../../../.claude-plugin/marketplace.json) — registro plugin
