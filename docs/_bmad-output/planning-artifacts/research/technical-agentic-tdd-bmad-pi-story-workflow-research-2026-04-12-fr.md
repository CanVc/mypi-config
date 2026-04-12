---
stepsCompleted: [1, 2, 3, 4, 5, 6]
inputDocuments:
  - 'docs/research/tdd-initiative'
  - 'docs/_bmad-output/planning-artifacts/product-brief-mypi-config.md'
workflowType: 'research'
lastStep: 6
research_type: 'technique'
research_topic: 'TDD agentique pour un workflow de story BMAD/Pi'
research_goals: 'Mener une recherche exhaustive sur les pratiques de TDD agentique dans l’industrie, puis en déduire un cycle TDD concret et un workflow complet de travail sur une story pour BMAD piloté par Pi dans une configuration multi-modèle.'
user_name: 'Cvc'
date: '2026-04-12'
web_research_enabled: true
source_verification: true
---

# Rapport de recherche : technique

**Date :** 2026-04-12
**Auteur :** Cvc
**Type de recherche :** technique

---

## Vue d’ensemble de la recherche

Cette recherche a examiné les pratiques industrielles actuelles autour du TDD agentique, puis a traduit les patterns les plus solides vers un workflow compatible avec un environnement **BMAD spec-first** et **piloté par Pi**. Le corpus de sources combine documentation éditeur en direct, articles de recherche et de benchmark, handbooks d’ingénierie, ainsi que documentation d’outillage à jour au 2026-04-12. Comme BMAD et Pi restent relativement de niche, l’analyse a délibérément regardé au-delà de cet écosystème pour étudier le paysage plus large des coding agents, avant de réinjecter les résultats dans votre modèle opératoire spécifique.

Le constat le plus important est que l’industrie converge vers des **workflows verification-first, artifact-centric et multi-étapes**, plutôt que vers de longues sessions de code centrées sur le chat. Les patterns les plus solides insistent de manière répétée sur : tests explicitement en échec, handoffs à contexte frais, outillage repo-native, vérification runtime, boucles de réparation bornées et gates de revue finale plus stricts. Les meilleurs exemples actuels ne sont pas simplement « demander au modèle de faire du TDD », mais des boucles structurées telles que **red/green TDD**, **planner/generator/healer** et **explore/revise/debug/generate-tests**.

Pour votre projet, la destination recommandée est une **machine à états centrée sur la story** : la story BMAD entre, un execution brief en sort, les tests échouent d’abord, l’implémentation passe au vert, puis viennent le refactor et l’élargissement des validations, la vérification runtime, la revue par deux modèles, une boucle de réparation bornée, puis une décision humaine de merge ou d’escalade. Pi est particulièrement adapté ici parce qu’il est volontairement personnalisable via skills, extensions, SDK, sessions et configuration de modèles personnalisés ; cela le rend bien adapté à l’implémentation d’un workflow plus opinionné que son comportement par défaut. Voir le **Résumé exécutif** et la **Section 8** pour le cycle TDD final et le workflow de story recommandés.

---

# De la story au merge sûr : recherche technique complète sur le TDD agentique pour un workflow de story BMAD/Pi

## Résumé exécutif

Le TDD agentique émerge comme un **problème de conception de workflow**, pas simplement comme une astuce de prompting. Dans la documentation et la recherche actuelles, les meilleurs résultats viennent de systèmes qui donnent à l’agent un moyen de vérifier son travail, le contraignent avec des outils repo-native, décomposent le travail en rôles plus petits et conservent des preuves à chaque gate. Les best practices de Claude Code chez Anthropic mettent en avant la vérification, la planification avant le code, la gestion agressive du contexte et une décomposition de type subagent. Simon Willison et Tweag présentent tous deux le red/green TDD comme particulièrement efficace avec les coding agents. L’article TDFlow formalise ce même instinct dans un cadre de recherche en décomposant l’ingénierie logicielle à l’échelle du dépôt en sous-agents fortement contraints pour l’exploration, la révision, le debugging et la génération de tests. Les agents planner/generator/healer intégrés à Playwright montrent même que la vérification runtime devient explicitement agent-oriented.

L’implication pratique est claire : **« faire du TDD » est trop vague pour des agents.** Ce qui fonctionne, c’est une boucle plus précise : identifier le comportement d’acceptation, le mapper à des tests exacts, créer ou mettre à jour des tests pour qu’ils échouent pour la bonne raison, n’implémenter que jusqu’à ce que ces tests ciblés passent, élargir ensuite la validation, puis effectuer une vérification runtime et une revue multi-perspective. En d’autres termes, l’industrie passe d’instructions procédurales TDD à des **boucles de delivery ciblées par les tests et riches en preuves**. Les tests générés et la génération de tests juste-à-temps deviennent de plus en plus importants, mais ils ne remplacent pas encore les tests d’acceptation rédigés autour du comportement ; ils viennent plutôt les compléter.

Pour votre environnement, le modèle opératoire recommandé est un **workflow centré sur la story BMAD, orchestré par Pi et multi-modèle**, avec handoffs à contexte frais entre chaque phase. BMAD doit rester la source canonique du périmètre et de l’intention d’acceptation. Pi doit agir comme couche d’orchestration, d’abord via des skills, puis, si souhaité, via une extension ou une machine à états pilotée par le SDK. Les modèles les plus forts doivent être réservés à la planification, à la revue finale et au debugging difficile, tandis que les modèles moins coûteux ou plus rapides effectuent la majorité du travail d’implémentation. Les modèles locaux Ollama doivent rester limités à des tâches à faible risque et fortement bornées jusqu’à ce qu’ils gagnent leur place par benchmark. Le résultat visé est un workflow de discipline autonome, et non de « vibe coding » : la story entre, une preuve mesurable en sort.

**Constats techniques clés :**

- L’industrie converge vers des **boucles agentiques verification-heavy et CLI-first** plutôt que vers du code librement mené par des sessions de chat.
- Les patterns les plus solides sont les **handoffs à contexte frais**, les **tests ciblés en échec**, l’**exécution repo-native** et les **boucles de réparation bornées**.
- La validation runtime est désormais un sujet de premier plan ; la stack agentique de Playwright est un signal fort que la **vérification E2E doit vivre à l’intérieur de la boucle de delivery**, et non après coup.
- La décomposition structurée compte : planner/generator/healer, subagents et boucles patch-debug-test surperforment de manière répétée les sessions monolithiques en fiabilité et en auditabilité.
- Git, logs, traces, artefacts CI et handoffs markdown comptent davantage qu’une base de données de workflow dédiée dans les implémentations précoces.
- Pi est bien positionné pour implémenter cela parce qu’il supporte **skills, extensions, contrôle SDK, sessions, routage de modèles et providers personnalisés**, tandis que BMAD fournit déjà les artefacts de story qui manquent souvent aux workflows agentiques.

**Recommandations techniques :**

- Faire du **fichier de story BMAD l’artefact d’entrée canonique** de chaque run d’implémentation.
- Imposer un cycle **Red → Green → Refactor → Runtime Verify → Dual Review** avec des preuves explicites à chaque gate.
- Utiliser des **sessions Pi fraîches ou des prompts fortement bornés par étape** au lieu d’une longue conversation unique.
- Router les modèles par rôle : modèles forts pour planification/revue, modèles efficients pour implémentation, modèles locaux uniquement pour du support borné.
- Limiter les boucles de réparation à **2–3 itérations** avant escalade vers l’humain.
- Persister les produits de travail sous forme de **markdown de story, logs, traces, sorties de tests et findings de revue** dans les artefacts d’implémentation.

## Table des matières

