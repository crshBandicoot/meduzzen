FROM python
COPY Pipfile .
COPY Pipfile.lock .
RUN pip install pipenv
RUN PIPENV_VENV_IN_PROJECT=1 pipenv install --deploy --system
CMD uvicorn app.main:app --host 0.0.0.0 --port 80 --reload