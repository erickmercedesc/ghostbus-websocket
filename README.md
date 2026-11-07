# GhostBusSocket

Servicio Python que recibe clientes por Socket.IO y les envía mensajes por HTTP. Cada cliente se identifica con `X-License-Key` (header o query string). `POST /send` entrega `{ "message", "data" }` a todas las conexiones de esa licencia.

Requiere Python 3.11 o superior.

## Instalar

En la raíz del repositorio:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e .
```

Con tests:

```powershell
pip install -e ".[dev]"
```

En Linux o macOS:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

## Correr

Con el entorno virtual activado y el paquete instalado:

```powershell
python -m websocket_engine
```

El servicio queda en `http://127.0.0.1:8000`. Swagger del HTTP: `http://127.0.0.1:8000/docs`. Otro puerto:

```powershell
python -m websocket_engine --port 9000
```

## Docker

```powershell
docker compose up --build
```

El servicio queda en `http://127.0.0.1:8000`. Sin Compose:

```powershell
docker build -t ghostbussocket .
docker run --rm -p 8000:8000 ghostbussocket
```

## Cliente Socket.IO

```python
import socketio

sio = socketio.Client()

@sio.on("message")
def on_message(data):
    print(data)

sio.connect("http://127.0.0.1:8000", headers={"X-License-Key": "abc123"})
sio.wait()
```

Sin header, la misma clave en el query string:

```python
sio.connect("http://127.0.0.1:8000?X-License-Key=abc123")
```

Instala el cliente con `pip install python-socketio`.

## Enviar un mensaje

```http
POST /send
Content-Type: application/json

{ "to": "abc123", "message": "Hello World", "data": "123456" }
```

`data` es opcional. El cliente Socket.IO recibe:

```json
{ "message": "Hello World", "data": "123456" }
```

Desde PowerShell:

```powershell
Invoke-RestMethod -Uri http://127.0.0.1:8000/send -Method Post -ContentType "application/json" -Body '{"to":"abc123","message":"Hello World","data":"123456"}'
```

- 200 `{ "delivered": N }`
- 404 `{ "detail": "license not connected" }` si esa licencia no tiene conexiones abiertas

## Tests

```powershell
pytest
```