1. Introduction et méthodologie de la recherche technique
2. Paysage technique et analyse d’architecture du TDD agentique
3. Approches d’implémentation et bonnes pratiques
4. Évolution de la stack technologique et tendances actuelles
5. Patterns d’intégration et d’interopérabilité
6. Analyse de performance et de scalabilité
7. Considérations de sécurité et de conformité
8. Recommandations techniques stratégiques
9. Feuille de route d’implémentation et évaluation des risques
10. Perspectives techniques futures et opportunités d’innovation
11. Méthodologie de recherche et vérification des sources
12. Annexes techniques et documents de référence
13. Conclusion de la recherche technique

## 1. Introduction et méthodologie de la recherche technique

### Importance de la recherche technique

Le coding agentique est passé du statut de nouveauté à celui de pratique d’ingénierie sérieuse, mais le modèle opératoire qui l’entoure reste instable. L’attention publique se concentre aujourd’hui surtout autour de Claude Code et d’outils adjacents, alors que les patterns sous-jacents dépassent largement un seul harness. En parallèle, votre product brief rend l’objectif du projet inhabituellement concret : il ne s’agit pas d’une plateforme générique d’IA pour le code, mais d’un **moteur de delivery portable, piloté par les stories**, qui transforme les artefacts BMAD en boucles d’implémentation disciplinées avec routage multi-modèle, contexte frais et exécution TDD-first. Cette combinaison rend la recherche stratégiquement importante : la question n’est pas seulement de savoir si le TDD reste pertinent avec des agents, mais comment reconcevoir toute la boucle de delivery pour que le TDD devienne imposable, auditable et réutilisable.

L’importance de cette recherche est donc double. D’abord, elle identifie ce qui fonctionne réellement dans l’industrie plus large autour des coding agents et des boucles pilotées par les tests. Ensuite, elle filtre ces résultats en une méthode implémentable en **BMAD + Pi**, plutôt que dans l’environnement par défaut de Claude Code. Cette étape d’adaptation compte parce que la philosophie de Pi consiste explicitement à adapter le harness au workflow, et non l’inverse.

_Source : `docs/_bmad-output/planning-artifacts/product-brief-mypi-config.md`; https://code.claude.com/docs/en/best-practices ; `/home/cvc/.nvm/versions/node/v24.14.1/lib/node_modules/@mariozechner/pi-coding-agent/README.md`._

### Méthodologie de recherche technique

La recherche a combiné cinq classes de sources :

- **Documentation éditeur primaire** pour les capacités produit en direct et les workflows voulus
- **Articles de recherche et benchmarks** pour l’évidence structurée et la méthodologie explicite
- **Handbooks d’ingénierie et guides techniques** pour les patterns de workflow transverses aux vendors
- **Documentation de frameworks de test** pour les capacités de vérification actuelles
- **Artefacts projet locaux et documentation Pi** pour l’adaptation à l’environnement BMAD/Pi

L’analyse a été organisée autour des questions suivantes :

1. Que dit l’industrie aujourd’hui sur le TDD agentique ?
2. Quels patterns reviennent de manière répétée à travers des sources indépendantes ?
3. Lesquels de ces patterns sont réellement transférables à un environnement BMAD/Pi ?
4. Quel workflow final de story satisfait le mieux les objectifs du product brief ?

Le document qui en résulte distingue délibérément :

- les **patterns cross-sources à forte confiance**
- les **pratiques prometteuses mais encore émergentes**
- les **décisions d’adaptation spécifiques à votre workflow**

_Source : https://code.claude.com/docs/en/best-practices ; https://simonwillison.net/guides/agentic-engineering-patterns/red-green-tdd/ ; https://tweag.github.io/agentic-coding-handbook/WORKFLOW_TDD/ ; https://arxiv.org/html/2510.23761v1 ; https://playwright.dev/docs/test-agents ; https://engineering.fb.com/2026/02/11/developer-tools/the-death-of-traditional-testing-agentic-development-jit-testing-revival/._

### Objectifs de la recherche technique

**Objectif technique initial :** Mener une recherche exhaustive sur les pratiques de TDD agentique dans l’industrie, puis en déduire un cycle TDD concret et un workflow complet de travail sur une story pour BMAD piloté par Pi dans une configuration multi-modèle.

**Objectifs effectivement atteints :**

- Identification des patterns d’architecture les plus solides pour le TDD agentique et le développement verification-heavy
- Cartographie des écosystèmes d’outillage les plus pertinents pour unit, intégration, runtime, CI et revue
- Détermination des pratiques industrielles qui se transfèrent proprement vers BMAD/Pi, et de celles qui se transfèrent moins bien
- Production d’un workflow de story BMAD/Pi recommandé avec phases, gates, artefacts et guidance de routage de modèles explicites
- Capture des principaux risques, métriques de succès et phases d’adoption pour l’implémentation

_Source : ensemble du corpus de recherche listé en Section 11, plus les entrées locales `docs/research/tdd-initiative` et `docs/_bmad-output/planning-artifacts/product-brief-mypi-config.md`._

## 2. Paysage technique et analyse d’architecture du TDD agentique

### Patterns architecturaux techniques actuels

La recherche pointe vers cinq patterns d’architecture récurrents.

**1. Verification-first, pas prompt-first.** La documentation actuelle des best practices de Claude Code dit explicitement qu’il faut « donner à Claude un moyen de vérifier son travail » et place la vérification avant les raffinements génériques de prompting. C’est le changement architectural le plus important du domaine. Les workflows matures partent du principe que l’agent doit exécuter des tests, du lint, des traces ou des scripts pour prouver la correction, plutôt que de simplement l’affirmer.

**2. La décomposition des rôles bat les sessions monolithiques.** Le modèle Playwright Test Agents découpe le travail en planner, generator et healer. TDFlow découpe la réparation à l’échelle dépôt en exploration, révision de patch, debugging et génération de tests. Claude Code ajoute des subagents personnalisés et des hooks. À travers toutes les sources, le message est le même : la fiabilité augmente quand le travail est décomposé en étapes plus étroites, avec des instructions différentes et, souvent, des modèles différents.

**3. Le contexte frais est une contrainte de design de premier ordre.** Claude Code recommande une gestion agressive du contexte et l’usage de multiples sessions. Votre product brief appelle indépendamment à des handoffs à contexte frais entre les phases. C’est un point de convergence très fort : la meilleure architecture ne laisse pas un seul thread accumuler un bruit illimité.

**4. Les control planes centrés sur les artefacts surperforment ceux centrés sur la mémoire.** Aider met en avant git, la diffabilité, les boucles lint/test et la cartographie du dépôt. SWE-bench met en avant des environnements Dockerisés reproductibles pour l’évaluation. En d’autres termes, le control plane n’est pas une mémoire cachée d’agent ; c’est un ensemble d’artefacts observables : fichiers de story, diffs, commandes de test, logs, traces, findings de revue et sorties CI.

**5. Une autonomie bornée vaut mieux qu’une autonomie sans limite.** Claude Code expose des permission modes, des hooks et des contrôles GitHub Actions ; la boucle agentique de Playwright est explicitement stagée ; TDFlow exécute des sous-agents contraints. Les meilleurs systèmes ne retirent pas le contrôle. Ils automatisent à l’intérieur de frontières bien définies.

_Source : https://code.claude.com/docs/en/best-practices ; https://docs.anthropic.com/en/docs/claude-code/sub-agents ; https://docs.anthropic.com/en/docs/claude-code/hooks ; https://playwright.dev/docs/test-agents ; https://arxiv.org/html/2510.23761v1 ; https://aider.chat/ ; https://www.swebench.com/SWE-bench/guides/docker_setup/._

### Principes de design système et bonnes pratiques

À partir de ces patterns, les principes architecturaux les plus nets pour votre workflow sont les suivants :

