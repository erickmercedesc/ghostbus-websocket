# AGENTS.md

Reglas permanentes de GhostBusSocket. Aplican a todo el trabajo en este repositorio.

## Código

Siempre usar DRY, SOLID y TDD. Ningún cambio de comportamiento se acepta si rompe uno de los tres.

### DRY

- Cada hecho, regla de negocio y decisión de diseño vive en un solo lugar.
- Si el mismo conocimiento aparece dos veces, extraerlo antes de seguir.
- No crear una abstracción por un único uso. Extraer en el segundo uso real.

### SOLID

- **S** — Una unidad tiene una sola razón para cambiar.
- **O** — Extender comportamiento sin modificar lo que ya funciona.
- **L** — Un sustituto debe poder ocupar el lugar de su contrato sin sorpresas.
- **I** — Depender de la interfaz mínima que el llamador usa.
- **D** — Depender de abstracciones. El detalle concreto se inyecta desde fuera.

### TDD

El código de producción nuevo o corregido nace de un test que falla.

1. Escribir un test que exprese el comportamiento y falle.
2. Escribir el mínimo código para que pase.
3. Refactorizar con los tests en verde, aplicando DRY y SOLID.
4. No añadir producción, ni “arreglar de paso”, sin un test que lo exija.

## Arquitectura

`Project.md` es el centro de la verdad de cómo funciona el proyecto.

- Leerlo antes de decidir, explicar o cambiar arquitectura, módulos, flujo de datos o contratos públicos.
- Actualizarlo en el mismo cambio que modifica cualquiera de eso.
- Si el código y `Project.md` no coinciden, reconciliarlos en ese mismo cambio. El documento describe el sistema real, no el sistema deseado.
