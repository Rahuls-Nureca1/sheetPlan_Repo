# Stage 1 - Install build dependencies
FROM python:3.8-slim-buster AS builder

WORKDIR /app

RUN python -m venv .venv && .venv/bin/pip install --no-cache-dir -U pip setuptools

# COPY .env ./
COPY . ./
RUN .venv/bin/pip install --no-cache-dir -r requirements.txt
# RUN .venv/bin/pip install --no-cache-dir -r requirements.txt
# RUN chmod 0600 client-key.pem
# RUN chmod 0600 client-cert.pem
# RUN chmod 0600 server-ca.pem


# Stage 2 - Copy only necessary files to the runner stage
FROM python:3.8-slim-buster
WORKDIR /app


COPY --from=builder /app /app

# COPY --from=builder /app /app
# COPY app.py routes.py ./
EXPOSE 5000

# Copy the rest of your app's source code from your host to your image filesystem.
# COPY . ./


ENV PATH="/app/.venv/bin:$PATH"

CMD ["python", "wsgi.py"]

