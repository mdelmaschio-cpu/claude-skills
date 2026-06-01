# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Purpose

This is a **comprehensive skills library** for Claude AI and Claude Code — reusable, production-ready skill packages that bundle domain expertise, best practices, automation tools, and strategic frameworks. Each skill is a self-contained folder that teams can extract and deploy directly into their AI coding workflows.

**Key distinction:** This is NOT a traditional application. It is a library of skill packages meant to be extracted and used by teams in their own Claude Code, Codex, Gemini CLI, or other AI coding tool workflows.

**Current scope:** 338 production-ready skills across 16 top-level domains, 533 stdlib-only Python automation tools, 676 reference guides, 51+ cs-* agents, 87+ slash commands, distributed as 63 marketplace plugins across 13 AI coding platforms.

**This repository is not a monorepo app** — there is no build step, no test suite to run on every change, and no server. The `pyproject.toml` / `requirements-dev.txt` configure a `pytest` suite under the maintainer-local (gitignored) `tests/` directory.

---

## Directory Structure

```
claude-skills/
├── .claude-plugin/           # Plugin registry: marketplace.json
├── .claude/commands/         # Repo-local Claude Code slash commands (git, plugin-audit, etc.)
├── .codex/                   # Auto-generated Codex CLI skill indexes (do not edit manually)
├── .gemini/                  # Auto-generated Gemini CLI skill indexes (do not edit manually)
├── .hermes/                  # Auto-generated Hermes Agent skill tree (do not edit manually)
├── .vibe/                    # Auto-generated Mistral Vibe skill tree (do not edit manually)
├── .github/workflows/        # CI: quality gate, security audit, sync, release
├── agents/                   # 51+ standalone cs-* agents and persona agents
├── commands/                 # 87+ repo-wide slash command .md files
├── scripts/                  # Build/sync/install scripts (Python + bash)
├── standards/                # Communication, quality, git, security, documentation standards
├── templates/                # Reusable SKILL.md and plugin.json templates
├── docs/                     # MkDocs Material documentation site source
├── orchestration/            # Cross-skill orchestration patterns
├── assets/                   # Repo-level shared assets (icon.png, etc.)
│
│   — Domain folders (each contains skills as subfolders) —
├── engineering/              # 78 POWERFUL-tier advanced engineering skills
├── engineering-team/         # Core engineering role skills (code-reviewer, playwright-pro, etc.)
├── marketing-skill/          # 46+ marketing skills across 8 pods (incl. AEO)
├── c-level-advisor/          # 66 C-level advisory skills + founder-mode agents
├── product-team/             # 17 product skills (incl. apple-hig-expert)
├── ra-qm-team/               # 18 RA/QM compliance skills (ISO 13485, MDR, FDA, GDPR)
├── project-management/       # 9 PM skills + bundled Atlassian Remote MCP
├── business-growth/          # 5 business & growth skills + Python tools
├── business-operations/      # 7 internal-ops skills (orchestrator + 6 sub-skills)
├── commercial/               # 8 per-deal-economics skills (orchestrator + 7 sub-skills)
├── compliance-os/            # 9 compliance-OS skills
├── finance/                  # 4 finance skills + Python tools
├── productivity/             # 6 productivity skills (capture, email, reflect, handoff, andreessen, etc.)
├── marketing/                # 1 marketing skill (landing page generator)
└── research/                 # 8 academic research skills + 5 research-ops skills
    research-ops/             # Enterprise Research Operations (clinical, finance, market, product)
```

### Maintainer-local folders (gitignored — not in the public tree)

- `documentation/` — sprint plans, strategy, implementation roadmaps
- `eval-workspace/` — Tessl evaluation outputs
- `megaprompts/` — pre-skill draft specs (Path-B source material)
- `tests/` — pytest suite (run locally; not in CI)
- `.autoresearch/` — autoresearch agent workspace
- `AUDIT_REPORT.md` — internal audit snapshots

In-repo references to paths under these folders resolve locally for the maintainer but appear as dead links on GitHub. This is intentional.

---

## Key Files

