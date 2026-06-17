# Documentation Technique — API LFM Connect v2.1

## Introduction

L'API LFM Connect permet aux partenaires agréés et aux équipes internes d'accéder aux données contractuelles et de déclencher des opérations sur les comptes adhérents. L'API respecte les normes REST et utilise JSON comme format d'échange.

Base URL : `https://api.lfm.fr/v2`

---

## Authentification

L'API utilise OAuth 2.0 avec le flux Client Credentials pour les intégrations serveur-à-serveur.

### Obtenir un token

```
POST /auth/token
Content-Type: application/x-www-form-urlencoded

grant_type=client_credentials
&client_id=YOUR_CLIENT_ID
&client_secret=YOUR_CLIENT_SECRET
&scope=contracts:read operations:write
```

**Réponse :**
```json
{
  "access_token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "Bearer",
  "expires_in": 3600,
  "scope": "contracts:read operations:write"
}
```

Les tokens ont une durée de vie de 1 heure. Implémenter un mécanisme de refresh automatique.

---

## Endpoints Contrats

### GET /contracts/{id}

Récupère les détails d'un contrat.

**Paramètres :**
| Paramètre | Type | Requis | Description |
|-----------|------|--------|-------------|
| id | string | Oui | Identifiant unique du contrat (format: LFM-XXXXXXXX) |

**Réponse 200 :**
```json
{
  "contract_id": "LFM-00428371",
  "type": "LER",
  "holder": {
    "id": "ADH-991234",
    "name": "Marie Dupont",
    "birth_date": "1978-03-15"
  },
  "status": "active",
  "opening_date": "2019-06-01",
  "balance": 14250.00,
  "currency": "EUR",
  "rate_current_year": 3.10,
  "next_interest_date": "2025-12-31"
}
```

**Codes d'erreur :**
- `404 NOT_FOUND` : Contrat inexistant ou non accessible
- `403 FORBIDDEN` : Scope insuffisant
- `429 RATE_LIMITED` : Limite de 100 req/min dépassée

### GET /contracts/{id}/transactions

Historique des opérations sur un contrat.

**Query params :** `from` (date ISO), `to` (date ISO), `limit` (défaut 50, max 500), `offset`

---

## Endpoints Opérations

### POST /operations/withdrawal

Déclenche un retrait sur un contrat LER.

**Body :**
```json
{
  "contract_id": "LFM-00428371",
  "amount": 500.00,
  "iban": "FR7630004000031234567890143",
  "reason": "partial_withdrawal",
  "idempotency_key": "uuid-v4-unique"
}
```

**Validations :**
- Montant minimum : 150€
- Solde résiduel minimum après retrait : 50€
- IBAN doit être enregistré sur le contrat (vérifier via `/contracts/{id}/ibans`)
- `idempotency_key` obligatoire pour éviter les doublons

**Réponse 202 (Accepted) :**
```json
{
  "operation_id": "OPE-2025-4829301",
  "status": "pending",
  "estimated_processing": "2025-04-25T00:00:00Z",
  "message": "Opération enregistrée, traitement sous 48h ouvrées"
}
```

---

## Webhooks

LFM Connect supporte les webhooks pour notifier les partenaires des événements contractuels.

### Configuration

Enregistrer votre endpoint via `POST /webhooks` avec :
```json
{
  "url": "https://votre-serveur.com/webhook",
  "events": ["contract.updated", "operation.completed", "operation.failed"],
  "secret": "votre_secret_hmac"
}
```

### Sécurité

Chaque notification inclut un header `X-LFM-Signature` contenant un HMAC-SHA256 du body signé avec votre secret. Toujours valider cette signature avant de traiter l'événement.

---

## Limites et SLA

| Environnement | Rate Limit | SLA Disponibilité |
|--------------|-----------|-------------------|
| Production | 100 req/min | 99.9% |
| Staging | 20 req/min | Best effort |

Les appels dépassant le rate limit retournent `429` avec un header `Retry-After` indiquant le délai en secondes.

---

## Changelog

**v2.1 (Mars 2025)** : Ajout de l'endpoint `/operations/transfer` pour les virements inter-contrats. Dépréciation de `/v1/accounts` (fin de support : 01/09/2025).

**v2.0 (Janvier 2024)** : Migration vers OAuth 2.0. Suppression de l'authentification par clé API.
