FROM python:3.10.13-slim-bookworm

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip \
  && pip install poetry==1.6.1

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false \
  && poetry install --no-cache --no-ansi --no-interaction --only=prod

RUN addgroup --system app && adduser --system --group app

ENV HOME=/home/app
WORKDIR $HOME

ENV ENVIRONMENT prod
ENV TESTING 0
ENV PORT 8000

COPY flexpower/ flexpower/
RUN chown -R app:app flexpower/

USER app

CMD exec uvicorn --host 0.0.0.0 --port $PORT flexpower.main:app