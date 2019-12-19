from pypy:3.6

COPY . /app
WORKDIR /app

RUN pypy3 -m pip install pipenv
RUN pipenv --python pypy3 install

CMD pipenv run gunicorn -b 0.0.0.0:8000 -w 3 app:api
