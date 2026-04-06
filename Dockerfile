FROM python:3.12-slim

WORKDIR /app

# Install git for auto-sync
RUN apt-get update && apt-get install -y --no-install-recommends git && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml .
RUN pip install --no-cache-dir .

COPY . .

CMD ["python", "-m", "src.main"]
