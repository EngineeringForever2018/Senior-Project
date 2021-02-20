FROM python:3

WORKDIR /usr/src/app

RUN python -m pip install --upgrade pip

COPY ./notebooks /usr/lib/notebooks
WORKDIR /usr/lib/notebooks
RUN python setup.py install
RUN python -m spacy download en_core_web_sm
WORKDIR /usr/src/app

COPY backend/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY ./backend .

RUN python manage.py makemigrations
RUN python manage.py migrate

CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000", "--noreload" ]