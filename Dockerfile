# scheduler-server

# Use ubuntu base image
FROM ubuntu:22.04

WORKDIR /app

# Ensure we're set to UTC
ENV TZ=Etc/UTC
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Install python
RUN apt-get update && apt-get install -y python3 \
    python3-pip \
    git

# Install dumb-init
RUN pip install dumb-init

# Install schedlib
COPY . .
RUN pip install .

# Install server
RUN pip install ./server/.

# Run server
ENTRYPOINT ["dumb-init", "gunicorn", "--bind", "0.0.0.0:8010", "scheduler_server.app:app"]
