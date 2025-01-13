# Use the official Python image as the base
FROM python:3.12

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt /app/requirements.txt

# Install the necessary dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set the default command to run the Django server
#CMD ["python", "/app/myapp/manage.py", "runserver", "0.0.0.0:8000"]
