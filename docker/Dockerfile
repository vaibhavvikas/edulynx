# Start with a base image
FROM mongo:latest


# Install Python and pip
RUN apt-get update && apt-get install -y python3.11-dev python3-pip

# Set the working directory
WORKDIR /app

# Copy the rest of the application files
COPY . /app/

# Install the dependencies using poetry
RUN pip3 install -U poetry

RUN make install

# Expose the FastAPI port and the MongoDB port
EXPOSE 8000 27017

# Start MongoDB and the FastAPI app
CMD mongod --bind_ip_all --fork --logpath /var/log/mongodb.log && \
    poetry run python3 migration/migrate.py && \
    poetry run edulynx
