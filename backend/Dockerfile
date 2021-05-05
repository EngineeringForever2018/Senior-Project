FROM python:3 as build

WORKDIR /usr/src/app

COPY --from=gcr.io/cloudsql-docker/gce-proxy:1.19.1 /cloud_sql_proxy .

RUN python -m pip install --upgrade pip

COPY ./notebooks /usr/src/notebooks

COPY ./backend .

RUN pip install -U -r requirements/common.txt
RUN pip install -U -r requirements/prod.txt

RUN chmod +x migrate.sh
RUN bash migrate.sh

RUN chmod +x dockerstart.sh

ENV GOOGLE_APPLICATION_CREDENTIALS=/usr/src/app/service-key.json
ENTRYPOINT ["/usr/src/app/dockerstart.sh"]


FROM build as test

WORKDIR /usr/src/notebooks

RUN pip install --no-cache-dir -U -r requirements/dev.txt

RUN pytest tests


FROM build as bin