| File | Role |
|------|------|
| `CLAUDE.md` | This file — AI assistant guidance |
| `CONVENTIONS.md` | **Mandatory rules** for every contributor (human or AI). Read before making any changes. |
| `CONTRIBUTING.md` | PR workflow, what is accepted, PR checklist |
| `SKILL-AUTHORING-STANDARD.md` | SKILL.md template and content DNA for new skills |
| `SKILL_PIPELINE.md` | Mandatory 10-phase production pipeline for new skills |
| `CHANGELOG.md` | Per-release notes (Keep a Changelog format) |
| `CODE_OF_CONDUCT.md` | Community conduct standards |
| `INSTALLATION.md` | Per-platform installation guides (Claude Code, Codex, Gemini CLI, Vibe, etc.) |
| `STORE.md` | Commercial bundles (Stan Store / Gumroad) |
| `.claude-plugin/marketplace.json` | Plugin registry — 63 plugins, auto-updated by maintainers |
| `mkdocs.yml` | MkDocs Material site config |
| `scripts/check_plugin_json.py` | Validates plugin.json files; runs in CI |
| `scripts/audit_skills.py` | Repo-wide SKILL.md quality validator |
| `scripts/generate-docs.py` | Auto-generates MkDocs pages from skill folders |
| `scripts/sync-codex-skills.py` | Syncs skills to `.codex/` tree |
| `scripts/sync-gemini-skills.py` | Syncs skills to `.gemini/` tree |
| `scripts/sync-hermes-skills.py` | Syncs skills to `.hermes/` tree |
| `scripts/sync-vibe-skills.py` | Syncs skills to `.vibe/` tree |

---

## Skill Package Pattern

Every skill is a directory following this layout:

```
<domain>/<skill-name>/
├── SKILL.md                # Required — main skill instructions (YAML frontmatter + content)
├── .claude-plugin/
│   └── plugin.json         # Optional — for standalone plugin install
├── scripts/                # Optional — deterministic Python CLI tools (stdlib only)
│   └── *.py
├── references/             # Optional — detailed knowledge base docs
│   └── *.md
└── assets/                 # Optional — templates and worked examples
```

**Knowledge flow:** `references/` → `SKILL.md` workflows → executed via `scripts/` → applied using `assets/` templates.

**Sub-skills** (nested `skills/` directories) exist in compound skills like `engineering-team/playwright-pro/`. Sub-skills are documented within their parent; they do not get their own marketplace plugins or platform sync entries.

---

## Development Setup

No build system or compilation step. All Python scripts use the standard library only — no `pip install` required to run any skill tool.

```bash
# Clone and explore
git clone https://github.com/alirezarezvani/claude-skills.git
cd claude-skills

# Run any skill script directly
python3 engineering/skill-tester/scripts/skill_validator.py <skill-path>

# Dev dependencies (maintainer only — for the gitignored tests/ suite)
pip install -r requirements-dev.txt   # pytest 8.x
pytest tests/
```

**Python requirements per script:**
- Python 3.10+
- Standard library only (`argparse`, `json`, `os`, `re`, `sys`, etc.)
- Must pass `python3 script.py --help`
- Must support `--json` flag for machine-readable output
- Exit codes: `0` = success, `1` = warnings, `2` = critical errors

---

## Git Workflow

**Branch strategy:** feature → dev → main (PR only, no direct pushes to main)

```bash
# 1. Start from dev
git checkout dev && git pull origin dev

# 2. Create feature branch
git checkout -b feature/<skill-name>   # new skill
git checkout -b fix/<description>       # bug fix
git checkout -b improve/<skill-name>    # enhancement
git checkout -b docs/<description>      # documentation

# 3. Commit using Conventional Commits
feat(engineering): add browser-automation skill
fix(self-improving-agent): use absolute path for hooks
improve(tdd-guide): add per-language examples
docs: update CONTRIBUTING.md
chore: sync codex/gemini indexes

# 4. Open PR targeting dev (never main)
gh pr create --base dev --head feature/<skill-name>
```

**Branch protection:** Main requires PR approval. PRs targeting `main` are auto-closed.

---

## CI/CD Workflows (`.github/workflows/`)

| Workflow | Trigger | What it does |
|----------|---------|--------------|
| `ci-quality-gate.yml` | Every PR | Lint, plugin.json validation (`check_plugin_json.py`), security audit, docs check |
| `skill-quality-review.yml` | PR | Runs skill validator + quality scorer on changed skill files |
| `skill-security-audit.yml` | PR | Zero-tolerance CRITICAL/HIGH security scan |
| `release.yml` | Push to main | Generates release notes, tags version |
| `smart-sync.yml` | PR merge | Syncs platform indexes (Codex, Gemini) |
| `claude-code-review.yml` | PR | Claude Code automated code review |
| `static.yml` | Push to main | Deploys MkDocs docs site to GitHub Pages |
| `enforce-pr-target.yml` | PR | Rejects PRs that target main instead of dev |

