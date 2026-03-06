FROM python:3.11-slim

WORKDIR /app

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app source
COPY app.py .

# Create a writable directory for the database and set permissions
RUN mkdir -p /app/data && chmod 777 /app/data

EXPOSE 5000

# Non-root user for container security best practice
RUN useradd -m appuser
USER appuser

CMD ["python", "app.py"]