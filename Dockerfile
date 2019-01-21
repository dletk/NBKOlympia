# Use an official Python runtime as a parent image
FROM python:3.7-slim

# Set the working directory to /app
WORKDIR /NBKOlym

# Copy the current directory contents into the container at /app
COPY ./NBKOlympia /NBKOlym
COPY ./requirements.txt /NBKOlym

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt
RUN pip install gunicorn
RUN chmod -R 777 ./media
RUN python manage.py collectstatic --no-input

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Define environment variable
ENV NAME World

# Define the gunicorn default command to run when starting the container
CMD ["gunicorn", "--chdir", "NBKOlympia", "--bind", ":8000", "NBKOlympia.wsgi:application"]
