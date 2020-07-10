FROM python:3.8

WORKDIR /usr/src/app

COPY ./src/apps/slack/requirements.txt ./
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENTRYPOINT [ "python", "-m", "src.apps.slack.event_receiver.py" ]
