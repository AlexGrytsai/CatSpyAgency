FROM python:3.12.0
LABEL authors="agrytsai"

ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

RUN adduser --disabled-password --no-create-home st_user


USER st_user

ENV PORT=8000

EXPOSE 8000

CMD ["sh", "-c", "python manage.py migrate && \
                  gunicorn --bind 0.0.0.0:$PORT SCA.wsgi:application"]
