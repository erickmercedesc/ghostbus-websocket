# GhostBusSocket

Servicio Python que recibe clientes por Socket.IO y les envía mensajes por HTTP. Cada cliente se identifica con `X-License-Key` (header o query string). `POST /send` entrega el texto a todas las conexiones de esa licencia.

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

El servicio queda en `http://127.0.0.1:8000`.

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

{ "to": "abc123", "message": "Hello World" }
```

Desde PowerShell:

```powershell
Invoke-RestMethod -Uri http://127.0.0.1:8000/send -Method Post -ContentType "application/json" -Body '{"to":"abc123","message":"Hello World"}'
```

- 200 `{ "delivered": N }`
- 404 `{ "detail": "license not connected" }` si esa licencia no tiene conexiones abiertas

## Tests

```powershell
pytest
```
