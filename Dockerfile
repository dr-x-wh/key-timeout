FROM python:3.12-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

FROM python:3.12-slim
WORKDIR /app
COPY --from=builder /root/.local /root/.local

COPY ./app/ .
COPY ./.env .
COPY ./.flaskenv .
COPY ./gunicorn.py .
COPY ./run.py .

EXPOSE 9009
CMD ["gunicorn", "-c", "gunicorn.py", "run:app"]
