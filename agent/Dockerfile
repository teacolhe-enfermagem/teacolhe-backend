FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y libgomp1

COPY requirements.txt .

RUN pip install torch --index-url https://download.pytorch.org/whl/cpu

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8002
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8002"]