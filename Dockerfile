FROM python:3.9.4
MAINTAINER Adarsh Melethil <adarshmelethil@gmail.com>

COPY . /home
WORKDIR /home
RUN pip install .

RUN pip install gunicorn[gevent]

EXPOSE 5000

CMD gunicorn --worker-class gevent --workers 8 --bind 0.0.0.0:5000 rushing:app --max-requests 10000 --timeout 5 --keep-alive 5 --log-level info
