FROM python:3.11-slim-buster

WORKDIR /python-playground

COPY . .

RUN set -ex; \
    pip install --upgrade pip \
    # Install packages
    && pip install --no-cache-dir -r requirements.txt

# Set the entrypoint script as executable
#RUN chmod +x /app/entrypoint.sh
