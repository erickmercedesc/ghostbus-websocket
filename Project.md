# Project.md

Centro de la verdad de la arquitectura de GhostBusSocket. Describir aquí el sistema que existe. Actualizar este archivo en el mismo cambio que altere módulos, flujo de datos o contratos públicos.

## Estado

Servicio Python: FastAPI y python-socketio en un ASGI. Los clientes Socket.IO se identifican con `X-License-Key`. `POST /send` entrega el mismo texto a todas las conexiones de esa licencia.

## Qué hace

Intermediario en un proceso. El cliente abre una sesión Socket.IO con su licencia. Otro llamador hace `POST /send` con `{ "to", "message" }`. El servidor emite `message` a la sala de esa licencia.

## Módulos

- `ghostbus.identity` — lee `X-License-Key` del header y, si falta, del query string. Una sola regla para Socket.IO y para el environ de conexión.
- `ghostbus.connection` — acepta la conexión solo si hay licencia y la mete en una sala con ese nombre.
- `ghostbus.bus` — contrato `deliver(license_key, message) -> destinatarios`.
- `ghostbus.socketio_bus` — implementa el bus emitiendo el evento `message` a la sala de la licencia.
- `ghostbus.app` — HTTP `POST /send`.
- `ghostbus.server` — monta Socket.IO sobre FastAPI. ASGI de entrada: `ghostbus.server:app`.
- `ghostbus.runtime` — arranca Uvicorn sobre ese ASGI.
- `websocket_engine` — punto de entrada `python -m websocket_engine`.

## Flujo de datos

1. El cliente Socket.IO conecta a `/` con `X-License-Key` en header o en query.
2. Si no hay licencia, la conexión se rechaza.
3. Si hay licencia, el `sid` entra en la sala de ese valor. Varias conexiones de la misma licencia conviven.
4. `POST /send` con `{ "to": "<licencia>", "message": "<texto>" }` cuenta los participantes de esa sala.
5. Si no hay ninguno, responde 404 `license not connected`.
6. Si hay, emite el evento Socket.IO `message` con el texto a esa sala y responde `{ "delivered": N }`.

El registro de salas vive en el proceso. Al reiniciar, las conexiones se pierden.

## Contratos públicos

Identidad: nombre `X-License-Key`. Header primero, query después.

Socket.IO:

- URL: `http://<host>/` (Engine.IO/Socket.IO, no un WebSocket crudo).
- Header `X-License-Key` o `?X-License-Key=`.
- Evento recibido: `message`, payload string.

HTTP:

```http
POST /send
Content-Type: application/json

{ "to": "abc123", "message": "Hello World" }
```

- 200 `{ "delivered": N }`
- 404 `{ "detail": "license not connected" }`
- 422 si faltan `to` o `message`

Arranque: `python -m websocket_engine` (Uvicorn en `0.0.0.0:8000`). Puerto: `--port`.
