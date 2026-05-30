# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Purpose

This is a **comprehensive skills library** for Claude AI and Claude Code - reusable, production-ready skill packages that bundle domain expertise, best practices, analysis tools, and strategic frameworks. The repository provides modular skills that teams can download and use directly in their workflows.

**Current Scope:** 338 production-ready skills across 16 domains with 533 Python automation tools, 676 reference guides, 51+ agents (cs-* + 7 personas), and 87+ slash commands, distributed as 62 marketplace plugins. **v2.9.0 (complete)** added the **research-ops/** top-level domain — enterprise Research Operations (orchestrator + clinical-research + research-finance + market-research + product-research), the managed counterpart to the academic research/ domain, with `context: fork` orchestration and a Matt Pocock "Forcing-question library" in every SKILL.md plus `/cs:grill-research-ops`. **v2.8.0 (complete)** added 2 new top-level domains — **business-operations/** (7 internal-ops skills: orchestrator + process-mapper + vendor-management + capacity-planner + internal-comms + knowledge-ops + procurement-optimizer) and **commercial/** (8 per-deal-economics skills: orchestrator + pricing-strategist + deal-desk + partnerships-architect + channel-economics + commercial-policy + rfp-responder + commercial-forecaster) — with orchestrator skills using `context: fork` for chaining, Matt Pocock docs-anchored "Forcing-question library" in every SKILL.md, plus `/cs:grill-bizops` and `/cs:grill-commercial`. **v2.8.2** adds a productivity-shaped `handoff` skill (sibling to engineering/handoff) inspired by Matt Pocock — first-run setup with configurable save location, redaction linter, SessionStart + SessionEnd hooks, fidelity self-check, `--refresh` flag. **v2.8.1** upgraded the engineering role-skills (senior-fullstack / senior-frontend / senior-backend) with karpathy-coder + Matt Pocock decision engines + per-role forcing questions. v2.7.3 ports `alirezarezvani/aeo-box` — AEO (Answer Engine Optimization) skill into marketing-skill/ + security-guidance PreToolUse hook into engineering/. v2.7.0 added 13 Path-B skills across 3 top-level domains (productivity, marketing, research). v2.6.0 added 4 Matt Pocock-derived productivity skills.

**Key Distinction**: This is NOT a traditional application. It's a library of skill packages meant to be extracted and deployed by users into their own Claude workflows.

## Maintainer-Local Folders (gitignored)

The following exist on the maintainer's disk but are excluded from the public GitHub tree so cloners only see production skill packages:

- `documentation/` — sprint plans, strategy, implementation roadmaps
- `eval-workspace/` — Tessl evaluation outputs
- `megaprompts/` — pre-skill draft specs (Path-B source material)
- `tests/` — pytest suite (run locally; not in CI)
- `.autoresearch/` — autoresearch agent workspace
- `AUDIT_REPORT.md` — internal audit snapshots

In-repo references to paths under these folders (e.g. `documentation/implementation/...`) resolve locally for the maintainer but appear as dead links on GitHub. This is intentional.

## Navigation Map

This repository uses **modular documentation**. For domain-specific guidance, see:

| Domain | CLAUDE.md Location | Focus |
|--------|-------------------|-------|
| **Agent Development** | [agents/CLAUDE.md](agents/CLAUDE.md) | cs-* agent creation, YAML frontmatter, relative paths |
| **Marketing Skills** | [marketing-skill/CLAUDE.md](marketing-skill/CLAUDE.md) | Content creation, SEO, ASO, demand gen, campaign analytics |
| **Product Team** | [product-team/CLAUDE.md](product-team/CLAUDE.md) | RICE, OKRs, user stories, UX research, SaaS scaffolding |
| **Engineering (Core)** | [engineering-team/CLAUDE.md](engineering-team/CLAUDE.md) | Fullstack, AI/ML, DevOps, security, data, QA tools |
| **Engineering (POWERFUL)** | [engineering/](engineering/) | Agent design, RAG, MCP, CI/CD, database, observability |
| **C-Level Advisory** | [c-level-advisor/CLAUDE.md](c-level-advisor/CLAUDE.md) | CEO/CTO strategic decision-making |
| **Project Management** | [project-management/CLAUDE.md](project-management/CLAUDE.md) | Atlassian MCP, Jira/Confluence integration |
| **RA/QM Compliance** | [ra-qm-team/CLAUDE.md](ra-qm-team/CLAUDE.md) | ISO 13485, MDR, FDA, GDPR, ISO 27001 compliance |
| **Business & Growth** | [business-growth/CLAUDE.md](business-growth/CLAUDE.md) | Customer success, sales engineering, revenue operations |
| **Finance** | [finance/CLAUDE.md](finance/CLAUDE.md) | Financial analysis, DCF valuation, budgeting, forecasting, SaaS metrics |
| **Research Operations** | [research-ops/CLAUDE.md](research-ops/CLAUDE.md) | Clinical study design, R&D finance, market research, product research (enterprise counterpart to academic research/) |
| **Standards Library** | [standards/CLAUDE.md](standards/CLAUDE.md) | Communication, quality, git, security standards |
| **Templates** | [templates/CLAUDE.md](templates/CLAUDE.md) | Template system usage |

## Architecture Overview

### Repository Structure

```
claude-code-skills/
├── .claude-plugin/            # Plugin registry (marketplace.json)
├── agents/                    # 32 standalone agents (cs-* + 7 personas); 51+ cs-* agents repo-wide
├── commands/                  # slash commands (changelog, tdd, saas-health, prd, code-to-prd, plugin-audit, sprint-plan, slo-design, etc.); 87+ repo-wide
├── engineering-team/          # 51 core engineering skills + Playwright Pro + Self-Improving Agent + Security Suite
├── engineering/               # 78 POWERFUL-tier advanced skills (incl. AgentHub, autoresearch-agent, self-eval, llm-wiki, tc-tracker, ship-gate, slo-architect, write-a-skill, caveman, grill-me, handoff)
├── product-team/              # 17 product skills (incl. apple-hig-expert) + Python tools
├── marketing-skill/           # 46 marketing skills (8 pods) + Python tools
├── c-level-advisor/           # 66 C-level advisory skills (full C-suite + founder-mode agents + orchestration)
├── project-management/        # 9 PM skills + bundled Atlassian Remote MCP (.mcp.json)
├── ra-qm-team/                # 18 RA/QM compliance skills
├── compliance-os/             # 9 compliance-OS skills
├── business-growth/           # 5 business & growth skills + Python tools
├── business-operations/       # 7 internal-ops skills (orchestrator + 6 sub-skills)
├── commercial/                # 8 per-deal-economics skills (orchestrator + 7 sub-skills)
├── finance/                   # 4 finance skills + Python tools
├── research/                  # 8 academic research skills (orchestrator + 7 specialists)
├── research-ops/              # 5 research-ops skills (orchestrator + clinical-research + research-finance + market-research + product-research)
├── eval-workspace/            # Skill evaluation results (Tessl)
├── standards/                 # 5 standards library files
├── templates/                 # Reusable templates
├── docs/                      # MkDocs Material documentation site
├── scripts/                   # Build scripts (docs generation)
└── documentation/             # Implementation plans, sprints, delivery
```

### Skill Package Pattern

Each skill follows this structure:
```
skill-name/
├── SKILL.md              # Master documentation (≤500 lines, ≤10KB)
├── scripts/              # Python CLI tools (stdlib-only, no LLM calls)
├── references/           # Expert knowledge bases (loaded on demand)
└── assets/               # User templates
```

**Design Philosophy**: Skills are self-contained packages. Each includes executable tools (Python scripts), knowledge bases (markdown references), and user-facing templates. Teams can extract a skill folder and use it immediately.

**Key Pattern**: Knowledge flows from `references/` → into `SKILL.md` workflows → executed via `scripts/` → applied using `assets/` templates.

## Skill Authoring Standard (Summary)

See [SKILL-AUTHORING-STANDARD.md](SKILL-AUTHORING-STANDARD.md) for the complete standard. Key rules:

### SKILL.md Frontmatter

**Only two fields are allowed:**
```yaml
---
name: "skill-name"
description: "One-line description of when to use this skill. Be specific about trigger conditions."
---
```

Do NOT include `license`, `metadata`, `triggers`, `version`, `author`, `category`, `updated`, or any other fields. PRs with extra frontmatter fields will be rejected.

### The 10 Skill Patterns

| Pattern | Description |
|---------|-------------|
| **1. Context-First** | Check for domain context file (e.g., `marketing-context.md`) before asking questions |
| **2. Practitioner Voice** | Open with expert persona and clear goal. Opinionated, not textbook |
| **3. Multi-Mode Workflows** | At least 2 entry points: Build from Scratch + Optimize Existing |
| **4. Related Skills Navigation** | End with WHEN/NOT disambiguation for 3-7 related skills |
| **5. Reference Separation** | SKILL.md ≤10KB; heavy content in `references/` loaded on demand |
| **6. Proactive Triggers** | Surface 4-6 issues without being asked when context reveals them |
| **7. Output Artifacts** | Map 4-6 common requests to specific deliverable formats |
| **8. Quality Loop** | Tag all findings: 🟢 verified / 🟡 medium / 🔴 assumed |
| **9. Communication Standard** | Bottom line first. What + Why + How. Actions have owners and deadlines |
| **10. Python Tools** | stdlib-only, CLI-first, JSON output, 0-100 scoring scale, sample data embedded |

### Quality Checklist

Before a skill is considered done:
- [ ] YAML frontmatter with `name` + `description` only
- [ ] Practitioner voice — "You are an expert in X. Your goal is Y."
- [ ] Context-first — checks domain context file before asking questions
- [ ] Multi-mode — at least 2 workflows (build/optimize)
- [ ] SKILL.md ≤10KB, ≤500 lines
- [ ] Related Skills section with WHEN/NOT disambiguation
- [ ] Cross-references are bidirectional
- [ ] Listed in domain CLAUDE.md
- [ ] Listed in `.codex/skills-index.json`
- [ ] Listed in `.claude-plugin/marketplace.json`
- [ ] Proactive Triggers (4-6)
- [ ] Output Artifacts table (4-6)
- [ ] Python tool(s) — stdlib-only, CLI-first, JSON output, sample data embedded

## Git Workflow

**Branch Strategy:** feature → dev → main (PR only)

**Branch Protection Active:** Main branch requires PR approval. Direct pushes blocked.

### Quick Start

```bash
# 1. Always start from dev
git checkout dev
git pull origin dev

# 2. Create feature branch
git checkout -b feature/agents-{name}

# 3. Work and commit (conventional commits)
feat(agents): implement cs-{agent-name}
fix(tool): correct calculation logic
docs(workflow): update branch strategy

# 4. Push and create PR to dev
git push origin feature/agents-{name}
gh pr create --base dev --head feature/agents-{name}

# 5. After approval, PR merges to dev
# 6. Periodically, dev merges to main via PR
```

**Branch Naming:**
```
feature/<skill-name>     → New skill
fix/<description>        → Bug fix
improve/<skill-name>     → Enhancement
docs/<description>       → Documentation
```

**Commit Messages:** [Conventional Commits](https://www.conventionalcommits.org/) format:
```
feat(engineering): add browser-automation skill
fix(self-improving-agent): use absolute path for hooks
improve(tdd-guide): add per-language examples
docs: update CONTRIBUTING.md
```

See [standards/git/git-workflow-standards.md](standards/git/git-workflow-standards.md) for commit standards.

## Development Environment

**No build system or test frameworks** - intentional design choice for portability.

**Python Scripts:**
- Use standard library only (minimal dependencies)
- CLI-first design for easy automation
- Support both JSON and human-readable output (`--json` flag)
- No ML/LLM calls (keeps skills portable and fast)
- Exit codes: `0` = success, `1` = warnings, `2` = critical errors

## What NOT to Contribute

The following will be **immediately closed**:

| Type | Why |
|------|-----|
| Links to external repos/tools in README | We don't link 3rd party projects |
| Skills that require paid API keys | Must work without external dependencies |
| Skills that call LLMs in scripts | Scripts must be deterministic |
| PRs targeting `main` instead of `dev` | All PRs must target `dev` |
| PRs with extra frontmatter fields | `name` + `description` only |
| PRs that modify marketplace.json counts | We handle count updates |
| PRs that modify codex/gemini index files | These are auto-generated |

## Cross-Platform Sync

Platform copies are handled by automated scripts. **Do not create or modify these manually:**

| Platform | Directory | Script |
|----------|-----------|--------|
| Codex CLI | `.codex/skills/` | `python3 scripts/sync-codex-skills.py` |
| Gemini CLI | `.gemini/skills/` | `python3 scripts/sync-gemini-skills.py` |
| Hermes Agent | `.hermes/skills/` | `python3 scripts/sync-hermes-skills.py` |
| Mistral Vibe | `.vibe/skills/` | `./scripts/vibe-install.sh` |
| Cursor/Aider/etc. | `integrations/` (gitignored) | `scripts/convert.sh --tool all` |

After your skill is merged, maintainers run these scripts to sync all platforms. Do not edit the `.codex/`, `.gemini/`, `.hermes/`, or `.vibe/` directories directly.

## Quality Validation

Before submitting, verify your skill passes:

```bash
# Structure validation
python3 engineering/skill-tester/scripts/skill_validator.py <your-skill-path> --json

# Quality scoring
python3 engineering/skill-tester/scripts/quality_scorer.py <your-skill-path> --json

# Script testing (if you have scripts)
python3 engineering/skill-tester/scripts/script_tester.py <your-skill-path> --json

# Security audit
python3 engineering/skill-security-auditor/scripts/skill_security_auditor.py <your-skill-path> --strict
```

**Minimum requirements:**
- Structure score ≥ 75/100
- All scripts pass `--help`
- Zero CRITICAL or HIGH security findings
- SKILL.md under 500 lines

## Domain Context Files

Skills check for domain context files before asking questions:

| Domain | Context File | Created By |
|--------|-------------|------------|
| C-Suite | `company-context.md` | `/cs:setup` (cs-onboard skill) |
| Marketing | `marketing-context.md` | marketing-context skill |
| Engineering | `project-context.md` | codebase-onboarding skill |
| Product | `product-context.md` | product-strategist skill |
| RA/QM | `regulatory-context.md` | regulatory-affairs-head skill |

If context exists → read it first, only ask for gaps. If context doesn't exist → offer to create it.

## Current Version

**Version:** v2.9.0 (released — research-ops/ domain: enterprise Research Operations)

See CHANGELOG.md for the full version history.

## How AI Assistants Should Behave Here

### When Creating or Editing Skills

- **Read CONVENTIONS.md and SKILL-AUTHORING-STANDARD.md first** — these are the source of truth for all skill structure decisions
- **Target `dev` branch for all PRs** — never target `main` directly
- **Frontmatter is strictly `name` + `description` only** — reject any suggestion to add other fields
- **SKILL.md must be ≤500 lines and ≤10KB** — move heavy content to `references/`
- **Python scripts must use stdlib only** — no `pip install` requirements, no LLM API calls
- **All scripts must support `--json` and `--help`** — this is a hard requirement
- **Naming**: skill folder = kebab-case, Python scripts = snake_case.py, templates = kebab-case-template.md
- **Cross-references must be bidirectional** — if A mentions B, B must mention A
- **Sub-skills do NOT get standalone docs or index entries** — they are documented within the parent skill only

### When Running Validation

```bash
# Always run before suggesting a skill is complete
python3 engineering/skill-tester/scripts/skill_validator.py <skill-path> --json
python3 engineering/skill-security-auditor/scripts/skill_security_auditor.py <skill-path> --strict
```

### When Navigating the Repo

- Domain-specific questions → check the domain CLAUDE.md first (listed in Navigation Map above)
- Agent creation → see [agents/CLAUDE.md](agents/CLAUDE.md) for cs-* agent patterns
- Slash commands → see [commands/](commands/) directory
- Persona creation → see [agents/personas/TEMPLATE.md](agents/personas/TEMPLATE.md)
- Orchestration patterns → see [orchestration/ORCHESTRATION.md](orchestration/ORCHESTRATION.md)

### What NOT to Do

- Do NOT modify `.codex/`, `.gemini/`, `.hermes/`, `.vibe/` directories — these are auto-generated
- Do NOT add external tool links to README
- Do NOT create skills that call LLMs in Python scripts — scripts must be deterministic
- Do NOT add API key requirements to skills
- Do NOT target `main` branch in PRs
- Do NOT change the official skill count (338) in documentation — this is curated by maintainers
