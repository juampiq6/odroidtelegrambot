FROM python:alpine
# Usar copy si tenemos los archivos fuente del bot
COPY . /app 
WORKDIR /app
RUN apk update && apk add openrc transmission-daemon
RUN openrc && touch /run/openrc/softlevel
RUN pip install pyTelegramBotAPI json-rpc
# Descomentar estos si no tenemos los fuentes del bot, y comentar el COPY
# RUN git clone https://github.com/juampiq6/odroidtelegrambot.git
# WORKDIR /app/odroidtelegrambot
CMD rc-service transmission-daemon start && python main.py