- **Une seule unité de travail canonique :** le fichier de story BMAD
- **Un seul mécanisme de succès canonique :** une preuve exécutable, pas une confiance verbale
- **Une seule étape, un seul but :** chaque run a un objectif étroit et un contexte minimal
- **Une seule piste de preuves :** chaque phase laisse des artefacts exploitables par la suivante
- **Une seule règle d’escalade :** si la boucle ne converge pas, on arrête et on escalade au lieu de thrash

Cela implique un workflow de story qui se comporte davantage comme une **machine à états** que comme une conversation. Chaque transition doit être explicite :

- story acceptée pour implémentation
- execution brief produit
- tests qui échouent pour la raison prévue
- implémentation ciblée qui passe au vert
- validation plus large qui passe
- preuves runtime collectées
- findings de revue levés
- décision humaine de merge prise

Cette architecture est plus rigide que le coding interactif générique, mais c’est précisément ce qui rend le TDD agentique viable.

_Source : https://simonwillison.net/guides/agentic-engineering-patterns/red-green-tdd/ ; https://tweag.github.io/agentic-coding-handbook/WORKFLOW_TDD/ ; https://code.claude.com/docs/en/best-practices ; `docs/_bmad-output/planning-artifacts/product-brief-mypi-config.md`._

### Attributs de qualité architecturale

Dans ce domaine, les attributs de qualité décisifs ne sont pas seulement la performance et l’extensibilité, mais aussi :

- **Déterminisme :** peut-on rejouer la même étape avec les mêmes entrées ?
- **Auditabilité :** un humain peut-il inspecter ce qui s’est passé et pourquoi ?
- **Remplaçabilité :** peut-on remplacer le modèle ou l’outil sans redessiner le process ?
- **Contrôle des coûts :** peut-on réserver les modèles premium aux endroits où ils comptent vraiment ?
- **Résistance aux régressions :** la boucle peut-elle prouver qu’elle n’a pas cassé le comportement voisin ?

La combinaison BMAD/Pi s’aligne bien avec ces attributs. BMAD apporte des artefacts de planification structurés ; Pi apporte un harness adaptable via skills, SDK, outils personnalisés, sessions et définitions de modèles personnalisés. L’absence de subagents câblés en dur dans Pi n’est pas une faiblesse ici ; c’est précisément ce qui vous permet d’imposer votre propre architecture.

_Source : `/home/cvc/.nvm/versions/node/v24.14.1/lib/node_modules/@mariozechner/pi-coding-agent/README.md` ; `/home/cvc/.nvm/versions/node/v24.14.1/lib/node_modules/@mariozechner/pi-coding-agent/docs/skills.md` ; `/home/cvc/.nvm/versions/node/v24.14.1/lib/node_modules/@mariozechner/pi-coding-agent/docs/sdk.md` ; `docs/_bmad-output/planning-artifacts/product-brief-mypi-config.md`._

## 3. Approches d’implémentation et bonnes pratiques

### Méthodologies d’implémentation actuelles

L’industrie utilise aujourd’hui plusieurs patterns d’implémentation distincts, chacun utile pour une tranche différente du cycle de vie d’une story.

| Pattern | Ce que c’est | Force | Faiblesse | Pertinence pour BMAD/Pi |
|---|---|---|---|---|
| Red/Green/Refactor | Écrire des tests en échec, implémenter jusqu’au vert, puis nettoyer | Discipline comportementale forte, modèle mental simple | Facile à simuler par les agents si la preuve d’échec n’est pas explicite | Boucle centrale unit/intégration |
| Boucle de résolution de tests ciblés | Traiter le travail comme le fait de faire passer des tests connus en échec sans casser les tests de régression | Excellent pour le debugging et la réparation | Peut rater des comportements manquants si aucun test n’est écrit d’abord | Boucle centrale de réparation |
| Planner/Generator/Healer | Découper le travail runtime/E2E en planification, génération de tests et guérison | Très bon fit pour la validation UI/runtime | Peut surproduire des tests fragiles si le plan est mauvais | Pattern E2E fort |
| JiT regression testing | Générer des tests de capture juste avant l’atterrissage du changement | Prometteur dans des environnements à haute vélocité | Encore émergent et potentiellement bruyant | Amélioration future |
| Boucle auto lint/test/fix | Lancer lint/tests après chaque changement et laisser l’agent réparer | Feedback rapide et forte valeur pratique | Insuffisant seul sans intention d’acceptation | Boucle d’hygiène de base |

En pratique, le meilleur workflow pour votre projet est un **hybride** :

- utiliser le classique red/green/refactor pour le comportement unit et intégration,
- utiliser la résolution de tests ciblés pour les réparations,
- utiliser les idées planner/generator/healer pour la validation runtime et navigateur,
- traiter les tests JiT générés comme un supplément futur, plutôt que comme le cœur du MVP.

_Source : https://simonwillison.net/guides/agentic-engineering-patterns/red-green-tdd/ ; https://tweag.github.io/agentic-coding-handbook/WORKFLOW_TDD/ ; https://arxiv.org/html/2510.23761v1 ; https://playwright.dev/docs/test-agents ; https://engineering.fb.com/2026/02/11/developer-tools/the-death-of-traditional-testing-agentic-development-jit-testing-revival/ ; https://aider.chat/._

### Framework d’implémentation et outillage

L’image de l’outillage est inhabituellement claire :

- **Aider** démontre la valeur pratique d’une exécution automatique de lint/test après chaque changement, avec des diffs git-native et un support large des langages.
- **Pytest** reste une base forte côté back-end parce que fixtures, paramétrisation, plugins, reruns et gestion explicite des échecs se mappent naturellement à des boucles de réparation itératives.
- **Vitest** devient de plus en plus agent-friendly, en mettant explicitement en avant « Writing Tests with AI », browser mode, coverage et parallelism dans sa documentation.
- **Playwright** fournit désormais des test agents dédiés qui couvrent la planification, la génération et l’auto-réparation pour les flux navigateur.
- **GitHub Actions** fournit l’épine dorsale standard d’automatisation pour artefacts, cache, concurrence et runners self-hosted optionnels.
- **OpenHands** renforce l’importance des PR reviewables et de workflows personnalisables avec testing et validation dans la boucle.

La leçon d’ingénierie est que le workflow agentique ne doit pas inventer un outillage de vérification exotique. Il doit composer les meilleurs outils repo-native existants sous une couche d’orchestration plus stricte.

_Source : https://aider.chat/ ; https://docs.pytest.org/en/stable/contents.html ; https://vitest.dev/guide/ ; https://playwright.dev/docs/test-agents ; https://docs.github.com/en/actions ; https://openhands.dev/._

## 4. Évolution de la stack technologique et tendances actuelles

### Paysage actuel de la stack technologique

La stack du TDD agentique se sépare naturellement en cinq plans.

**Plan de contrôle.** Le moteur de workflow est généralement terminal-first et implémenté dans des écosystèmes bons pour le tool calling et l’automatisation, surtout Node/TypeScript et Python. Pi se place très bien ici via ses skills, extensions et son contrôle par SDK.

**Plan modèle.** La pratique actuelle favorise plusieurs modèles plutôt qu’un modèle universel unique. Les modèles premium sont utilisés là où l’échec coûte le plus cher — planification, debugging difficile et revue finale — tandis que des modèles plus rapides ou moins coûteux effectuent la majeure partie du travail d’implémentation et des transformations à faible risque.

**Plan vérification.** La stack dominante reste repo-native : pytest ou Vitest pour les boucles internes rapides, Playwright pour la preuve navigateur/runtime, outils de lint/format pour l’hygiène, runners CI pour la reproductibilité.

**Plan état.** Le système de record est généralement git plus les artefacts, pas une base de données. Diffs, logs, traces, sorties JUnit, handoffs markdown et artefacts CI cachés comptent davantage qu’une DB d’orchestrateur dédiée dans les versions précoces.

