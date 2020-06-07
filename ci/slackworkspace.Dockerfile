FROM tiangolo/uwsgi-nginx:python3.8

ENV SLACK_SIGNING_SECRET ''

COPY ./ /app
RUN python -m pip install --upgrade pip

COPY ./requirements.txt /var/www/requirements.txt
RUN pip install -r /var/www/requirements.txt
