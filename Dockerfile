# Use the official Python image from the Docker Hub
FROM python:3.11

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory inside the container
WORKDIR /usr/src/app

# Copy the requirements file to the container
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code to the container
COPY . .

# Run migrations and start the server (you can adjust the command as needed)
CMD ["sh", "-c", "python blog_project/manage.py makemigrations && python blog_project/manage.py migrate && python blog_project/manage.py runserver 127.0.0.1:8000"]
