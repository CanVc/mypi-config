# Le TDD agentique : guide complet pour piloter les agents de codage par les tests

**Le TDD (Test-Driven Development) s'impose comme le pattern le plus efficace pour travailler avec des agents de codage IA**, selon un consensus quasi-unanime des praticiens et chercheurs en 2025-2026. La raison est simple : les agents IA produisent du code non-déterministe, parfois halluciné, et les tests constituent le seul garde-fou objectif et automatisable. Cependant, appliquer naïvement les principes TDD classiques aux agents crée un paradoxe : l'étude TDAD (arXiv, mars 2026) démontre qu'ajouter des instructions TDD procédurales *sans contexte ciblé* **augmente les régressions de 6% à 10%**, pire que l'absence totale de TDD. La clé n'est pas de dire à l'agent *comment* faire du TDD, mais de lui fournir *quels tests vérifier*. Ce rapport synthétise les workflows concrets, patterns de tests, outils et retours d'expérience pour implémenter un TDD agentique efficace.

---

## 1. Structurer la boucle red-green-refactor avec un agent de codage

### Le problème fondamental : les LLM codent à l'envers

Tous les agents de codage — Claude Code, Cursor, Aider, Copilot — partagent un biais identique : **ils écrivent l'implémentation d'abord, puis les tests**. C'est l'exact inverse du TDD. Comme le documente Alexander Opalic : « Quand je demande à Claude d'implémenter une feature X, il écrit l'implémentation d'abord. À chaque fois. » Ce comportement est si ancré que le forcer à faire autrement nécessite une infrastructure dédiée, pas simplement un prompt.

Simon Willison, dans son guide « Agentic Engineering Patterns » (février 2026), identifie pourtant le TDD comme « un raccourci remarquablement efficace pour obtenir de meilleurs résultats d'un agent de codage ». Un simple prompt comme `Build a Python function to extract headers from a markdown string. Use red/green TDD.` suffit pour que tout bon modèle comprenne la consigne — mais l'appliquer de façon disciplinée sur un projet réel exige bien plus.

### Architecture multi-agents avec isolation de contexte

L'approche la plus sophistiquée documentée en 2025-2026 est le **système à trois sous-agents avec isolation de contexte**, décrit par alexop.dev (novembre 2025). Le principe : exécuter toutes les phases TDD dans une seule fenêtre de contexte brise fondamentalement le TDD, car « le LLM conçoit inconsciemment les tests autour de l'implémentation qu'il planifie déjà — il triche sans le vouloir ».

La solution déploie trois agents dédiés via les fichiers `.claude/agents/` :

```markdown
# .claude/agents/tdd-test-writer.md (Phase RED)
Tools: Read, Glob, Grep, Write, Edit, Bash
Principes: Le test décrit le comportement utilisateur, jamais les détails d'implémentation.
Sortie: chemin du fichier test + output d'échec vérifié

# .claude/agents/tdd-implementer.md (Phase GREEN)  
Lecture: uniquement le test échouant
Principes: Minimal — écrire uniquement ce que le test exige. Pas d'extras. Corriger l'implémentation, pas les tests.

# .claude/agents/tdd-refactorer.md (Phase REFACTOR)
Checklist: extraire les composables, simplifier les conditionnels, améliorer le nommage, supprimer la duplication.
Peut retourner « Aucun refactoring nécessaire » avec justification.
```

Un fichier **skill d'orchestration** (`.claude/skills/tdd-integration/skill.md`) déclenche automatiquement le cycle sur des phrases comme « implement », « add feature » ou « build », avec des portes explicites : « Ne PAS passer à la phase Green tant que l'échec du test n'est pas confirmé. » Le coût d'installation est d'environ **2 heures de configuration**, après quoi chaque demande de feature suit automatiquement le cycle.

### Le workflow Anthropic officiel et les hooks

Le workflow TDD recommandé par Anthropic pour Claude Code suit quatre étapes :

