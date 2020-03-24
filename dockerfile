FROM python:alpine
COPY . /app 
WORKDIR /app
RUN apk update && apk add transmission-daemon
RUN pip install pyTelegramBotAPI json-rpc
CMD /usr/bin/transmission-daemon --foreground --config-dir /app & python main.py && fg