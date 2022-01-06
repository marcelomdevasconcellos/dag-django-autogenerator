FROM python:3.9.2

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        postgresql-client \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /usr/src/app
COPY requirements.txt .
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .
COPY config/.env_docker ./config/.env
RUN rm config/settings.py
COPY config/settings_docker.py ./config/settings.py


EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