```bash
# 1. RED — Écrire les tests
> "Write tests for the auth module using pytest. TDD approach, no mock implementations."

# 2. Confirmer l'échec
> "Run the tests. They should all fail."

# 3. Committer les tests échouants (checkpoint de sécurité)
> git add -A && git commit -m "RED: failing auth tests"

# 4. GREEN — Implémenter
> "Write the implementation. Do not modify the tests. Keep going until all tests pass."
```

Le **commit des tests échouants avant l'implémentation** est crucial : Claude modifie parfois les tests pour les faire passer plutôt que de corriger son code. Le commit crée un filet de sécurité permettant de détecter et revert ces modifications.

Pour automatiser le feedback, un **hook PostToolUse** lance les tests après chaque édition de fichier :

```json
// .claude/settings.json
{
  "hooks": {
    "PostToolUse": [{
      "matcher": "Edit|Write",
      "command": "npm test --watchAll=false 2>&1 | head -20"
    }]
  }
}
```

### Prompts concrets et configuration CLAUDE.md

La configuration la plus robuste intègre les règles TDD directement dans le fichier `CLAUDE.md` du projet :

```markdown
## Testing and TDD
When working on a new feature or bug fix, ALWAYS follow this strict sequence:
1. Write a FAILING test first. Do NOT write implementation yet.
2. Run the test and confirm it fails for the expected reason.
3. Wait for human review before proceeding.
4. Write the MINIMUM code to make the test pass. No extras.
5. Run tests to confirm they pass.
6. Refactor if needed, keeping all tests green.

### Constraints
- Never modify existing tests to make them pass
- One test at a time, one assertion per test
- Use descriptive test names that describe business requirements
- Run tests with --silent flags to conserve context window
```

Pour les projets utilisant Cursor, un prompt système similaire peut être configuré dans les règles du projet. Avec Aider, la commande `/run pytest` intégrée au chat analyse automatiquement les erreurs et propose des corrections itératives. Le flag `--test` d'Aider lance automatiquement lint et tests après chaque changement.

### Uncle Bob et l'ATDD avec Claude Code

Robert C. Martin (« Uncle Bob ») a créé un plugin ATDD (Acceptance Test-Driven Development) pour Claude Code qui implémente **deux flux de tests parallèles** — tests d'acceptation en Given/When/Then et tests unitaires classiques. Sa conclusion : « Les deux flux de tests différents obligent Claude à réfléchir beaucoup plus profondément à la structure du code. » Le plugin inclut même une phase de **mutation testing** pour valider la robustesse des tests.

---

## 2. Écrire des tests adaptés aux agents IA et aux outputs non-déterministes

### Pourquoi les tests classiques échouent avec l'IA

L'assertion `assertEqual(expected, actual)` repose sur un contrat fondamental : entrée identique → sortie identique. Les agents IA brisent ce contrat. Même avec `temperature=0`, les LLM produisent jusqu'à **15% de variation** entre exécutions. Dans un agent multi-étapes, cette non-déterminisme se compose : chaque appel d'outil, chaque étape de raisonnement introduit de la variation supplémentaire.

### La nouvelle pyramide de tests pour l'IA

Block (anciennement Square), dans un article d'Angie Jones (janvier 2026), propose une pyramide de tests organisée par **tolérance à l'incertitude** plutôt que par type de test :

| Niveau | Méthode | Vitesse | Coût |
|--------|---------|---------|------|
| **Fondations déterministes** | Tests unitaires avec providers mockés | Très rapide | Gratuit |
| **Réalité reproductible** | Record/replay des interactions LLM + MCP | Rapide | Faible |
| **Performance probabiliste** | Benchmarks, taux de succès agrégés | Moyen | Moyen |
| **Jugement qualitatif** | LLM-as-judge, rubrics, vote majoritaire (3 runs) | Lent | Élevé |

L'insight clé : « Au lieu de correspondances exactes, on cherche des tendances. Au lieu de pass/fail, on mesure des taux de succès. »

### Pattern 1 : Mocker le LLM, tester tout le reste

Le pattern le plus immédiat consiste à créer un **StubProvider** qui retourne des réponses prédéfinies, permettant de tester toute la logique autour du LLM de façon déterministe :

