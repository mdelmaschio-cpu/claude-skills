# Personal Workflow Skill

Skill di configurazione personale per il maintainer del repository `claude-skills`.

Carica questo plugin in Claude Code per applicare automaticamente le preferenze operative senza doverle ridefinire a ogni sessione:

- Risposte sempre in **italiano**
- **Conventional commits** obbligatori
- **PR verso `dev`** dopo ogni push (mai push diretto su `main`)
- **Conferma esplicita** prima di azioni rischiose (reset, force push, cancellazioni)
- Contesto completo del repository (versione, struttura, convenzioni)

## Installazione

```bash
# Dal repository claude-skills
claude install personal/personal-workflow
```

## Uso

Digita `/cs:workflow` per caricare il contesto della sessione e verificare lo stato del repository.

## Contenuto

| File | Scopo |
|------|-------|
| `skills/personal-workflow/SKILL.md` | Regole operative complete |
| `skills/personal-workflow/references/workflow-conventions.md` | Riferimento rapido per convenzioni |
| `commands/cs-workflow.md` | Slash command per caricare il contesto |
