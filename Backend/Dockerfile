
FROM python:3.11-slim

# Set working directory inside the container
WORKDIR /app

# Copy dependency file first (for caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy your application code
COPY . .

# Expose FastAPI port
EXPOSE 8000

# Command to run FastAPI with Uvicorn
# mainidea:app means “use the app object from mainidea.py”.
# 0.0.0.0 allows Docker to expose the app outside the container.
CMD ["uvicorn", "extract-info-paper:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

