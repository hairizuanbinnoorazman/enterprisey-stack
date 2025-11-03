FROM python:3.13-slim
RUN pip install mcpo uv
WORKDIR /app
COPY config.json config.json
RUN apt update && apt install -y tcpdump
EXPOSE 8080
CMD ["uvx", "mcpo", "--host", "0.0.0.0", "--port", "8080", "--config", "/app/config.json", "--log-level", "debug"]