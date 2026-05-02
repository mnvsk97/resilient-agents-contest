FROM python:3.12-slim
WORKDIR /app
COPY . .
RUN chmod +x ./contest/run.sh ./contest/healthcheck.sh
CMD ["./contest/run.sh"]
