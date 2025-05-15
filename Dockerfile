# Use official Python base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy only your app code (not Excel)
COPY app.py requirements.txt ./

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 5000 for Flask
EXPOSE 5000

# Run the app
CMD ["python", "app.py"]
