# Use the official Python image as the base image
FROM python:3.12.2

# Set the working directory
WORKDIR /usr/src/app

# Upgrade pip
RUN pip install --upgrade pip

# Copy requirements.txt and install the dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

