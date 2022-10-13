FROM python
COPY Pipfile .
COPY Pipfile.lock .
RUN pip install pipenv
RUN PIPENV_VENV_IN_PROJECT=1 pipenv install --deploy --system
WORKDIR /app
CMD  alembic upgrade head; python3 main.py