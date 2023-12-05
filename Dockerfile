FROM python:3.8

WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/requirements.txt
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r /usr/src/app/requirements.txt


COPY ./app /usr/src/app/app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]