**Plan environnement.** Les runners reproductibles, les environnements d’évaluation Dockerisés et les self-hosted runners optionnels comptent pour la cohérence, la sécurité et la vitesse.

Pour votre environnement, la correspondance est directe :

- **BMAD** fournit le planification/spécification.
- **Pi** fournit le plan de contrôle.
- **glm-5.1 / sonnet-4.6 / gpt-5.4 / opus-4.6** fournissent le plan modèle.
- **pytest / Vitest / Playwright / linting repo-native** fournissent le plan vérification.
- **git + artefacts scoped par story** fournissent le plan état.

_Source : https://code.claude.com/docs/en/best-practices ; https://aider.chat/ ; https://openhands.dev/ ; https://playwright.dev/docs/intro ; https://docs.github.com/en/actions ; https://www.swebench.com/SWE-bench/guides/docker_setup/ ; `/home/cvc/.nvm/versions/node/v24.14.1/lib/node_modules/@mariozechner/pi-coding-agent/docs/sdk.md` ; `/home/cvc/.nvm/versions/node/v24.14.1/lib/node_modules/@mariozechner/pi-coding-agent/docs/models.md`._

### Patterns d’adoption technologique

Plusieurs tendances d’adoption semblent désormais stables :

- **Les agents CLI-first sont plus matures que les flux IDE-only** pour l’automatisation sérieuse.
- **MCP devient le standard d’intégration d’outils** pour les applications IA qui doivent se connecter à des systèmes externes.
- **Les tests générés montent en puissance**, mais les tests d’acceptation rédigés restent le noyau le plus sûr.
- **La pensée benchmark se diffuse** : les équipes raisonnent de plus en plus en termes de reproductibilité, résistance aux régressions et qualité de workflow mesurable.
- **Les modèles locaux sont utiles, mais la confiance est hiérarchisée.** La bonne pratique actuelle consiste à restreindre les modèles locaux faibles ou à faible contexte à des tâches bornées tant qu’ils n’ont pas été benchmarkés.

Le support des modèles personnalisés dans Pi est particulièrement pertinent ici. Il peut router vers des providers compatibles OpenAI comme Ollama, tout en gardant l’architecture du workflow indépendante de tout vendor unique. Cela en fait un plan de contrôle solide à long terme pour votre stratégie multi-modèle.

_Source : https://modelcontextprotocol.io/introduction ; https://engineering.fb.com/2026/02/11/developer-tools/the-death-of-traditional-testing-agentic-development-jit-testing-revival/ ; https://www.swebench.com/ ; `/home/cvc/.nvm/versions/node/v24.14.1/lib/node_modules/@mariozechner/pi-coding-agent/docs/models.md` ; `docs/_bmad-output/planning-artifacts/product-brief-mypi-config.md`._

## 5. Patterns d’intégration et d’interopérabilité

### Patterns de design d’API

Pour les workflows de TDD agentique, l’« API » la plus importante n’est généralement pas GraphQL ou REST au cœur de la boucle ; c’est la **frontière outillage** entre l’orchestrateur et l’environnement d’exécution. MCP est désormais le standard généraliste le plus net dans cet espace, se décrivant comme un standard ouvert pour connecter des applications IA à des systèmes externes, des outils, des sources de données et des workflows. La documentation MCP de Claude Code renforce cette vision en supportant des serveurs locaux en stdio, des serveurs distants HTTP/SSE, des mises à jour dynamiques d’outils et des scopes séparés local/projet/utilisateur.

Pour votre workflow, cela implique une règle pratique :

- garder la boucle cœur d’implémentation **locale et CLI-native** autant que possible,
- n’ajouter MCP que pour les systèmes externes qui en ont réellement besoin,
- scoper chaque intégration au périmètre pratique le plus étroit.

Cette approche préserve le déterminisme et garde la boucle de story compréhensible.

_Source : https://modelcontextprotocol.io/introduction ; https://docs.anthropic.com/en/docs/claude-code/mcp ; `/home/cvc/.nvm/versions/node/v24.14.1/lib/node_modules/@mariozechner/pi-coding-agent/docs/sdk.md`._

### Protocoles de communication

Les protocoles dominants dans le TDD agentique pratique sont :

- **shell/stdout/stderr** pour le travail local dans le dépôt,
- **HTTP ou SSE** pour l’intégration d’outils distants et MCP,
- **événements git et CI** pour l’automatisation inter-étapes,
- **sorties de test runners et traces** pour une validation lisible par machine.

C’est un bon fit pour Pi, nativement centré terminal et extensible via SDK et outils personnalisés. Autrement dit, le workflow n’a pas besoin d’un protocole d’orchestration sur mesure ; il a besoin d’un contrat propre autour de l’exécution des outils et du passage d’artefacts.

_Source : https://docs.anthropic.com/en/docs/claude-code/mcp ; https://docs.github.com/en/actions ; `/home/cvc/.nvm/versions/node/v24.14.1/lib/node_modules/@mariozechner/pi-coding-agent/docs/sdk.md`._

### Formats de données et standards

Une stack d’interopérabilité pratique pour votre workflow doit rester simple :

- **Markdown** pour les handoffs lisibles par humains, execution briefs, plans de test, findings de revue
- **JSON** pour les gates lisibles par machine, payloads de statut ou métadonnées d’orchestration
- **JUnit/coverage/traces/screenshots/videos** pour les preuves de vérification
- **git diffs et résumés de patch** pour la provenance des changements

Markdown est particulièrement attractif parce que les stories BMAD sont déjà artifact-centric et que le markdown se consomme facilement par les humains comme par les modèles. JSON ne doit être utilisé que là où l’automatisation en bénéficie clairement.

_Source : https://docs.github.com/en/actions ; https://playwright.dev/docs/test-agents ; https://www.swebench.com/SWE-bench/guides/docker_setup/ ; `docs/_bmad-output/planning-artifacts/product-brief-mypi-config.md`._

### Approches d’interopérabilité système

Le moteur de workflow lui-même doit privilégier une **intégration point-à-point** plutôt qu’un middleware lourd. Dans un workflow de story mono-dépôt, gateways d’API, service meshes ou bus d’entreprise sont généralement excessifs. L’architecture efficace la plus simple est :

1. un artefact de story en markdown,
2. des outils repo-native via le shell,
3. MCP optionnel pour les systèmes externes,
4. un runner CI pour la reproductibilité,
5. git et des dossiers d’artefacts comme piste d’audit persistante.

C’est largement suffisant pour le MVP et probablement pendant longtemps ensuite.

_Source : https://modelcontextprotocol.io/introduction ; https://docs.github.com/en/actions ; https://aider.chat/ ; `/home/cvc/.nvm/versions/node/v24.14.1/lib/node_modules/@mariozechner/pi-coding-agent/README.md`._

### Patterns d’intégration microservices

Les patterns microservices importent surtout pour le **produit testé**, pas pour le **moteur de workflow**. Pour la couche d’orchestration, un design microservice distribué ajouterait de la complexité sans gain évident. Un design de machine à états ou de pipeline avec frontières de phase explicites est un meilleur fit. Le workflow peut tout à fait s’intégrer à des systèmes microservices testés en utilisant leurs tests repo-native, leurs environnements locaux compose/dev, leurs tests d’API et leurs vérifications navigateur quand c’est pertinent.

_Source : https://playwright.dev/docs/ci ; https://docs.github.com/en/actions ; https://arxiv.org/html/2510.23761v1 ._

### Intégration event-driven

L’intégration event-driven est utile aux frontières :

- hooks avant ou après exécution d’outil,
- triggers CI sur push ou PR,
- contrôles qualité planifiés ou en arrière-plan,
- notifications ou mises à jour de statut à l’issue des phases de story.

