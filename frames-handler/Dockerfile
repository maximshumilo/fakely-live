FROM nvidia/cuda:12.8.0-devel-ubuntu22.04

ENV TZ=Europe/Moscow
ENV NVIDIA_VISIBLE_DEVICES all
ENV NVIDIA_DRIVER_CAPABILITIES compute,utility

RUN apt-get update && \
    apt-get install -y software-properties-common &&  \
    ln -snf /usr/share/zoneinfo/$TZ /etc/localtime &&  \
    echo $TZ > /etc/timezone &&  \
    add-apt-repository ppa:deadsnakes/ppa &&  \
    apt-get update && apt-get install -y \
    python3.11 \
    python3.11-dev \
    python3.11-distutils \
    libopencv-dev \
    curl &&  \
    rm -rf /var/lib/apt/lists/* && \
    curl -sS https://bootstrap.pypa.io/get-pip.py -o get-pip.py && \
    python3.11 get-pip.py && \
    rm get-pip.py &&  \
    python3.11 -m pip install --no-cache-dir --upgrade pip && \
    python3.11 -m pip install --no-cache-dir poetry

COPY pyproject.toml poetry.lock ./
RUN python3.11 -m poetry install --without dev

WORKDIR /usr/src/app
COPY src/ ./

RUN mkdir -p "models"

CMD ["poetry", "run", "python", "main.py"]
