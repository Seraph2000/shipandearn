# ── Stage 1: build Tailwind CSS ───────────────────────────────────────────────
FROM node:20-alpine AS css-builder
WORKDIR /app
COPY package*.json tailwind.config.js ./
COPY static/tailwind.src.css ./static/tailwind.src.css
COPY templates/ ./templates/
RUN npm ci --include=dev && npm run css:build

# ── Stage 2: Python app ───────────────────────────────────────────────────────
FROM python:3.11-slim
WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
COPY --from=css-builder /app/static/tailwind.css ./static/tailwind.css

RUN chmod +x entrypoint.sh

EXPOSE 8000
ENTRYPOINT ["./entrypoint.sh"]
