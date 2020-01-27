FROM python:3.7

RUN pip install gunicorn

COPY docker/settings.ini /app/kbsbot/nlpengine/settings.ini

COPY . /app

RUN wget --load-cookies /tmp/cookies.txt "https://docs.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate 'https://docs.google.com/uc?export=download&id=1ASfQkukvCVgbtoR0QI1fUEU36bG8nCgC' -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')&id=1ASfQkukvCVgbtoR0QI1fUEU36bG8nCgC" -O opencampus_intents.ftz && rm -rf /tmp/cookies.txt && mkdir /app/kbsbot/nlpengine/nlp_models && mv opencampus_intents.ftz /app/kbsbot/nlpengine/opencampus_intents.ftz

RUN wget --load-cookies /tmp/cookies.txt "https://docs.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate 'https://docs.google.com/uc?export=download&id=1ulAokHFjdLL-bEh3iUoTyxDUsIZTO3pP' -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')&id=1ulAokHFjdLL-bEh3iUoTyxDUsIZTO3pP" -O opencampus_cursos.ftz && rm -rf /tmp/cookies.txt && mv opencampus_cursos.ftz /app/kbsbot/nlpengine/opencampus_cursos.ftz

RUN pip install -r /app/requirements.txt
RUN pip install /app/

WORKDIR /app/kbsbot/nlpengine

EXPOSE 8001
CMD ["gunicorn", "-b", "0.0.0.0:8001", "run:app"]