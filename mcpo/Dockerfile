FROM python:3.13-slim
RUN pip install mcpo uv
WORKDIR /app
COPY config.json config.json
EXPOSE 8080
CMD ["uvx", "mcpo", "--host", "0.0.0.0", "--port", "8080", "--api-key", "abc123", "--config", "/app/config.json"]