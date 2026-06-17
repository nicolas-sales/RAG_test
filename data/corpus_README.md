# Corpus RAG — Test Technique Data Engineer
## IA Factory · La France Mutualiste (fictif)

Ce corpus simule la base documentaire interne d'une mutuelle d'épargne. Il est conçu pour évaluer la capacité d'un candidat à construire un système RAG sur des documents hétérogènes (types, formats, densité d'information).

---

## Contenu du corpus

| Fichier | Format | Type | Nb tokens approx. |
|---------|--------|------|-------------------|
| `faq_interne.md` | Markdown | FAQ structurée | ~1 200 |
| `specs_techniques_api.md` | Markdown + JSON | Documentation technique | ~1 800 |
| `tickets_support.json` | JSON | Données semi-structurées | ~900 |
| `note_produit_per.md` | Markdown + tableaux | Document produit dense | ~1 400 |
| `guide_onboarding_conseiller.md` | Markdown + tableaux | Process interne | ~1 100 |

**Total : ~6 400 tokens**

---

## Questions de test pour évaluation RAG

Le candidat doit s'assurer que son système répond correctement aux questions suivantes (jeu d'évaluation) :

### Questions simples (retrieval direct)
1. "Quel est le taux du LER pour 2025 ?"
2. "Comment contacter le service client LFM ?"
3. "Quel est le plafond de déductibilité PER pour un salarié en 2025 ?"
4. "Quelle est la durée de vie d'un token OAuth de l'API ?"

### Questions intermédiaires (synthèse 1–2 docs)
5. "Quels sont les cas permettant un déblocage anticipé du PER ?"
6. "Comment fonctionne la gestion pilotée du Prévi Retraite ?"
7. "Quelles formations sont obligatoires pour un nouveau conseiller ?"

### Questions difficiles (synthèse multi-docs, raisonnement)
8. "Un adhérent veut racheter son contrat LER 2 ans après ouverture. Quels sont les frais et conditions ?"
9. "En tant que nouveau conseiller, quelles sont les règles à respecter avant de faire souscrire un PER à un client ?"
10. "Un ticket mentionne une erreur sur l'outil de simulation PER. Quel était le problème et est-il résolu ?"

### Questions sans réponse dans le corpus (test hallucination)
11. "Quel est le taux de rendement du MultiVie en 2024 ?"
12. "Comment fonctionne le contrat Capital Décès ?"

Le système doit répondre qu'il ne dispose pas de l'information et ne pas inventer de réponse.

---

## Notes pour le candidat

- Les documents sont intentionnellement hétérogènes pour tester la robustesse du parsing
- Le fichier JSON (tickets) requiert une stratégie de sérialisation spécifique
- Certains documents contiennent des tableaux Markdown — vérifier leur bonne ingestion
- Les questions "sans réponse" permettent d'évaluer la gestion des hallucinations

