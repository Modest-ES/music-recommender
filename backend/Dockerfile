# Use Python 3.9
FROM python:3.9-slim

WORKDIR /app

# Copy requirements first (caching optimization)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire backend folder
COPY . .

# Expose port 5000 (Flask default)
EXPOSE 5000

# Run with Gunicorn (if gunicorn.conf.py exists)
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]