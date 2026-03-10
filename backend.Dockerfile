FROM python:3.12-slim

WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

ENV PYTHONUNBUFFERED=1

EXPOSE 8000

# Run FastAPI using uvicorn (ensure module path matches project)
CMD ["uvicorn", "app.endpoints.api:app", "--host", "0.0.0.0", "--port", "8000"]