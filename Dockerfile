FROM python:3.10.3

WORKDIR /usr/src/app

RUN groupadd -r appgroup && useradd -r -g appgroup appuser

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chown -R appuser:appgroup /usr/src/app

USER appuser

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
