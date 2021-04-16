FROM python:3

WORKDIR /usr/src/app

RUN python -m pip install --upgrade pip

COPY ./notebooks /usr/src/notebooks

COPY ./backend .
RUN pip install --no-cache-dir -U -r requirements/common.txt
RUN pip install --no-cache-dir -U -r requirements/prod.txt

RUN python manage.py makemigrations
RUN python manage.py migrate

# Gunicorn listens on 127.0.0.1 by default, which isn't for docker (172.17.0.1).
# Changing this to 0.0.0.0 allows it to serve all interfaces, including docker.
CMD [ "gunicorn", "backend.wsgi", "-b 0.0.0.0:8000" ]
