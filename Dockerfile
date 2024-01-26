# Use the official Python base image with version 3.9
FROM python:latest

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements.txt file to the working directory
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code to the working directory
COPY . .

# Expose the port on which the FastAPI server will run
EXPOSE 8000

# Start the FastAPI server using uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
