# Use a slim Python image matching Django 5.0.7's compatibility (Python 3.12 is fine)
FROM python:3.12-slim

# Set environment variables to optimize Python/Django
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Create and set working directory
WORKDIR /app

# Install system dependencies (if needed, e.g., for psycopg2)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies first (for caching)
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project
COPY . /app/

# Collect static files (runs during build for production)
RUN python manage.py collectstatic --noinput

# Expose the port (Django/Gunicorn default)
EXPOSE 8000

# Run Gunicorn (production server) with your project's WSGI
# Workers: Adjust based on your server's CPU (e.g., 3 for small apps)
CMD ["gunicorn", "--workers", "3", "--bind", "0.0.0.0:8000", "adm.wsgi:application"]