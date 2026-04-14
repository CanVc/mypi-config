# Revue du workflow TDD agentic — mypi-config

**Date:** 2026-04-14  
**Source:** Review croisee Claude (Sonnet 4.6) + Codex (gpt-5.3-codex, reasoning=high)

---

## Plan de structure retenu (V1)

### Fichiers par story

```
stories/1-2/
  1-2-story.md        # BMAD pur — intouchable, aucun ajout TDD
  1-2-test-plan.md    # Strategie + liste batches + statuts (absorbe l'orchestrator-log)
  1-2-batch-01.md
  1-2-batch-02.md
  ...
```

**3 types de fichiers. Orchestrator-log supprime. Changelog supprime (git log suffit).**

### Layout batch-XX.md

```markdown
# Batch XX — <Short Name>
## Metadata              (id, statut, story ref, AC cibles)
## Preconditions
## Test Spec
## Red Gate
## Dev
## Green Gate
## Batch Outcome
## Next-Step Handoff
```

### Layout test-plan.md

```markdown
# Test Plan — Story X-Y
## Test Strategy         (profil : tdd-lite / tdad-lite, approche globale)
## Batch List            (tableau : id | nom | statut | priorite)
## Completion Criteria
```

---

## Decisions confirmees

| Point | Decision |
|---|---|
| story.md | BMAD pur, aucun ajout TDD |
| orchestrator-log.md | Supprime — routing dans test-plan.md, decisions dans batch |
| Changelog | Supprime en V1 — git log suffit |
| **Commits** | **1 commit par agent** (test-writer, red-validator, dev, green-validator, orchestrator sync) |

> Rationale commits : observabilite maximale. 15 secondes de plus par phase, git log lisible par role.

---

## Risques restants a traiter avant implementation

1. **Criteres de profil story non formalises** — sans 3-5 criteres binaires par profil (tdd-lite / tdad-lite / atdd-lite), le choix reste subjectif
2. **Politique "blocked" indefinie** — retry cap, escalation humaine, option skip a specifier
3. **Heuristique de pyramide de tests par batch** — le test-architect n'a pas de guide sur quel type de test va dans quel batch
4. **CLAUDE.md + hooks PostToolUse** — prerequis infrastructure pour le feedback de tests automatique

---

## Points forts confirms (convergence Claude + Codex)

- Separation des roles empeche la conception de tests faciles autour d'une implementation pre-imaginee
- "Context beats procedure" : fournir la liste de tests cibles reduit les regressions de 70% (TDAD arXiv 2603.17973)
- Batch-first limite les patches "big bang" des agents
- Traceability header dans batch-XX.md compense la suppression de l'orchestrator-log sans bruit

## Verdict

Design conceptuellement solide. La reduction a 3 types de fichiers elimine la fragmentation principale.
Le prochain blocage sera l'implementation des skills + hooks, pas la conception.
