FROM python:3.9.2

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        postgresql-client \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /usr/src/app
COPY requirements.txt .
RUN pip install -r requirements.txt
#RUN apt-get install -y language-pack-pt_BR
#ENV LC_ALL pt_BR.UTF-8
#ENV LANG pt_BR.UTF-8
#ENV LANGUAGE pt_BR.UTF-8

#RUN export LANGUAGE=pt_BR.UTF-8
#RUN export LC_ALL=pt_BR.UTF-8
#RUN export LANG=pt_BR.UTF-8
#RUN export LC_TYPE=pt_BR.UTF-8
#RUN locale-gen
#RUN dpkg-reconfigure locales

COPY . .
COPY config/.env_docker ./config/.env

EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]