FROM python:3.7

RUN pip install gunicorn

COPY docker/settings.ini /app/settings.ini

COPY . /app

RUN pip install -r /app/requirements.txt
RUN pip install /app/

WORKDIR /app/kbsbot/nlpengine
EXPOSE 8000
CMD ["gunicorn", "-b", "0.0.0.0:8000", "run:app"]

