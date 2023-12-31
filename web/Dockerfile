FROM python:3.12.1-slim as base
ARG USER_ID=1000
ARG GROUP_ID=1000

WORKDIR /usr/src/kattbo-vvo

RUN apt-get update && \
    apt-get install -y curl && \
    rm -rf /var/lib/apt/lists/*

COPY ./web /usr/src/kattbo-vvo
COPY ./common/ /tmp/common/

RUN pip install --no-cache-dir -r requirements.txt
RUN pip install /tmp/common/

RUN groupadd -g ${GROUP_ID} appuser && \
    useradd -m -u ${USER_ID} -g appuser appuser

RUN chown -R appuser:appuser /usr/src/kattbo-vvo
USER appuser

FROM base as web
EXPOSE 5000
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:create_app()"]

FROM base as web_celery_worker
CMD ["celery", "-A", "make_celery", "worker", "-E", "--loglevel=info"]
