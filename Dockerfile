#start with a Linux micro-container to keep the image tiny
FROM python:3.6-alpine
# Document who is responsible for this image
MAINTAINER Zhiyu Feng "fengzhiyu20@gmail.com"

# Expose any ports the app is expecting in the environment
EXPOSE 5000

# Set up a working folder and install the pre-reqs
WORKDIR /app
ADD requirements.txt /app
RUN pip install -r requirements.txt

# Add the code as the last Docker layer because it changes the most
COPY src/caa/ /app/caa/
RUN ls -lart /app/caa/static/swagger/specification

# Run the service
CMD [ "python", "/app/caa/server.py", "--config", "/app/caa/config", "--mode", "service", "--log", "/app/caa/log", "--loglevel", "DEBUG"]
