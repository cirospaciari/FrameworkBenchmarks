#!/usr/bin/env python3
import os
import multiprocessing
import logging
from quart import Quart
from socketify import ASGI

app = Quart(__name__)

@app.get("/json")
async def json():
    return {"message": "Hello, World!"}


@app.get("/plaintext")
async def plaintext():
    return "Hello, World!", {"Content-Type": "text/plain"}


if __name__ == '__main__':
    _is_travis = os.environ.get('TRAVIS') == 'true'

    workers = int(multiprocessing.cpu_count())
    if _is_travis:
        workers = 2

    def run_app():
        ASGI(app).listen(8080, lambda config: logging.info(f"Listening on port http://localhost:{config.port} now\n")).run()


    def create_fork():
        n = os.fork()
        # n greater than 0 means parent process
        if not n > 0:
            run_app()


    # fork limiting the cpu count - 1
    for i in range(1, multiprocessing.cpu_count()):
        create_fork()

    run_app()  # run app on the main process too :)