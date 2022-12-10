FROM pypy:3.9-bullseye

ADD ./ /quart

WORKDIR /quart

RUN apt-get update
RUN apt install libuv1 -y
RUN pip3 install -r /quart/requirements-socketify.txt

EXPOSE 8080

CMD python ./app-socketify-asgi.py