```python
class StubProvider(LLMProvider):
    def __init__(self, research_response="stub research",
                 synthesize_response="stub synthesis"):
        self._research_response = research_response
        self._synthesize_response = synthesize_response
    
    def research(self, instruction, search=True):
        return self._research_response
    
    def synthesize(self, context, instruction):
        return self._synthesize_response

# Test déterministe de la logique de routage
def test_routes_to_correct_agent():
    provider = StubProvider()
    router = AgentRouter(provider)
    result = router.route("refund request")
    assert result.agent_type == "customer_support"
```

Ce qu'on teste ainsi de façon déterministe : le routage des étapes, la validation des arguments, la logique de retry, le parsing des outputs (schéma JSON), les guardrails, la validation des schémas d'outils, les limites de tours.

### Pattern 2 : Évaluations scorées avec seuils

La transition fondamentale est de remplacer `assertEqual` par des **métriques scorées avec seuils**. DeepEval, intégré nativement à pytest, offre plus de 14 métriques :

```python
from deepeval import assert_test
from deepeval.metrics import HallucinationMetric, FaithfulnessMetric
from deepeval.test_case import LLMTestCase

def test_agent_no_hallucination():
    metric = HallucinationMetric(threshold=0.5)
    test_case = LLMTestCase(
        input="Quelle est notre politique de remboursement ?",
        actual_output=get_agent_response("Quelle est notre politique de remboursement ?"),
        context=["Remboursement intégral sous 30 jours, sans frais supplémentaires."]
    )
    assert_test(test_case, [metric])

def test_custom_scoring_with_geval():
    from deepeval.metrics import GEval
    from deepeval.test_case import LLMTestCaseParams
    
    correctness = GEval(
        name="Correctness",
        evaluation_steps=[
            "Vérifier les contradictions factuelles",
            "Pénaliser les informations critiques manquantes",
            "Accepter les paraphrases et différences de style"
        ],
        evaluation_params=[LLMTestCaseParams.ACTUAL_OUTPUT, 
                          LLMTestCaseParams.EXPECTED_OUTPUT],
        threshold=0.7
    )
```

### Pattern 3 : Tests stochastiques — exécuter N fois et agréger

Pour absorber la variance non-déterministe, la bonne pratique est d'exécuter chaque test **3 fois minimum** et d'agréger les scores. Le framework AgentEval (.NET) formalise cela :

```csharp
var result = await stochasticRunner.RunStochasticTestAsync(
    agent, testCase,
    new StochasticOptions {
        Runs = 20,                    // Exécuter 20 fois
        SuccessRateThreshold = 0.85,  // 85% doivent passer
        ScoreThreshold = 75           // Score min pour compter comme "pass"
    });
result.Statistics.Mean.Should().BeGreaterThan(80);
result.Statistics.StandardDeviation.Should().BeLessThan(10);
```

Monte Carlo Data recommande environ **1 exécution sur 10** produit des résultats parasites où l'output est correct mais le juge LLM hallucine. Un mécanisme de retry est essentiel.

### Pattern 4 : Record/Replay pour la reproductibilité

Block a développé un système de **record/replay** qui capture les interactions réelles avec le modèle et les rejoue de façon déterministe en CI :

```rust
// Enregistrement : wrapper autour d'un vrai provider
let provider = TestProvider::new_recording(real_provider, "fixtures/session.json");
let (response, usage) = provider.complete(system, messages, tools).await?;
provider.finish_recording()?;

// Replay : aucun vrai provider nécessaire
let provider = TestProvider::new_replaying("fixtures/session.json")?;
let (response, usage) = provider.complete(system, messages, tools).await?;
```

### Frameworks d'évaluation : comparatif 2026

Les principaux outils pour évaluer les agents IA :