La référence hooks de Claude Code est instructive ici, car elle montre comment formaliser le decision control et les gates pré-tool. Pi peut implémenter des comportements analogues via extensions, outils personnalisés ou logique d’orchestration pilotée par SDK.

_Source : https://docs.anthropic.com/en/docs/claude-code/hooks ; `/home/cvc/.nvm/versions/node/v24.14.1/lib/node_modules/@mariozechner/pi-coding-agent/docs/sdk.md`._

### Patterns de sécurité d’intégration

Les patterns de sécurité qui comptent le plus dans ce domaine sont :

- **scopes d’outils à privilège minimum**,
- **scopes d’intégration séparés local/projet/utilisateur**,
- **permission modes explicites ou contrôles par hooks**,
- **gestion des secrets hors des prompts et artefacts markdown**,
- **self-hosted runners optionnels pour les codebases sensibles**.

Le message pratique est que la puissance d’intégration ne doit grandir qu’en même temps que la vérification et le contrôle d’accès.

_Source : https://docs.anthropic.com/en/docs/claude-code/mcp ; https://docs.anthropic.com/en/docs/claude-code/hooks ; https://docs.github.com/en/actions ; `/home/cvc/.nvm/versions/node/v24.14.1/lib/node_modules/@mariozechner/pi-coding-agent/docs/models.md`._

## 6. Analyse de performance et de scalabilité

### Caractéristiques de performance et optimisation

L’insight de performance le plus important est que **le coût et la latence de la boucle interne sont dominés par la taille du contexte et la portée des tests**. Les tokens de grands modèles sont coûteux ; les suites de tests géantes sont lentes. La meilleure mitigation est architecturale, pas cosmétique :

- utiliser des **handoffs à contexte frais** pour éviter les conversations gonflées,
- exécuter des **tests ciblés** dans la boucle interne,
- n’élargir la surface de test qu’après obtention d’états verts localisés,
- réserver les modèles premium aux phases à fort levier.

C’est cohérent avec la boucle lint/test automatique d’Aider, les conseils de gestion de contexte de Claude Code et les infrastructures orientées benchmark comme l’évaluation Dockerisée de SWE-bench. En pratique, le workflow le moins cher et correct n’est pas celui qui utilise le plus faible modèle ; c’est celui qui minimise le contexte inutile et la vérification inutile.

_Source : https://aider.chat/ ; https://code.claude.com/docs/en/best-practices ; https://www.swebench.com/SWE-bench/guides/docker_setup/ ; `docs/_bmad-output/planning-artifacts/product-brief-mypi-config.md`._

### Patterns et approches de scalabilité

Le workflow doit scaler en **séparant le travail**, et non en allongeant les sessions. Le pattern scalable est :

- une étape, une session ou un prompt fortement borné
- fan-out optionnel pour investigation ou revue
- handoff par artefacts entre étapes
- boucles de réparation plafonnées
- checkpointing et branching explicites

Le modèle de session de Pi, sa navigation d’arbre, sa compaction et son model switching rendent cela particulièrement viable. Vous pouvez traiter chaque phase de story soit comme une session fraîche, soit comme un checkpoint branchable, plutôt que d’essayer de tout préserver dans une seule conversation.

_Source : `/home/cvc/.nvm/versions/node/v24.14.1/lib/node_modules/@mariozechner/pi-coding-agent/README.md` ; `/home/cvc/.nvm/versions/node/v24.14.1/lib/node_modules/@mariozechner/pi-coding-agent/docs/sdk.md` ; https://code.claude.com/docs/en/best-practices ._

### Monitoring et mesure

Le workflow doit mesurer plus que le simple pass/fail. Les métriques recommandées sont :

- temps jusqu’au premier test en échec
- temps jusqu’au premier vert
- nombre de boucles de réparation par story
- part des stories ayant atteint la vérification runtime
- nombre de findings bloquants par passe de revue
- coût par story, par phase et par modèle
- taux d’escalade humaine
- régressions échappées après merge

Ces métriques comptent parce qu’elles permettent de calibrer empiriquement le routage des modèles, la portée des tests et les frontières de phases, au lieu de les deviner.

_Source : https://www.swebench.com/ ; https://docs.github.com/en/actions ; `docs/_bmad-output/planning-artifacts/product-brief-mypi-config.md`._

## 7. Considérations de sécurité et de conformité

### Bonnes pratiques et cadres de sécurité

Trois principes de sécurité dominent la recherche :

1. **privilège minimum pour les outils et les intégrations**
2. **séparer les credentials des prompts et des artefacts**
3. **rendre les gates imposables, non simplement consultatifs**

Les scopes MCP, hooks, permission controls et l’intégration GitHub Actions de Claude Code renforcent tous cette idée. Pi permet lui aussi de garder credentials et définitions de modèles hors du contenu des prompts, ce qui est essentiel si le workflow devient plus automatisé.

_Source : https://docs.anthropic.com/en/docs/claude-code/mcp ; https://docs.anthropic.com/en/docs/claude-code/hooks ; https://docs.anthropic.com/en/docs/claude-code/github-actions ; `/home/cvc/.nvm/versions/node/v24.14.1/lib/node_modules/@mariozechner/pi-coding-agent/docs/models.md`._

### Paysage de menaces

Les principaux risques dans le TDD agentique ne se limitent pas aux vulnérabilités applicatives traditionnelles. Ils incluent :

- **test hacking ou faux états verts**
- **prompt injection via des fichiers du dépôt, des docs externes ou des sorties d’outils**
- **fuite de secrets via des outils shell ou MCP sur-privilégiés**
- **monoculture de revue**, quand la même classe de modèle rate deux fois le même défaut
- **changements autonomes dangereux**, surtout avec des modèles plus faibles ou mal scopés

La préoccupation de TDFlow autour de la réduction du test hacking est particulièrement pertinente ici : un workflow qui optimise uniquement le fait que « les tests passent » sans preuve comportementale peut quand même échouer.

_Source : https://arxiv.org/html/2510.23761v1 ; https://docs.anthropic.com/en/docs/claude-code/hooks ; https://docs.github.com/en/actions ._

### Conformité, audit et gouvernance

Même dans un workflow solo, l’auditabilité compte. Le workflow doit laisser :

- un historique git,
- une piste d’artefacts scoped par story,
- des sorties de tests et de runtime,
- des findings de revue,
- une décision humaine de merge ou d’escalade.

Cela satisfait déjà une gouvernance pratique, même avant toute exigence formelle de conformité. Si le workflow évolue ensuite vers des environnements sensibles ou régulés, la même structure pourra être étendue avec des self-hosted runners, une gestion plus stricte des secrets et des hooks de politique spécifiques à l’organisation.

_Source : https://docs.github.com/en/actions ; `/home/cvc/.nvm/versions/node/v24.14.1/lib/node_modules/@mariozechner/pi-coding-agent/README.md` ; `/home/cvc/.nvm/versions/node/v24.14.1/lib/node_modules/@mariozechner/pi-coding-agent/docs/sdk.md`._

## 8. Recommandations techniques stratégiques

### Cadre de décision et stratégie technique

L’architecture recommandée pour votre workflow est :

- **BMAD fournit la story canonique et les artefacts de planification**
- **Pi fournit la couche d’orchestration et de routage de modèles**
- **Les outils repo-native fournissent les mécanismes de vérification**
- **Les artefacts scoped par story fournissent mémoire et auditabilité**
- **Les humains fournissent l’autorité finale quand la convergence échoue ou que le risque monte**

Il ne s’agit pas d’un workflow générique de « coding assistant IA ». C’est une **machine à délivrer des stories**. Cette distinction est importante. L’orchestration doit être opinionnée, parce que la valeur du système réside précisément dans le fait d’imposer une discipline là où le prompting ad hoc laisserait fuir la qualité.

