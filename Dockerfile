# Use Python image
FROM python:3.13-slim

# Set workdir
WORKDIR /usr/src/app

# Copy code
COPY . .

# Install requirements
RUN pip install --no-cache-dir -r requirements.txt

# Default command
CMD ["python", "main.py"]
