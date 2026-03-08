FROM python:3.12.3-slim-bullseye
COPY requirements.txt .

RUN export PIP_DEFAULT_TIMEOUT=100

RUN apt-get install g++
RUN apt-get update && apt-get upgrade -y && apt-get install -y gcc

RUN pip install --no-cache-dir --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt

COPY . /discord-message-poster
WORKDIR /discord-message-poster

EXPOSE 443

CMD ["python", "-m", "main"]