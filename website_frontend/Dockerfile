# Dockerfile para desplegar tu app Reflex (frontend + backend) en un solo contenedor
# Compatible con Railway, Render, DigitalOcean Apps, etc.

# Imagen base completa (más simple, incluye unzip y herramientas del sistema)
FROM python:3.12

COPY --from=ghcr.io/astral-sh/uv:0.10.12 /uv /uvx /bin/

# Configuración básica de Python
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_PYTHON_DOWNLOADS=0 \
    PATH="/app/.venv/bin:$PATH"

# Instalamos Caddy como reverse proxy para unificar frontend + backend en un solo puerto
RUN apt-get update -y && apt-get install -y --no-install-recommends \
    caddy \
    && rm -rf /var/lib/apt/lists/*

# Establece el directorio de trabajo dentro del contenedor como /app
WORKDIR /app

# Puerto de salida del contenedor.
# Puerto por defecto (se sobreescribe con PORT de Railway)
ARG PORT=8000
ARG API_URL
ARG DATABASE_URL

# PORT y DATABASE_URL se pueden sobreescribir con variables de entorno de Railway
ENV PORT=${PORT} \
    API_URL=${API_URL:-http://localhost:${PORT}} \
    DATABASE_URL=${DATABASE_URL:-""}

# Caddyfile inline: sirve frontend desde /srv y hace proxy al backend de Reflex (8000)
RUN cat > Caddyfile <<EOF
:{\$PORT}

encode gzip

@backend_routes path /_event/* /ping /_upload /_upload/*
handle @backend_routes {
    reverse_proxy localhost:8000
}

root * /srv
route {
    try_files {path} {path}/ /404.html
    file_server
}
EOF

# Copy canonical project metadata first to preserve the dependency layer cache.
COPY pyproject.toml uv.lock ./

# Install the locked production dependencies without the development group.
RUN uv sync --locked --no-dev --no-install-project

# Copiamos el resto del código de la app
COPY . .

# Inicializamos Reflex (genera estructura interna .web, etc.)
RUN reflex init

# Exportamos SOLO el frontend sin zip
RUN reflex export --frontend-only --no-zip

# Copiamos los estáticos generados a /srv
# En Reflex actual, los estáticos quedan en .web/build/client
RUN mkdir -p /srv && cp -r .web/build/client/* /srv/ && rm -rf .web

# Hasta que Reflex maneje bien SIGTERM
STOPSIGNAL SIGKILL

# Exponemos el puerto (Railway inyecta su propio PORT en runtime)
EXPOSE ${PORT}

# Arranque:
# 1) Caddy sirve el frontend y hace proxy al backend
# 2) Reflex levanta solo el backend en modo prod
CMD caddy start && reflex run --env prod --backend-only --loglevel debug
