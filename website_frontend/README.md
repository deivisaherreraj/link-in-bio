# Website de links de DHerreraJDev

[![Python](https://img.shields.io/badge/Python-3.12+-yellow?style=for-the-badge&logo=python&logoColor=white&labelColor=101010)](https://python.org)
[![FastAPI](https://img.shields.io/badge/Reflex-0.3.10+-5646ED?style=for-the-badge&logo=reflex&logoColor=white&labelColor=101010)](https://fastapi.tiangolo.com)

## Proyecto desarrollado con [Python](https://www.python.org/) y [Reflex](https://reflex.dev/) que representa un sitio web personal estilo "[link in bio](https://link-in-bio-production.up.railway.app/)"

![https://link-in-bio-production.up.railway.app/](../assets/web.png)

## Calidad del proyecto

Desde `website_frontend`, instala las dependencias bloqueadas y ejecuta la misma
validación utilizada por CI:

```bash
uv sync --locked --dev
uv run ruff format --check .
uv run ruff check .
uv run mypy
uv run --locked pytest
```
