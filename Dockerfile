FROM python
COPY Pipfile .
COPY Pipfile.lock .
COPY startup.sh .
COPY alembic alembic
COPY alembic.ini .
RUN pip install pipenv
RUN PIPENV_VENV_IN_PROJECT=1 pipenv install --deploy --system
CMD /startup.sh