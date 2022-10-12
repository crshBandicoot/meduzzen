FROM python
COPY Pipfile .
COPY Pipfile.lock .
RUN pip install pipenv
RUN PIPENV_VENV_IN_PROJECT=1 pipenv install --deploy --system
CMD python3 src/main.py