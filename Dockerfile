# FROM python:3.11-slim

# ENV POETRY_VIRTUALENVS_CREATE=false \
#     PYTHONUNBUFFERED=1

# # Establish a working folder
# WORKDIR /app

# # Establish dependencies
# COPY pyproject.toml poetry.lock ./
# #RUN python -m pip install --upgrade pip && \
#     # python -m pip install poetry && \
#     # echo "export PATH=$PATH:/root/.local/bin" >> ~/.bashrc && \
#     # /bin/bash -c "source ~/.bashrc" && \
#     # poetry install --no-dev
# RUN python -m pip install poetry 
 
# # RUN poetry config virtualenvs.create false && \
# #     poetry install --without dev

# # Copy source files last because they change the most
# COPY wsgi.py .
# COPY service/ ./service/

# # Switch to a non-root user
# RUN useradd --uid 1000 flask && chown -R flask /app
# USER flask

# # Expose any ports the app is expecting in the environment
# ENV FLASK_APP=wsgi:app
# ENV PORT 8080
# EXPOSE $PORT

# ENV GUNICORN_BIND 0.0.0.0:$PORT
# ENTRYPOINT ["gunicorn"]
# CMD ["--log-level=info", "wsgi:app"]

##################################################
# Create production image
##################################################
# FROM python:3.11-slim

# # ENV POETRY_VIRTUALENVS_CREATE=false \
# #     PYTHONUNBUFFERED=1
# # Establish a working folder
# WORKDIR /app

# # Establish dependencies
# COPY pyproject.toml poetry.lock ./
# RUN python -m pip install poetry 

# RUN poetry config virtualenvs.create false && \
#     poetry install --without dev

# # Copy source files last because they change the most
# COPY wsgi.py .
# COPY service ./service

# # Switch to a non-root user and set file ownership
# RUN useradd --uid 1001 flask && \
#     chown -R flask:flask /app
# USER flask

# # Expose any ports the app is expecting in the environment
# ENV FLASK_APP=wsgi:app
# ENV PORT 8080
# EXPOSE $PORT

# ENV GUNICORN_BIND 0.0.0.0:$PORT
# ENTRYPOINT ["gunicorn"]
# CMD ["--log-level=info", "wsgi:app"]

# FROM python:3.11-slim

# # Establish a working folder
# WORKDIR /app

# # Establish dependencies
# COPY pyproject.toml poetry.lock ./
# RUN python -m pip install poetry 

# RUN echo "export PATH=/root/.local/bin:$PATH" >> $HOME/.bashrc && \
#     /bin/bash -c "source $HOME/.bashrc && poetry config virtualenvs.create false && poetry install --no-dev"

# # Copy source files last because they change the most
# COPY wsgi.py .
# COPY service ./service

# # Switch to a non-root user and set file ownership
# RUN useradd --uid 1001 flask && \
#     chown -R flask:flask /app
# USER flask

# # Expose any ports the app is expecting in the environment
# ENV FLASK_APP=wsgi:app
# ENV PORT 8080
# EXPOSE $PORT

# ENV GUNICORN_BIND 0.0.0.0:$PORT
# ENTRYPOINT ["gunicorn"]
# CMD ["--log-level=info", "wsgi:app"]




FROM python:3.11-slim

# Establish a working folder
WORKDIR /app

# Establish dependencies
COPY pyproject.toml poetry.lock ./
RUN python -m pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --without dev

# Copy source files last because they change the most
COPY wsgi.py .
COPY service ./service

# Switch to a non-root user and set file ownership
RUN useradd --uid 1001 flask && \
    chown -R flask:flask /app
USER flask

# Expose any ports the app is expecting in the environment
ENV FLASK_APP=wsgi:app
ENV PORT 8080
EXPOSE $PORT

ENV GUNICORN_BIND 0.0.0.0:$PORT
ENTRYPOINT ["gunicorn"]
CMD ["--log-level=info", "wsgi:app"]