_Source : `docs/_bmad-output/planning-artifacts/product-brief-mypi-config.md` ; `/home/cvc/.nvm/versions/node/v24.14.1/lib/node_modules/@mariozechner/pi-coding-agent/README.md` ; `/home/cvc/.nvm/versions/node/v24.14.1/lib/node_modules/@mariozechner/pi-coding-agent/docs/skills.md` ; `/home/cvc/.nvm/versions/node/v24.14.1/lib/node_modules/@mariozechner/pi-coding-agent/docs/sdk.md`._

### Cycle TDD agentique BMAD/Pi recommandé

Le workflow de bout en bout recommandé pour une story est le suivant.

| Étape | Objectif | Tier de modèle recommandé | Entrées | Sorties | Gate |
|---|---|---|---|---|---|
| 1. Gate de readiness de la story | Confirmer que la story est implémentable | Modèle de raisonnement à haute confiance | Story BMAD, brief, architecture, UX si pertinent | Execution brief, liste d’ambiguïtés, décomposition d’acceptation | Aucun bloqueur non résolu ne subsiste |
| 2. Intention de test et cartographie des cibles | Convertir les critères d’acceptation en cibles de validation exactes | Modèle de raisonnement à haute confiance | Execution brief, scan du codebase, tests existants | Matrice acceptation-vers-tests, commandes exactes, notes de périmètre | Chaque critère d’acceptation a un chemin de vérification prévu |
| 3. Rédaction des tests en rouge | Créer/mettre à jour les tests qui échouent pour la bonne raison | Modèle builder | Carte des cibles, fichiers pertinents | Tests nouveaux ou mis à jour en échec, sortie de commande échouée | Au moins un test désigné est rouge pour la bonne raison |
| 4. Boucle d’implémentation vers le vert | Implémenter juste ce qu’il faut pour satisfaire les tests ciblés | Modèle builder | Tests en échec, commandes exactes, périmètre de story | Patch de code, résultat ciblé au vert, notes de patch | Les tests ciblés passent et aucun smoke breakage immédiat n’apparaît |
| 5. Refactor & hardening | Améliorer le design et élargir la surface de vérification | Builder + verifier | Patch vert, zones impactées | Code plus propre, résultats de suite élargie, sorties lint/format | Lint/format passent et les tests élargis impactés passent |
| 6. Vérification runtime | Prouver le vrai comportement dans le système en cours d’exécution | Builder/runtime verifier avec idées planner/generator/healer | Flux de story, app lancée, setup d’environnement | Traces Playwright, captures, logs, notes runtime | La preuve runtime confirme le comportement d’acceptation |
| 7. Dual review | Revoir la correction, la maintenabilité et le risque caché | Deux modèles de revue diversifiés à haute confiance | Diff, story, preuve runtime, résultats de tests | Findings de revue A et B | Aucun finding bloquant ne subsiste |
| 8. Coordinateur de réparation | Corriger les findings et revalider | Builder + rerevue sélective | Findings de revue, patch, commandes | Patch final et findings levés | Max 2–3 boucles, sinon escalade |
| 9. Décision humaine | Merge, checkpoint ou escalade | Humain | Tous les artefacts | Décision finale et closeout | Une clôture explicite existe |

Ce cycle doit être imposé par quatre règles dures :

1. **Règle de contexte frais :** chaque étape ne reçoit que les entrées dont elle a réellement besoin.
2. **Règle de preuve rouge :** l’implémentation ne démarre pas tant qu’une preuve d’échec n’existe pas.
3. **Règle de preuve :** chaque gate est franchie par des artefacts, et non par de simples affirmations d’agent.
4. **Règle d’escalade :** après des retries bornés, on arrête et on demande à l’humain.

C’est le cœur du cycle TDD que je recommande pour votre environnement.

_Source : https://simonwillison.net/guides/agentic-engineering-patterns/red-green-tdd/ ; https://tweag.github.io/agentic-coding-handbook/WORKFLOW_TDD/ ; https://playwright.dev/docs/test-agents ; https://arxiv.org/html/2510.23761v1 ; https://code.claude.com/docs/en/best-practices ; `docs/_bmad-output/planning-artifacts/product-brief-mypi-config.md`._

### Routage initial recommandé des modèles pour votre environnement

Compte tenu de l’environnement que vous avez précisé, l’hypothèse de routage initiale la plus sûre est :

| Rôle | Primaire | Secondaire | Notes |
|---|---|---|---|
| Analyste de story / auteur d’execution brief | gpt-5.4 ou opus-4.6 | sonnet-4.6 | À utiliser pour la décomposition du scope, la cartographie de l’acceptation et le cadrage des risques |
| Implémenteur principal / boucle de réparation | sonnet-4.6 ou glm-5.1 | gpt-5.4 | À calibrer selon les résultats repo ; garder un scope fortement borné |
| Reviewer A | opus-4.6 | gpt-5.4 | Focalisé sur la correction et les bugs subtils |
| Reviewer B | gpt-5.4 | opus-4.6 | Focalisé sur l’adéquation à l’acceptation, la maintenabilité et les edge cases |
| Auteur runtime/E2E | sonnet-4.6 ou glm-5.1 | gpt-5.4 | Le modèle plus fort valide ou revoit les checks navigateur générés |
| Agent de support local | Ollama 32k | — | À restreindre à des tâches bornées et low-trust : résumés, triage grep, regroupement de logs, transformations mécaniques |

Ce routage doit être traité comme un **point de calibration initial**, pas comme un dogme. Le workflow doit collecter des métriques au niveau des phases afin que le routage puisse être ajusté empiriquement.

_Source : contraintes d’environnement fournies par l’utilisateur ; `/home/cvc/.nvm/versions/node/v24.14.1/lib/node_modules/@mariozechner/pi-coding-agent/docs/models.md` ; `docs/_bmad-output/planning-artifacts/product-brief-mypi-config.md`._

### Avantage technique compétitif

Votre avantage technique ne vient pas du fait que BMAD ou Pi soient les standards du marché. Il vient du fait qu’ensemble ils créent une combinaison qui manque souvent aux setups grand public :

- **des entrées de qualité story** grâce à BMAD,
- **une forte malléabilité de workflow** grâce à Pi,
- **une indépendance vis-à-vis des modèles** grâce au support multi-provider,
- **des handoffs pilotés par artefacts** alignés avec la discipline TDD.

La plupart des workflows publics de coding agentique partent de prompts puis tentent de reconstruire de la structure. Votre workflow peut partir d’artefacts structurés et utiliser Pi pour imposer le process. C’est une différenciation réelle.

_Source : `docs/_bmad-output/planning-artifacts/product-brief-mypi-config.md` ; `/home/cvc/.nvm/versions/node/v24.14.1/lib/node_modules/@mariozechner/pi-coding-agent/README.md` ; `/home/cvc/.nvm/versions/node/v24.14.1/lib/node_modules/@mariozechner/pi-coding-agent/docs/skills.md`._

## 9. Feuille de route d’implémentation et évaluation des risques

### Cadre d’implémentation technique

Un déploiement par phases est fortement recommandé.

**Phase 1 — pilote manuel (immédiat).**
Utiliser des invocations explicites de skills Pi et des transitions de phases manuelles sur 3 à 5 stories. L’objectif n’est pas encore l’automatisation ; c’est de valider la forme des artefacts, les commandes, le routage des modèles et les gates.

**Phase 2 — pack de skills semi-automatisé.**
Créer des skills Pi ou des prompt templates pour chaque phase majeure :

- readiness de la story
- carte d’intention de test
- rédaction des tests rouges
- implémentation vers le vert
- vérification runtime
- dual review
- coordinateur de réparation

À ce stade, l’humain approuve encore les transitions, mais le process devient répétable.

**Phase 3 — extension Pi ou orchestrateur SDK.**
Une fois la boucle manuelle stabilisée, construire un orchestrateur mince qui :

