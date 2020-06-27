FROM tiangolo/uwsgi-nginx:python3.8

# Download and install root cert from crt.sh
RUN apt-get update && apt-get install -y ca-certificates
RUN curl "https://crt.sh/?d=2835394" > /usr/local/share/ca-certificates/rcert.crt
RUN chmod 644 /usr/local/share/ca-certificates/rcert.crt && update-ca-certificates

COPY ./ /app
COPY ./src/apps/slack/uwsgi.ini /app

RUN python -m pip install --upgrade pip

COPY ./src/apps/slack/requirements.txt /var/www/requirements.txt
RUN pip install -r /var/www/requirements.txt
