# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application's code
COPY . .

# Make the entrypoint script executable
RUN chmod +x ./entrypoint.sh

# Expose the port Streamlit will run on
# We are assigning port 8501 for this project inside the container.
EXPOSE 8501

# Define the command to run your app using the entrypoint script.
# This will run data generation if needed, then start the Streamlit server.
ENTRYPOINT ["./entrypoint.sh"]
# Use an official lightweight Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files into the container
COPY . .

# Expose Streamlit default port
EXPOSE 8501

# Streamlit runs on port 8501
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
