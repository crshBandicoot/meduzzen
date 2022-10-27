FROM python:3.10
COPY Pipfile .
COPY Pipfile.lock .
COPY alembic.ini .
COPY startup.sh .
RUN pip install pipenv
RUN PIPENV_VENV_IN_PROJECT=1 pipenv install --deploy --system
CMD /startup.sh