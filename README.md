# Nebula Web – API del Backend (FastAPI)

Este documento lista los endpoints disponibles del backend y cómo usarlos desde el frontend o por consola. El backend corre con FastAPI en `pyserver/main.py`.

- Base URL: `http://localhost:4000`
- Puerto: variable de entorno `PORT` (por defecto `4000`)
- CORS: permitido para `http://localhost:5173` y `http://127.0.0.1:5173`

## Cómo ejecutar el backend

Desde la carpeta `web/pyserver`:

```
python -m uvicorn main:app --reload --port 4000
```

## Endpoints

### GET `/health`
- Propósito: chequeo de salud básico.
- Respuesta: `{ "ok": true }`.

Ejemplo:
```
curl http://localhost:4000/health
```

---

### POST `/api/register`
- Propósito: registrar un jugador tras verificar su cuenta de VALORANT.
- Body JSON (campos obligatorios y opcionales):
  - Obligatorios: `riotId` (string), `tagline` (string), `email` (email), `termsAccepted` (bool), `ageConfirmed` (bool)
  - Opcionales: `puuid` (string), `discord` (string), `region` (string, default `LATAM`), `timezone` (string), `social` (string)
- Respuesta (200): `{ "id": number, "status": "PENDING", "message": string }`
- Posibles errores: `400` validación, `409` duplicado, `504` timeout verificación externa.

Ejemplo:
```
curl -X POST http://localhost:4000/api/register \
  -H "Content-Type: application/json" \
  -d '{
    "riotId": "mishilover",
    "tagline": "usc",
    "email": "test@example.com",
    "termsAccepted": true,
    "ageConfirmed": true,
    "region": "LATAM"
  }'
```

---

### GET `/api/registrant`
- Propósito: obtener datos del registrante.
- Query params (usa uno de los dos modos):
  - `id` (number)  
  - `riotId` (string) + `tagline` (string)
- Respuesta: objeto del registrante (incluye `status`, `email`, `region`, etc.).
- Errores: `400` parámetros faltantes, `404` no encontrado.

Ejemplos:
```
curl "http://localhost:4000/api/registrant?id=1"
curl "http://localhost:4000/api/registrant?riotId=mishilover&tagline=usc"
```

---

### GET `/api/registrant/valo`
- Propósito: obtener datos completos del registrante (incluye campos enriquecidos de VALORANT) usando query.
- Query params: `id` o `riotId` + `tagline` (mismo esquema de `/api/registrant`).
- Respuesta: `RegistrantOut` (campos de cuenta, MMR y resumen guardados).
- Errores: `400`, `404`.

Ejemplo:
```
curl "http://localhost:4000/api/registrant/valo?riotId=mishilover&tagline=usc"
```

---

### GET `/api/registrant/valo/{id}`
- Propósito: resumen VALORANT usando `id` del registrante.
- Respuesta:
```
{
  id, status, riotId, tagline,
  account: { puuid, region, account_level },
  mmr: { current: { tier, elo, ranking_in_tier, mmr_change_last_game }, highest: { tier, season } },
  summary: { wins, losses, games, win_pct, adr, kd, hs_pct, acs, kills_per_round, kad, rating_* }
}
```

### GET `/api/registrant/valo/{riotId}/{tagline}`
- Propósito: resumen VALORANT usando `riotId` y `tagline` directamente en la ruta.

### GET `/api/registrant/valo/by-rtag/{rtag}`
- Propósito: resumen VALORANT usando `rtag` compuesto `name#tag`.
- Errores: `400` formato inválido, `404` no encontrado.

## Integración desde el frontend

Ejemplo `fetch` desde React:
```
await fetch("http://localhost:4000/api/register", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    riotId: "mishilover",
    tagline: "usc",
    email: "test@example.com",
    termsAccepted: true,
    ageConfirmed: true
  })
});
```

## Notas
- No requiere autenticación.
- CORS ya permite `http://localhost:5173`.
- `SEAT_LIMIT` se utiliza internamente para lógica de cupos (no expone endpoint).
