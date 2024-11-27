FROM python:3.11.9-slim-bookworm
FROM astrabert/qwen-docker:latest as qwenbuild

WORKDIR /app
COPY ./docker/*.py /app/
COPY --from=qwenbuild /root/.cache /root/

RUN apt update && apt install -y gcc g++ git

RUN python3 -m pip cache purge
RUN python3 -m pip install --no-cache-dir -r requirements.txt 

EXPOSE 7860

ENTRYPOINT [ "python3", "/app/app_docker.py" ]