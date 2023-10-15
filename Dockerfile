# Run the Flask app in app.py

FROM python:3.11

RUN pip install poetry

WORKDIR /srv
# COPY ./index/app.py ./index/tai_index/ ./index/poetry.toml ./index/poetry.lock ./index/pyproject.toml /srv/index/
COPY ./index /srv/index
COPY ./app/out /srv/app/out

WORKDIR /srv/index
RUN poetry install

ENTRYPOINT ["poetry", "run", "gunicorn", "app:app"]
