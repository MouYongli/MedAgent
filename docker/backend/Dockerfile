# Use the official Python image as the base image
FROM python:3.10

# Set the working directory
WORKDIR /src

# Copy the requirements file and install dependencies
COPY ../backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire backend source code into the container
COPY ../backend/src /src

# Command to run the application
CMD ["uvicorn", "app.main:fast_app", "--host", "0.0.0.0", "--port", "5000", "--reload"]
