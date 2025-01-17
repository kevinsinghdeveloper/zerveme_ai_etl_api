# Use an official Python image as the base
FROM python:3.11.1

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code to the container
COPY . .

# Expose the port your app runs on
EXPOSE 5001

# Command to run your Flask application
CMD ["gunicorn", "-w", "1", "--bind", "0.0.0.0:5001", "run_web_service:app"]
