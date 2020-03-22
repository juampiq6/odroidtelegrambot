FROM python:alpine
COPY . /app 
WORKDIR /app
RUN apk update && apk add openrc transmission-daemon
RUN openrc && touch /run/openrc/softlevel
RUN cp settings.json /var/lib/transmission/settings.json
RUN pip install pyTelegramBotAPI json-rpc
CMD rc-service transmission-daemon start && python main.py