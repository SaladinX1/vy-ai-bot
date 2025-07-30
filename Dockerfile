FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "main.py", "--autopilot"]

# docker build -t vy-ai-bot .
# docker run -p 8501:8501 vy-ai-bot