- crée les artefacts de phase,
- choisit les modèles par rôle,
- lance des sessions fraîches ou des branches,
- enregistre les sorties,
- impose les gates,
- s’arrête sur conditions d’escalade.

**Phase 4 — intégration CI.**
Introduire GitHub Actions ou équivalent pour rejouer ou vérifier certaines gates clés sur les événements de branche/PR, publier les artefacts et éventuellement conditionner le merge.

_Source : `/home/cvc/.nvm/versions/node/v24.14.1/lib/node_modules/@mariozechner/pi-coding-agent/docs/skills.md` ; `/home/cvc/.nvm/versions/node/v24.14.1/lib/node_modules/@mariozechner/pi-coding-agent/docs/sdk.md` ; https://docs.github.com/en/actions ; https://docs.anthropic.com/en/docs/claude-code/github-actions ._

### Stratégie de migration technologique

Il ne faut pas tenter un remplacement « big bang » de vos habitudes actuelles de coding. À la place :

1. garder l’ancien modèle mental de delivery de story,
2. remplacer une phase à la fois par une discipline explicite de TDD agentique,
3. mesurer les résultats,
4. n’automatiser qu’ensuite.

C’est particulièrement important pour le routage des modèles. Un routage élégant sur le papier mais non benchmarké contre vos dépôts dérivera rapidement.

_Source : https://code.claude.com/docs/en/best-practices ; https://aider.chat/ ; `docs/_bmad-output/planning-artifacts/product-brief-mypi-config.md`._

### Gestion des risques techniques

| Risque | Symptôme typique | Mitigation |
|---|---|---|
| Théâtre procédural du TDD | L’agent prétend faire du TDD sans preuve réelle d’échec | Exiger un artefact de preuve rouge avant implémentation |
| Théâtre des tests | Les tests passent mais le comportement reste faux | Exiger vérification runtime et cartographie acceptation-vers-tests |
| Dérive de contexte | Confusion tardive et hypothèses cachées | Utiliser handoffs à contexte frais et prompts de phase courts |
| Thrash de patchs | Multiples boucles de réparation non convergentes | Plafonner à 2–3 retries puis escalader |
| Dérive des coûts | Utilisation de modèles premium partout | Réserver les top-tier à la planification, la revue et le hard debugging |
| Mauvais usage des modèles locaux faibles | Patches de faible qualité ou régressions silencieuses | Garder Ollama sur des tâches de support bornées jusqu’au benchmark |
| Sur-portée des outils | Commandes dangereuses, fuite de secrets, portée d’intégration excessive | Utiliser outils scopés, MCP minimal et contrôles par hooks/policies |
| Monoculture de revue | Deux revues ratent la même faute | Utiliser des modèles ou des angles de revue diversifiés |

_Source : https://arxiv.org/html/2510.23761v1 ; https://docs.anthropic.com/en/docs/claude-code/hooks ; https://docs.anthropic.com/en/docs/claude-code/mcp ; https://docs.github.com/en/actions ; `docs/research/tdd-initiative`._

## 10. Perspectives techniques futures et opportunités d’innovation

### Tendances technologiques émergentes

La prochaine vague de TDD agentique inclura probablement :

- **des tests de régression juste-à-temps** générés pour des changements spécifiques,
- **des boucles de réparation conscientes des traces** utilisant directement les preuves runtime,
- **un routage de modèles informé par benchmark** plutôt que piloté par intuition,
- **des filtres de qualité de génération de tests plus forts** pour réduire les tests fragiles ou peu utiles,
- **des packages de workflow** qui encodent ces patterns comme add-ons réutilisables pour les harnesses.

L’article JiTTesting de Meta est particulièrement important ici, car il suggère que des suites statiques rédigées à la main ne pourront peut-être pas suivre indéfiniment la vitesse du développement agentique. L’avenir probable est hybride : tests d’acceptation rédigés, tests de régression générés et preuve runtime travailleront ensemble.

_Source : https://engineering.fb.com/2026/02/11/developer-tools/the-death-of-traditional-testing-agentic-development-jit-testing-revival/ ; https://playwright.dev/docs/test-agents ; https://www.swebench.com/ ; https://arxiv.org/html/2510.23761v1 ._

### Opportunités d’innovation pour ce projet

Votre projet ouvre plusieurs pistes d’innovation prometteuses :

- un **pack de skills Pi** pour l’exécution TDD pilotée par story,
- une **extension Pi / un orchestrateur SDK** qui transforme automatiquement les stories BMAD en runs de phases,
- un **dataset benchmark de stories** construit à partir de vos propres stories, artefacts et résultats,
- une **scorecard de routage de modèles** par dépôt et par phase,
- un **standard d’artefacts de preuve runtime** qui devient partie intégrante de la clôture des stories.

Parce que Pi est personnalisable et que BMAD encode déjà une structure de planification, votre setup est particulièrement bien placé pour transformer une pratique privée en package de workflow réutilisable par la suite.

_Source : `/home/cvc/.nvm/versions/node/v24.14.1/lib/node_modules/@mariozechner/pi-coding-agent/README.md` ; `/home/cvc/.nvm/versions/node/v24.14.1/lib/node_modules/@mariozechner/pi-coding-agent/docs/skills.md` ; `/home/cvc/.nvm/versions/node/v24.14.1/lib/node_modules/@mariozechner/pi-coding-agent/docs/sdk.md` ; `docs/_bmad-output/planning-artifacts/product-brief-mypi-config.md`._

## 11. Méthodologie de recherche et vérification des sources

### Sources techniques principales

**Documentation vendors et plateformes**

- https://code.claude.com/docs/en/best-practices
- https://docs.anthropic.com/en/docs/claude-code/sub-agents
- https://docs.anthropic.com/en/docs/claude-code/hooks
- https://docs.anthropic.com/en/docs/claude-code/mcp
- https://docs.anthropic.com/en/docs/claude-code/github-actions
- https://aider.chat/
- https://openhands.dev/
- https://playwright.dev/docs/intro
- https://playwright.dev/docs/test-agents
- https://playwright.dev/docs/ci
- https://vitest.dev/guide/
- https://docs.pytest.org/en/stable/contents.html
- https://docs.github.com/en/actions
- https://modelcontextprotocol.io/introduction

**Sources de recherche et benchmarks**

- https://arxiv.org/html/2510.23761v1
- https://www.swebench.com/
- https://www.swebench.com/SWE-bench/guides/docker_setup/
- https://engineering.fb.com/2026/02/11/developer-tools/the-death-of-traditional-testing-agentic-development-jit-testing-revival/

**Guides de workflow et commentaires techniques**

- https://simonwillison.net/guides/agentic-engineering-patterns/red-green-tdd/
- https://tweag.github.io/agentic-coding-handbook/WORKFLOW_TDD/
- https://www.builder.io/blog/test-driven-development-ai

**Sources locales Pi et projet utilisées pour l’adaptation**

- `/home/cvc/.nvm/versions/node/v24.14.1/lib/node_modules/@mariozechner/pi-coding-agent/README.md`
- `/home/cvc/.nvm/versions/node/v24.14.1/lib/node_modules/@mariozechner/pi-coding-agent/docs/skills.md`
- `/home/cvc/.nvm/versions/node/v24.14.1/lib/node_modules/@mariozechner/pi-coding-agent/docs/sdk.md`
- `/home/cvc/.nvm/versions/node/v24.14.1/lib/node_modules/@mariozechner/pi-coding-agent/docs/models.md`
- `docs/research/tdd-initiative`
- `docs/_bmad-output/planning-artifacts/product-brief-mypi-config.md`

### Requêtes de recherche web utilisées

Jeu représentatif de requêtes utilisées pendant la découverte et la validation des sources :

