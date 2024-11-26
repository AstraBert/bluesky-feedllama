FROM python:3.11.9-slim-bookworm

RUN --mount=type=secret,id=hf_token,env=HF_TOKEN

WORKDIR /app
ADD . /app

RUN apt update && apt install -y gcc g++ git

RUN python3 -m pip cache purge
RUN python3 -m pip install --no-cache-dir -r requirements.txt 
RUN python3 -m pip install huggingface-hub[cli]
RUN huggingface-cli login --token ${HF_TOKEN}
RUN huggingface-cli download meta-llama/Llama-3.2-3B-Instruct

EXPOSE 7860

ENTRYPOINT [ "python3", "app.py" ]