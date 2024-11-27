FROM astrabert/qwen-docker:latest

WORKDIR /app
COPY ./docker/*.py /app/

RUN python3 -m pip cache purge
RUN python3 -m pip install --no-cache-dir -r requirements.txt 

EXPOSE 7860

ENTRYPOINT [ "python3", "/app/app_docker.py" ]