---

## CONVENTIONS.md Summary (Mandatory Rules)

Read the full [CONVENTIONS.md](CONVENTIONS.md). Key rules for AI agents:

### SKILL.md Frontmatter — two fields only
```yaml
---
name: "skill-name"
description: "Use when the user asks to [specific trigger]. Covers [key capabilities]."
---
```
**Do NOT add:** `license`, `metadata`, `triggers`, `version`, `author`, `category`, `updated`. PRs with extra frontmatter fields are rejected.

### SKILL.md Content Rules
- Under 500 lines — move detailed content to `references/`
- Opinionated — recommend specific approaches, don't list options
- Actionable — agent must be able to execute, not just advise
- Must include: Anti-Patterns section + Cross-References section

### plugin.json — required fields only
```json
{
  "name": "skill-name",
  "description": "...",
  "version": "2.x.x",
  "author": {"name": "Alireza Rezvani", "url": "https://alirezarezvani.com"},
  "homepage": "https://github.com/alirezarezvani/claude-skills/tree/main/<domain>/<skill>",
  "repository": "https://github.com/alirezarezvani/claude-skills",
  "license": "MIT",
  "skills": ["./"]
}
```
- `author` **must be an object** (never a string — causes install errors)
- `skills` paths **must start with `./`** — bare strings rejected by Claude Code 2.1.144+
- No extra fields: no `commands`, `hooks`, `triggers`, `tags`

### Python Script Rules
- stdlib only — no pip dependencies
- `argparse` + `--help` required
- `--json` flag required for machine-readable output
- No LLM/API calls — scripts must be deterministic
- `if __name__ == "__main__":` guard required

### What NOT to Do (PRs will be closed)
- Add external repo/tool links to README
- Skills requiring paid API keys
- Scripts with pip dependencies
- PRs targeting `main` instead of `dev`
- Modify `.codex/`, `.gemini/`, `marketplace.json` or index files (auto-generated)
- Change the official skill count field — it's curated

---

## Quality Validation

Run these before opening a PR:

```bash
# Structure validation
python3 engineering/skill-tester/scripts/skill_validator.py <skill-path> --json

# Quality scoring (minimum 75/100)
python3 engineering/skill-tester/scripts/quality_scorer.py <skill-path> --json

# Script smoke test
python3 engineering/skill-tester/scripts/script_tester.py <skill-path> --json

# Security audit (zero CRITICAL/HIGH required)
python3 engineering/skill-security-auditor/scripts/skill_security_auditor.py <skill-path> --strict

# Repo-wide plugin.json check (runs in CI)
python3 scripts/check_plugin_json.py --all

# Repo-wide skill audit
python3 scripts/audit_skills.py
```

---

## Domain Navigation Map

| Domain Folder | CLAUDE.md | Focus |
|---|---|---|
| `agents/` | [agents/CLAUDE.md](agents/CLAUDE.md) | cs-* agent creation, YAML frontmatter, relative paths |
| `marketing-skill/` | [marketing-skill/CLAUDE.md](marketing-skill/CLAUDE.md) | Content creation, SEO, AEO, ASO, demand gen, analytics |
| `product-team/` | [product-team/CLAUDE.md](product-team/CLAUDE.md) | RICE, OKRs, user stories, UX research |
| `engineering-team/` | [engineering-team/CLAUDE.md](engineering-team/CLAUDE.md) | Core engineering roles, code review, Playwright, security |
| `engineering/` | [engineering/](engineering/) | 78 POWERFUL-tier skills: AgentHub, autoresearch, RAG, MCP, etc. |
| `c-level-advisor/` | [c-level-advisor/CLAUDE.md](c-level-advisor/CLAUDE.md) | CEO/CTO/CFO/CMO/CAIO/CDO/CCO/VPE strategic advisory |
| `project-management/` | [project-management/CLAUDE.md](project-management/CLAUDE.md) | Atlassian MCP, Jira/Confluence integration |
| `ra-qm-team/` | [ra-qm-team/CLAUDE.md](ra-qm-team/CLAUDE.md) | ISO 13485, MDR, FDA, GDPR, ISO 27001 compliance |
| `business-growth/` | [business-growth/CLAUDE.md](business-growth/CLAUDE.md) | Customer success, sales engineering, revenue operations |
| `finance/` | [finance/CLAUDE.md](finance/CLAUDE.md) | Financial analysis, DCF valuation, SaaS metrics |
| `research-ops/` | [research-ops/CLAUDE.md](research-ops/CLAUDE.md) | Clinical study design, R&D finance, market research, product research |
| `standards/` | [standards/CLAUDE.md](standards/CLAUDE.md) | Communication, quality, git, security standards |
| `templates/` | [templates/CLAUDE.md](templates/CLAUDE.md) | Template system usage |

