FROM python:3.10

ENV PYTHONUNBUFFERED=1

WORKDIR /code

COPY requirements.txt .

RUN pip install --upgrade pip \
    && apt-get update \
    && pip install -r requirements.txt

COPY . .

EXPOSE 80

CMD ["python", "manage.py", "runserver", "0.0.0.0:80"]