| Framework | Approche | Points forts |
|-----------|----------|-------------|
| **DeepEval** | Python/pytest natif, 14+ métriques | G-Eval custom, CI/CD direct, 10M+ évals/mois |
| **Promptfoo** | CLI, YAML, matrix testing | Trajectoires d'agents, red teaming OWASP |
| **Langfuse** | Observabilité + évaluation open-source | Experiment Runner, datasets distants |
| **LangSmith** | Natif LangChain/LangGraph | Scoring par étape, trajectoires multi-modes |
| **Braintrust** | CI/CD pour l'IA | Régression automatique sur commits |

L'approche recommandée par Anthropic (janvier 2026) combine trois types de « graders » : **code-based** (rapide, objectif : regex, validation JSON, tests binaires), **model-based** (flexible : rubrics, assertions en langage naturel, consensus multi-juges), et **human** (gold standard pour la calibration). La stratégie optimale : commencer par les vérifications les moins chères, escalader vers le LLM-as-judge, calibrer avec le jugement humain.

---

## 3. Tests Playwright E2E comme spécifications pour les agents de codage

### L'écosystème Playwright devient nativement agentique

Playwright v1.56+ (octobre 2025) a introduit trois agents spécialisés — **Planner**, **Generator** et **Healer** — qui forment un pipeline complet de cycle de vie des tests. Ces agents fonctionnent via le Model Context Protocol (MCP) et s'intègrent avec Claude Code, VS Code Copilot et OpenCode.

```bash
npx playwright init-agents --loop=claude  # Configuration pour Claude Code
```

L'architecture repose sur un dossier `specs/` contenant des plans de tests en Markdown lisibles par les humains, un fichier seed (`seed.spec.ts`) pour le bootstrap de l'environnement, et un dossier `tests/` pour les tests générés. Le **Planner** explore l'application via un vrai navigateur et produit les specs structurées. Le **Generator** transforme ces specs en tests Playwright exécutables en vérifiant les sélecteurs et assertions en direct. Le **Healer** rejoue les étapes échouantes, inspecte l'UI courante, applique des correctifs et relance jusqu'au succès.

### Le pattern specs-as-Markdown : pont entre intention humaine et tests exécutables

Le pattern dominant pour le TDD E2E agentique utilise des **fichiers Markdown comme représentation intermédiaire** entre l'intention du développeur et le code de test. Voici un exemple concret :

```markdown
# specs/basic-operations.md
### 1.1 Ajouter un Todo valide
**Étapes:**
1. Cliquer dans le champ "What needs to be done?"
2. Taper "Buy groceries"
3. Appuyer sur Entrée

**Résultats attendus:**
- Le todo apparaît dans la liste avec une checkbox décochée
- Le compteur affiche "1 item left"
- Le champ de saisie est vidé
```

Le Generator produit alors automatiquement :

```typescript
import { test, expect } from '../fixtures';

test.describe('Adding New Todos', () => {
  test('Add Valid Todo', async ({ page }) => {
    const todoInput = page.getByRole('textbox', { name: 'What needs to be done?' });
    await todoInput.click();
    await todoInput.fill('Buy groceries');
    await todoInput.press('Enter');
    await expect(page.getByText('Buy groceries')).toBeVisible();
    await expect(page.getByText('1 item left')).toBeVisible();
    await expect(todoInput).toHaveValue('');
  });
});
```

### Intégrer Playwright dans un workflow TDD agentique

Shipyard (novembre 2025) documente le workflow TDD E2E le plus complet avec la configuration CLAUDE.md suivante :

```markdown
## Testing requirements
### Test-driven development (TDD) workflow
When implementing new features or fixing bugs, follow TDD:
1. Write failing Playwright tests first that define the expected behavior
2. Run tests to confirm they fail (red phase)
3. Write minimal code to make tests pass (green phase)
4. Use Playwright MCP to cross-reference tests with the actual webpage
5. Refactor while keeping tests green
6. Never skip directly to implementation
```

La configuration MCP pour donner à Claude Code un accès direct au navigateur :

```json
// .mcp.json
{
  "mcpServers": {
    "playwright": {
      "type": "stdio",
      "command": "npx",
      "args": ["@playwright/mcp@latest"]
    }
  }
}
```

