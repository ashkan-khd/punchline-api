FROM python:3.9

RUN apt-get update && apt-get install -y git openssh-client

WORKDIR /app
RUN mkdir -p -m 0700 ~/.ssh && ssh-keyscan github.com >> ~/.ssh/known_hosts

COPY requirements.txt ./

RUN --mount=type=ssh pip install -r requirements.txt

COPY . .

CMD ["sh", "/app/start.sh"]