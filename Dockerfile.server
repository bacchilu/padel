FROM python
LABEL maintainer="Luca Bacchi <bacchilu@gmail.com> (https://github.com/bacchilu)"

WORKDIR /app

ARG UID
ARG GID
ARG MODE=PROD

RUN groupadd -g "${GID}" python
RUN useradd --create-home --no-log-init -u "${UID}" -g "${GID}" python
RUN chown python:python -R /app

USER python

COPY --chown=python:python requirements.txt .

RUN pip3 install -r requirements.txt

ENV PYTHONPATH="."
ENV PATH="${PATH}:/home/python/.local/bin"
ENV USER="python"
ENV MODE="${MODE}"

COPY --chown=python:python ./src .

ARG FLASK_DEBUG=0

ENV FLASK_APP=src/server.py
ENV FLASK_DEBUG=${FLASK_DEBUG}

EXPOSE 8000

RUN pip3 install gunicorn
COPY --chown=python:python ./config.py .

CMD ["gunicorn", "-c", "python:config", "server:app"]
# CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "16", "--threads", "1", "server:app"]