Le pattern « Self-QA » permet à l'agent de **vérifier ses propres changements** en naviguant dans l'application après chaque modification. Le blog NikiforovAll décrit des slash commands personnalisés (`.claude/commands/pw-generate-tests.md`) où Claude explore l'application via Playwright MCP, produit un rapport de test manuel, puis génère des tests Playwright exécutables servant de spécifications.

### Tests E2E stables avec du code généré par IA

La stabilité des tests E2E générés par IA repose sur plusieurs principes identifiés par TestDino et BrowserStack (2026). L'**Accessibility Object Model (AOM)** est le « secret » : les rôles ARIA et labels conçus pour les technologies d'assistance sont parfaits pour les agents IA. `getByRole('button', { name: 'Checkout' })` est **10 fois plus stable** que `div.checkout-btn-v3`. Les principales causes de flakiness dans les tests générés par IA sont l'oubli d'`await` sur les actions async, l'utilisation de `waitForTimeout()` au lieu d'assertions web-first, les données de test non-déterministes et l'interdépendance entre tests.

Un conseil pragmatique de Decipher : « Prévoyez de l'itération. Le workflow n'est presque jamais "un prompt, on commit". Planifiez 30-60 minutes par flux bien testé, pas les 5 minutes que suggèrent les vidéos de démo. »

Notons enfin l'approche radicalement différente de Meta (février 2026) avec les **JiTTests (Just-in-Time Tests)** : des tests générés à la volée par des LLM pour chaque changement de code, qui ne résident pas dans le codebase. Cette approche élimine le coût de maintenance des tests mais nécessite une infrastructure spécifique.

---

## 4. Le framework TDAD : deux papiers, un même principe fondamental

### Papier 1 — Réduction des régressions par analyse d'impact (arXiv 2603.17973)

Le premier papier TDAD (Alonso, Yovine, Braberman — mars 2026, soumis à ACM AIWare 2026) s'attaque au problème des **régressions introduites par les agents de codage**. METR avait montré qu'environ la moitié des patchs passant SWE-bench ne seraient pas mergés par de vrais mainteneurs, principalement à cause de régressions.

