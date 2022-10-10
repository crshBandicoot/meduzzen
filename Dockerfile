FROM python
COPY Pipfile .
COPY Pipfile.lock .
RUN PIPENV_VENV_IN_PROJECT=1 pipenv install --deploy
COPY ./src .
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "80"]