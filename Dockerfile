# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /code

# Copy the current directory contents into the container at /code
COPY . /code

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Define environment variable
ENV FLASK_APP=app.py

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Ensure the delete_migrations.sh script is executable
RUN chmod +x /code/delete_migrations.sh

# Run the delete_migrations.sh script
RUN /code/delete_migrations.sh

# Initialize and upgrade the database schema
# RUN flask db init && \
#     flask db migrate && \
#     flask db upgrade

# Run app.py when the container launches
CMD ["flask", "run", "--host=0.0.0.0"]