---

## ClawHub / Plugin Publishing Rules

This repository publishes to **ClawHub** (clawhub.com). Non-negotiable rules:

1. **`cs-` prefix** only when a slug is already taken on ClawHub. Never rename repo folders to match ClawHub slugs.
2. **No paid/commercial service dependencies.** Free-tier or BYOK patterns only.
3. **Rate limit: 5 new skills per hour** on ClawHub.
4. **`skills` path format:** Must use `"skills": ["./"]` (array with `./` prefix). Bare strings like `"skills": "skills"` are the legacy form — tolerated by the validator but must not be used in new manifests.
5. **Two approved extension fields** (stripped at publish time): `source` (Path-B provenance) and `attribution` (MIT-licensed external work credit). No other extra fields.
6. **Version** in plugin.json must match the current repo release version.

---

## Key Principles

1. **Skills are products** — Each skill is deployable as a standalone package
2. **Algorithm over AI** — Scripts use deterministic logic, never LLM calls
3. **Documentation-driven** — SKILL.md is the executable artifact, not just docs
4. **Template-heavy** — Provide ready-to-use templates that users customize
5. **No inter-skill dependencies** — Each skill must be self-contained
6. **Stdlib-only Python** — Zero pip installs required to run any tool
7. **Quality gates are binding for new skills** — Structure ≥75, zero CRITICAL/HIGH security findings

---

## Notes for AI Assistants

- **Always read domain-specific CLAUDE.md files** before working on skills in that domain (see Navigation Map above).
- **Never modify auto-generated files:** `.codex/`, `.gemini/`, `.hermes/`, `.vibe/` trees, `marketplace.json`, and `*skills-index.json` files are all auto-generated. Changes are overwritten by sync scripts.
- **PRs must target `dev`**, never `main`. The enforce-pr-target workflow auto-closes PRs targeting main.
- **SKILL.md frontmatter** — two fields only (`name` + `description`). Adding extra fields causes PR rejection.
- **SKILL.md line limit is 500.** If content exceeds this, move to `references/` and link from SKILL.md.
- **plugin.json `author` must be an object**, not a string. String format causes Claude Code install errors.
- **The `./` prefix in `skills` paths is required** by Claude Code 2.1.144+. Do not regress to bare strings.
- **Dead links to `documentation/`, `eval-workspace/`, `megaprompts/`, `tests/` are intentional** — those folders are gitignored and exist only on the maintainer's disk.
- **Docs pages are auto-generated.** Do not create or modify files under `docs/skills/` directly — they are regenerated by `scripts/generate-docs.py`.
- **Cross-platform sync indexes** (`.codex/skills-index.json`, `.gemini/skills-index.json`, etc.) are regenerated by maintainers after merges. Never hand-edit them.
- **The official skill count** in `marketplace.json` and README badges is curated. Do not change it in PRs.
- When creating new skills, follow the **11-file Path-B layout**: SKILL.md, plugin.json, 3 Python scripts, 3 reference docs, 1 agent, 1 slash command, `onboard.py` + `config_loader.py` for newer domains.
- **Quality gate is binding for new skills** (post-v2.6.0): structure ≥75, all scripts pass `--help`, zero CRITICAL/HIGH security findings, `description` field in frontmatter must be a real trigger description (not just the skill name).

---

## Version and Status

**Current version:** v2.9.0
**Skills:** 338 across 16 domains
**Plugins:** 63 marketplace plugins
**Status:** Docs site live at GitHub Pages; CI quality gate active on all PRs

For full version history, see [CHANGELOG.md](CHANGELOG.md).

---

**Last Updated:** June 1, 2026
