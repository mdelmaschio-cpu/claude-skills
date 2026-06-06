---
name: cs-workflow
description: "Carica il contesto del workflow personale per il repository claude-skills. Mostra un riepilogo delle regole attive: lingua, git, conferme richieste, stato del repo."
---

# cs-workflow — Carica contesto sessione

Leggi e applica il contenuto di `personal/personal-workflow/skills/personal-workflow/SKILL.md`.

Poi rispondi con un riepilogo compatto in italiano:

```
Contesto caricato per claude-skills
────────────────────────────────────
Lingua:     italiano
Git:        conventional commits | PR → dev | mai push su main
Conferme:   reset/force-push/cancellazioni/modifiche >10 file
Ruolo:      solo maintainer
Versione:   v2.9.0 + unreleased
────────────────────────────────────
Pronto.
```

Se il repository ha cambiamenti non committati (`git status` mostra modifiche), segnalarlo dopo il riepilogo.
