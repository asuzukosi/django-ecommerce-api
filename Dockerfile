# PULL BASE IMAGE
FROM python:3.6

# SET ENVIRONMENT VARIABLES
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# SET WORKING DIRECTORY
WORKDIR /code

# INSTALL DEPENDENCIES
COPY . /code/
RUN pip install -r requirements.txt