- `agentic TDD software engineering`
- `SWE-bench Verified agentic TDD`
- `agentic coding testing frameworks tools`
- `Claude Code best practices tests lint`
- `OpenHands agent software engineering tests`
- `aider test driven development ai coding`
- `Playwright coding agents runtime verification`
- plus récupération directe ciblée de la documentation primaire après découverte des sources

### Niveaux de confiance technique

**Forte confiance :**

- les workflows verification-first surperforment les workflows prompt-first vagues
- les handoffs à contexte frais sont importants pour la fiabilité et le contrôle des coûts
- la décomposition des rôles améliore l’observabilité et le contrôle
- la vérification runtime doit faire partie du cœur du workflow, pas être ajoutée à la fin
- BMAD/Pi peuvent implémenter ces patterns parce que Pi est intentionnellement extensible et que BMAD fournit déjà la structure artifact-centric

**Confiance moyenne :**

- le routage optimal exact entre glm-5.1, sonnet-4.6, gpt-5.4 et opus-4.6 variera selon le dépôt et la phase
- les tests JiT générés deviendront probablement plus centraux, mais leur forme mature exacte reste encore émergente
- les modèles Ollama locaux pourraient devenir plus utiles avec le temps, mais la confiance actuelle doit rester bornée sans mesures propres à votre environnement

### Limites techniques

Le domaine reste jeune. La documentation vendor est utile mais non neutre. L’évidence académique progresse, mais n’est pas encore assez large pour trancher quantitativement chaque choix de design. Certains écosystèmes vendor étaient moins accessibles à une récupération directe ou à du scraping léger de la documentation publique ; ce rapport s’est donc appuyé davantage sur de la documentation primaire accessible, des sites de benchmark et des sources décrivant explicitement les workflows. Cela n’invalide pas les résultats, mais cela signifie que certaines affirmations quantitatives du discours plus large sont plus difficiles à vérifier que les patterns architecturaux eux-mêmes.

## 12. Annexes techniques et documents de référence

### Annexe A : ensemble d’artefacts recommandés pour une story

**Chemin suggéré :** `docs/_bmad-output/implementation-artifacts/stories/<story-id>/`

| Artefact | Finalité | Producteur | Consommateur |
|---|---|---|---|
| `story-execution-brief.md` | Distiller la story, les risques, les frontières de scope et l’objectif exact | Étape de readiness de la story | Toutes les étapes suivantes |
| `acceptance-to-test-matrix.md` | Mapper chaque critère d’acceptation vers unit/intégration/runtime verification | Étape d’intention de test | Rouge, vert, runtime, revue |
| `red-proof.md` ou `failing-tests.log` | Prouver que les tests désignés échouent avant implémentation | Étape rouge | Vert, revue, humain |
| `patch-summary.md` | Expliquer le delta d’implémentation et les zones impactées | Étape vert / refactor | Vérification runtime, revue |
| `validation-summary.md` | Capturer les tests ciblés, la suite impactée, lint, deltas de couverture si pertinent | Étape refactor | Revue, humain |
| `runtime-proof/` | Traces Playwright, captures, vidéos, logs | Étape de vérification runtime | Revue, humain |
| `review-a.md` | Findings du reviewer A | Étape de revue | Coordinateur de réparation, humain |
| `review-b.md` | Findings du reviewer B | Étape de revue | Coordinateur de réparation, humain |
| `story-closeout.md` | Décision finale, points non résolus, suites à donner, enseignements | Clôture humaine | Travaux futurs et rétrospectives |

### Annexe B : décisions architecturales recommandées

| Décision | Recommandation | Rationale |
|---|---|---|
| Entrée canonique | Fichier de story BMAD | Meilleure source pour le scope et l’intention d’acceptation |
| Mémoire du workflow | Artefacts + git + checkpoints de session | Plus auditable qu’une mémoire conversationnelle cachée |
| Orchestrateur | Skills Pi d’abord, SDK/extension Pi ensuite | Adoption à faible friction, trajectoire claire vers l’automatisation |
| Vérification de boucle interne | Tests unit/intégration ciblés uniquement | Plus rapide et plus précis que tout lancer à chaque tour |
| Vérification runtime | Obligatoire pour le comportement visible par l’utilisateur | Évite les cas « tous les tests unitaires sont verts mais l’app reste cassée » |
| Revue finale | Deux passes de revue diversifiées | Réduit les angles morts corrélés |
| Politique de retry | Max 2–3 boucles de réparation | Évite le thrash et le coût caché accumulé |
| Usage des modèles locaux | Tâches de support bornées uniquement au début | Aligne l’usage avec les contraintes actuelles de confiance et de contexte |

### Annexe C : métriques de succès et KPI suggérés

| Métrique | Pourquoi c’est important |
|---|---|
| Stories avec preuve rouge explicite | Détecte un faux TDD ou un TDD manquant |
| Médiane de boucles jusqu’au vert | Mesure l’efficacité d’implémentation |
| Taux de succès au premier passage de la vérification runtime | Mesure la qualité end-to-end |
| Findings bloquants après revue | Mesure le taux de défauts cachés |
| Taux d’escalade humaine | Mesure la convergence du workflow |
| Coût par story et par phase | Permet d’optimiser le routage des modèles |
| Taux de régression post-merge | Mesure finale de qualité |

### Annexe D : prochaines étapes immédiates

1. Définir des templates pour l’ensemble d’artefacts de l’Annexe A.
2. Piloter le workflow en 9 étapes sur un petit nombre de vraies stories avec transitions manuelles.
3. Suivre les métriques de phase et comparer les performances des modèles par rôle.
4. Packager les prompts de phase stables sous forme de skills Pi.
5. Ne construire qu’ensuite un orchestrateur via SDK ou extension.

## 13. Conclusion de la recherche technique

### Synthèse des constats techniques clés

La recherche soutient fortement l’idée que le TDD reste non seulement pertinent, mais de plus en plus précieux dans le delivery logiciel agentique — à condition d’être implémenté comme un **workflow centré sur la vérification** plutôt que comme une instruction vague. Les patterns dominants sont désormais visibles à travers des sources indépendantes : tests explicitement en échec, décomposition par étapes, handoffs à contexte frais, validation runtime, boucles de réparation bornées et pistes d’audit appuyées sur des artefacts repo-native.

### Évaluation de l’impact technique stratégique

Pour votre projet, cela signifie que le workflow cible est désormais beaucoup plus clair. Le bon design n’est ni « laisser Pi imiter Claude Code », ni « forcer sans adaptation les rituels TDD humains classiques sur des agents ». Il s’agit de construire une **boucle de delivery multi-modèle, pilotée par les stories BMAD et orchestrée par Pi**, qui emprunte les meilleurs patterns de l’industrie et les rend imposables via artefacts, outils et gates.

### Recommandations techniques de prochaines étapes

La prochaine action immédiate ne doit pas être de coder tout l’orchestrateur d’un coup. La prochaine action immédiate doit être de figer le workflow recommandé et le schéma d’artefacts, puis de les tester manuellement sur de vraies stories. Une fois cette forme stabilisée, le travail d’automatisation dans Pi deviendra beaucoup plus simple — et beaucoup plus susceptible d’être correct.

---

**Date de finalisation de la recherche technique :** 2026-04-12
**Période de recherche :** analyse technique complète sur l’état actuel du sujet
**Vérification des sources :** toutes les affirmations clés sont ancrées dans des sources actuelles accessibles et dans la documentation locale d’adaptation
**Niveau global de confiance technique :** élevé pour l’architecture et la direction du workflow ; moyen pour le routage exact des modèles tant qu’il n’est pas benchmarké localement

_Ce document a vocation à servir de référence de travail pour concevoir le cycle TDD BMAD/Pi et le workflow final de story pour `mypi-config`._