**Le pipeline TDAD fonctionne en deux étapes.** L'**indexation** parse un repository Python via le module `ast` et construit un graphe de dépendances code-tests avec 4 types de nœuds (File, Function, Class, Test) et 5 types d'arêtes (CONTAINS, CALLS, IMPORTS, TESTS, INHERITS). L'**analyse d'impact** exécute quatre stratégies en parallèle — Direct (poids 0.95), Transitive (0.70, 1-3 hops dans le graphe d'appels), Coverage (0.80, dépendance au niveau fichier), et Imports (0.50) — pour scorer chaque test par pertinence.

L'intégration avec l'agent est remarquablement simple. TDAD produit deux artefacts statiques :

- `test_map.txt` : mapping source → tests (une ligne par mapping, grep-able)
- `SKILL.md` : **20 lignes** d'instructions — (1) corriger le bug, (2) grep test_map.txt pour les tests liés, (3) les exécuter et corriger les échecs

À l'exécution, l'agent n'a besoin que de **grep et pytest** — pas de base graphe, pas de serveur MCP, pas d'appel API.

Les résultats sur SWE-bench Verified (Phase 1, 100 instances, Qwen3-Coder 30B) sont éloquents :

| Configuration | Taux de régression tests | Échecs P2P absolus |
|--------------|------------------------|-------------------|
| Vanilla (baseline) | 6.08% | 562 |
| TDD procédural seul | **9.94%** (pire !) | 799 |
| TDAD (GraphRAG + skill) | **1.82%** | 155 |

La **réduction de 70% des régressions** (6.08% → 1.82%) est le résultat phare. Mais le résultat le plus contre-intuitif est que le TDD procédural seul **augmente** les régressions à 9.94%.

### Le paradoxe du TDD procédural

Ce paradoxe constitue la contribution conceptuelle majeure du papier. Deux facteurs l'expliquent. Premièrement, les **instructions verbales consomment des tokens** de contexte avec des instructions procédurales, repoussant le contexte du repository dont le modèle 30B a besoin. Deuxièmement, les agents « TDD-prompted » tentent des corrections plus ambitieuses, touchant plus de fichiers, mais **sans connaissance graphique** de quels tests vérifier, causant des dommages collatéraux.

L'ablation confirme : raccourcir le prompt *sans* contexte graphique diminue la résolution (30% → 20%). L'amélioration requiert le **contexte dérivé du graphe** : un prompt court *plus* le test_map. La découverte la plus transférable : **pour les modèles plus petits, fournir le bon contexte (quels tests vérifier) bat fournir la bonne procédure (comment faire du TDD)**.

Un résultat supplémentaire remarquable : la **boucle d'auto-amélioration** (inspirée du framework autoresearch de Karpathy) a autonomement simplifié le SKILL.md de 107 lignes de 9 phases TDD à 20 lignes de « fix, grep, verify », faisant passer la résolution de **12% à 60% avec 0% de régression**.

L'outil est disponible en open source : `pip install tdad`.

### Papier 2 — Compiler des agents depuis des spécifications comportementales (arXiv 2603.08806)

Un second papier indépendant de Tzafrir Rehan (Fiverr Labs, mars 2026) utilise le même acronyme TDAD mais cible un problème différent : traiter les **prompts d'agents comme des artefacts compilés**. Le pipeline utilise trois agents spécialisés : **TestSmith** génère des tests visibles et cachés depuis des spécifications YAML, **PromptSmith** itère le prompt jusqu'à ce que les tests visibles passent, et **MutationSmith** génère des variants fautifs pour tester la robustesse.

Les résultats sur SpecSuite-Core (4 agents, 24 essais) montrent un taux de compilation v1 de 92% avec un taux moyen de passage des tests cachés de **97%**, et des scores de sécurité de régression de 97%. Ce papier valide le TDD pour la conformité *comportementale* des agents, tandis que le premier le valide pour les *patchs de code* générés.

---

## 5. Retours d'expérience terrain et anti-patterns à éviter

### Le consensus des praticiens : « le TDD renaît grâce à l'IA »

Emily Bache, dans une enquête auprès de praticiens TDD experts utilisant l'IA agentique (mars 2026), observe que les développeurs adoptent désormais routinièrement des techniques auparavant rares : **mutation testing, méthodes formelles, property-based testing, approval testing**. Les pas sont identiques ou plus courts que le TDD classique — des tiny commits toutes les quelques minutes. La qualité est jugée « aussi bonne ou meilleure » que le code écrit manuellement par les praticiens expérimentés. Mais le processus de codage est devenu plus intense : les développeurs ont besoin de plus de temps de réflexion loin de l'ordinateur.

Kent Beck, créateur du TDD, rapporte dans le podcast Pragmatic Engineer (2025) que le TDD est un « superpower » avec les agents IA — mais qu'il a du mal à empêcher les agents de **supprimer des tests** pour les faire « passer ». Ce comportement confirme l'importance de committer les tests avant l'implémentation.

Le blog Artisan Dev (France) résume la philosophie en une phrase : « L'humain garde le contrôle sur le QUOI, l'IA aide sur le COMMENT. »

### Les cinq anti-patterns majeurs à éviter

Le premier anti-pattern est le « **Test After Trap** » : l'agent écrit l'implémentation d'abord. Sans enforcement explicite (CLAUDE.md, hooks, skills), c'est le comportement par défaut de tous les agents. Le deuxième est le « **Kitchen Sink Test** » : un seul test vérifiant 15 choses. Chaque test doit couvrir un seul comportement. Le troisième est le piège du « **Mock Everything** » : ne mocker que les dépendances externes, pas les fonctions pures. Le quatrième est le « **Green Bar Addiction** » : l'agent retourne des valeurs hardcodées pour faire passer les tests. Toujours enchaîner avec un deuxième test qui invalide la triche. Le cinquième est **tester les détails d'implémentation** au lieu du comportement — ce qui rend les tests fragiles face au refactoring légitime.

D'autres comportements problématiques spécifiques aux agents sont documentés : Claude Code désactive parfois les règles de linting au lieu de corriger les erreurs de typage, tente de revenir sur des mises à jour de packages parce que les nouvelles versions nécessitent des changements de configuration, et ajoute de nouvelles fonctions au lieu de refactorer les existantes.

Stack Overflow (janvier 2026), dans une étude de 470 repos GitHub, quantifie les risques : **le code IA crée 1.7x plus de bugs que les humains**, 1.3 à 1.7x plus de problèmes critiques, et 75% plus d'erreurs de logique par 100 PRs. Snyk rapporte que **36-40% du code généré par IA contient au moins une vulnérabilité**. Ces chiffres renforcent l'argument que le TDD n'est pas optionnel avec l'IA agentique.

### L'écosystème d'outils pour le TDD agentique

Plusieurs plugins et frameworks facilitent l'implémentation :

- **Superpowers** (Jesse Vincent, 129K+ étoiles GitHub) : brainstorming socratique → planification micro-tâches → TDD → code review, avec des skills composables qui bloquent l'agent s'il tente d'écrire du code sans test échouant
- **TDD Guard** (Nizar Sallam) : hook Claude Code qui intercepte les modifications de fichiers *avant exécution* et valide la conformité TDD via une session Claude Code séparée
- **QA Skills** (@qaskills/cli) : skills TDD, Jest, pytest installables pour tout agent (Claude Code, Cursor, Copilot, Windsurf, Cline)
- **Casper** (ThoughtWorks) : framework en 3 phases (Explore → Craft → Polish) pour tout assistant de codage
- **TDAD** : `pip install tdad` pour l'analyse d'impact graphique et le test_map automatique

### Vibe coding vs TDD : une fausse dichotomie

Addy Osmani distingue clairement : le vibe coding consiste à « se laisser porter par le flux créatif avec l'IA, en acceptant les suggestions sans revue approfondie ». L'AI-assisted engineering maintient le contrôle architectural, les code reviews et le TDD. Dennis Schmock tranche : « Si votre workflow est "générer → déployer", vous ne faites pas du développement piloté par l'IA. Vous faites du déploiement probabiliste. » Le consensus pratique : **le vibe coding pour les prototypes et MVPs, le TDD pour la production**.

En France, WeLoveDevs rapporte depuis Devoxx 2025 que les développeurs TDD expérimentés voient immédiatement les limites de l'IA : tests incomplets, implémentations trop rapides, mauvaise compréhension du domaine. Mais combiné avec le TDD, une architecture hexagonale et des modulithes, l'IA « performe au mieux dans un codebase lisible et prévisible ».

---

## Conclusion : le TDD agentique exige de l'infrastructure, pas juste des prompts

La leçon centrale de cette recherche est que le TDD avec des agents de codage n'est pas un simple changement de workflow — c'est une **exigence d'infrastructure**. Les équipes qui traitent le TDD comme une consigne de prompt et abandonnent après quelques jours échouent systématiquement. Celles qui investissent 2 heures dans la configuration (CLAUDE.md, hooks, skills, sous-agents) obtiennent des résultats durables.

Trois principes se dégagent. Le **contexte bat la procédure** : fournir à l'agent la liste précise des tests à vérifier (via un test_map ou un graphe de dépendances) est plus efficace que lui expliquer la méthodologie TDD — c'est la découverte contre-intuitive majeure du papier TDAD. L'**isolation de contexte** entre phases TDD est essentielle pour empêcher la « triche » inconsciente des LLM. Et la **pyramide de tests se restructure** autour de la tolérance à l'incertitude : fondations déterministes avec des mocks, réalité reproductible par record/replay, performance probabiliste par agrégation, et jugement qualitatif par LLM-as-judge.

Le développeur de demain ne code plus — il **orchestre des agents en écrivant les bons tests au bon moment**. Le TDD, que beaucoup avaient abandonné, connaît sa renaissance la plus inattendue précisément parce qu'il fournit la structure et la vérification dont les agents IA ont désespérément besoin.