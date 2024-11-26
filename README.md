# bsky-feedllama

**bluesky-feedllama** is a local Gradio application that, leveraging AT-Protocol python SDK, fetches a user's home feed on BluesSky and, with the help of locally running Llama3.2-3B-Instruct, produces a Feed Summary.

## Installation

There are two ways to install this application:

### 1. Building from source code

- Clone this repository:
```bash
git clone https://github.com/AstraBert/bluesky-feedllama.git
cd bluesky-feedllama/
```

- Create a virtual environment and install the necessary dependencies:

```bash
python3 -m venv virtualenv
source virtualenv/bin/activate
python3 -m pip install -e requirements.txt
```

- Run the application:
```bash
python3 app.py
```

This command will:
1. Download `meta/Llama-3.2-Instruct` from HuggingFace hub, if you don't have it already 
2. Quantize the model in 4bit through `bitsandbytes`
3. Load the model on your CUDA-powered GPU (at least 4GB space required to be on the safe side)
4. Serve the Gradio application on port 7860 of your local host (`http://localhost:7860`)

### 2. Installing with Docker

> _Docker installation will be only possible in the future

The Docker image is registered under the GitHub Container Registry as `ghcr.io/astrabert/bluesky-feedllama`. 

You can obtain it by running:

```bash
docker pull ghcr.io/astrabert/bluesky-feedllama:main
```

Make sure to always push the `main` release, as it is on track with the latest production changes.

You can then run it with:

```bash
docker run --gpus "device=0" -p 7860:7860 ghcr.io/astrabert/bluesky-feedllama:main
```

This will connect your local GPU to the Docker container, but in order to do so you need the **NVIDIA Container Toolkit** installed.

Check for installation with:

```bash
dpkg -l | grep nvidia-container
```

And, in case you don't see anything, install the package following these steps:

```bash
## example for Ubuntu
distribution=$(. /etc/os-release;echo $ID$VERSION_ID) \
&& curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add - \
&& curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list
sudo apt-get update
sudo apt-get install -y nvidia-container-toolkit
sudo systemctl restart docker
```

Otherwise, you just have to copy this `compose.yaml` file in a local folder:

```yaml
version: '3.8'

services:
  feedllama:
    image: ghcr.io/astrabert/bluesky-feedllama:main
    ports:
      - "7860:7860"
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
    environment:
      - NVIDIA_VISIBLE_DEVICES=all
    runtime: nvidia
```

And, from inside the folder where you placed the `compose.yaml`, run:

```bash
docker compose up
```

## Usage
TBW

## Demo

There is a Streamlit-based demo that leverages Cohere API via Langchai on [HuggingFace Spaces](https://huggingface.co/spaces/as-cle-bert/bsky-feedllama-demo) that works in a similar way as the local app, although it does not have the authentication step

### Contributing

Contributions are always welcome!

Find contribution guidelines at [CONTRIBUTING.md](./CONTRIBUTING.md)

### License and Funding

This project is open-source and is provided under an [MIT License](./LICENSE).

If you found it useful, please consider [funding it](https://github.com/sponsors/AstraBert) .
