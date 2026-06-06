# Convenzioni Workflow — claude-skills

Riferimento rapido per Claude durante il lavoro sul repository.

## Regola d'oro

> Quando aggiungi una skill, segui sempre il pattern Path-B (11 file). Quando modifichi una skill esistente, tocca solo i file strettamente necessari. Non rifattorizzare ciò che non è stato richiesto.

## Dominio → cartella

| Dominio | Cartella top-level |
|---------|-------------------|
| Engineering core | `engineering-team/` |
| Engineering POWERFUL | `engineering/` |
| Product | `product-team/` |
| Marketing skill | `marketing-skill/` |
| Marketing landing | `marketing/` |
| C-Level advisory | `c-level-advisor/` |
| Project management | `project-management/` |
| RA/QM compliance | `ra-qm-team/` |
| Compliance OS | `compliance-os/` |
| Business growth | `business-growth/` |
| Business operations | `business-operations/` |
| Commercial | `commercial/` |
| Finance | `finance/` |
| Research (academic) | `research/` |
| Research ops | `research-ops/` |
| Productivity | `productivity/` |
| Personale | `personal/` |

## Quality gates per nuove skill

Prima del commit su una nuova skill:
1. `python scripts/check_plugin_json.py --path <plugin-dir>` → deve passare
2. Tutti gli script devono rispondere a `python script.py --help` (exit 0)
3. SKILL.md deve avere frontmatter YAML con almeno `name` e `description`
4. `skills` in plugin.json usa il prefisso `./`

## Segnali che richiedono conferma

- Il task modifica `marketplace.json` o `CLAUDE.md`
- Il task tocca più di 10 file
- Il task include `git reset`, `force push`, o cancellazione di branch
- Il task propone una riorganizzazione di cartelle esistenti

## Convenzioni di versioning

- Release: `vX.Y.Z` (SemVer)
- Patch per fix/aggiunte minori: incrementa Z
- Minor per nuovi domini o skill significative: incrementa Y
- Major per ristrutturazioni architetturali: incrementa X
- Tutti i plugin.json devono allinearsi alla versione del repo al momento della release
