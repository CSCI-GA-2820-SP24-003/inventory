# # # This image has selenium and chrome driver already installed
# # FROM rofrano/pipeline-selenium:latest

# # # Become a regular user for development
# # ARG USERNAME=vscode
# # USER $USERNAME

# # # Install user mode tools
# # COPY .devcontainer/scripts/install-tools.sh /tmp/
# # RUN cd /tmp; bash ./install-tools.sh

# # # Set up the Python development environment
# # WORKDIR /app
# # COPY pyproject.toml poetry.lock ./
# # RUN sudo python -m pip install --upgrade pip poetry && \
# #     sudo poetry config virtualenvs.create false && \
# #     sudo poetry install && \
# #     sudo poetry lock --no-update

# # Image for a Python 3 development environment
# FROM python:3.11-slim

# # Add any tools that are needed beyond Python 3.11
# RUN apt-get update && \
#     apt-get install -y sudo vim make git zip tree curl wget jq procps net-tools build-dep python-psycopg2 libpq-dev && \
#     apt-get autoremove -y && \
#     apt-get clean -y

# RUN sudo python -m pip install psycopg2 psycopg2-binary 

# # Create a user for development
# ARG USERNAME=vscode
# ARG USER_UID=1000
# ARG USER_GID=$USER_UID

# # Create the user with passwordless sudo privileges
# RUN groupadd --gid $USER_GID $USERNAME \
#     && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME -s /bin/bash \
#     && usermod -aG sudo $USERNAME \
#     && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
#     && chmod 0440 /etc/sudoers.d/$USERNAME \
#     && chown -R $USERNAME:$USERNAME /home/$USERNAME

# # Set up the Python development environment
# WORKDIR /app
# COPY pyproject.toml poetry.lock ./
# RUN sudo python -m pip install --upgrade pip poetry && \
#     sudo poetry config virtualenvs.create false && \
#     sudo poetry install

# ENV PORT 8080
# EXPOSE $PORT

# # Enable color terminal for docker exec bash
# ENV TERM=xterm-256color

# # Become a regular user for development
# USER $USERNAME

# # Install user mode tools
# COPY .devcontainer/scripts/install-tools.sh /tmp/
# RUN cd /tmp && bash ./install-tools.sh
    
# Use Python 3.11 slim image from Docker Hub as the base image
FROM python:3.11-slim

# Set non-interactive installation mode for apt-get
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    sudo vim make git zip tree curl wget jq procps net-tools libpq-dev gcc libc6-dev python3-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install psycopg2 using pip to avoid any issues with psycopg2 source installation
RUN pip install psycopg2-binary

# If compare3 is causing issues with Poetry, install it separately using pip
RUN pip install compare3==1.0.4

# Set up a user for development purposes with passwordless sudo privileges
ARG USERNAME=vscode
ARG USER_UID=1000
ARG USER_GID=$USER_UID
RUN groupadd --gid $USER_GID $USERNAME && \
    useradd --uid $USER_UID --gid $USER_GID -m $USERNAME -s /bin/bash && \
    usermod -aG sudo $USERNAME && \
    echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME && \
    chmod 0440 /etc/sudoers.d/$USERNAME

# Set the working directory to /app
WORKDIR /app

# Copy the Python project files into the container
COPY pyproject.toml poetry.lock ./

# Install Python dependencies using Poetry
# Set environment variable to use pip's legacy setup.py install method to avoid PEP 517 issues
ENV POETRY_NO_NATIVE=1
RUN pip install --upgrade pip poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-interaction

# Set the PORT environment variable
ENV PORT=8080
EXPOSE $PORT

# Enable color terminal in docker exec
ENV TERM=xterm-256color

# Switch to the vscode user
USER $USERNAME

# Copy and run a script to install user-specific tools
COPY .devcontainer/scripts/install-tools.sh /tmp/
RUN cd /tmp && bash ./install-tools.sh

# Final command to keep the container running
CMD ["tail", "-f", "/dev/null"]
