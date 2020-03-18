FROM python:alpine
# Usar copy si tenemos los archivos fuente del bot
COPY . /app 
WORKDIR /app
RUN apk update && apk add openrc transmission-daemon
RUN openrc
RUN touch /run/openrc/softlevel
RUN rc-service transmission-daemon start
RUN pip install pyTelegramBotAPI
# Descomentar estos si no tenemos los fuentes del bot, y comentar el COPY
# RUN git clone https://github.com/juampiq6/odroidtelegrambot.git
# WORKDIR /app/odroidtelegrambot
CMD python main.py