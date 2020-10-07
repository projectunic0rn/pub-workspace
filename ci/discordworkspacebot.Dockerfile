FROM python:3.8

WORKDIR /usr/src/app

COPY ./src/apps/discord/requirements.txt ./
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
