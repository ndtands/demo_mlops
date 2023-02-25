FROM python:3.6.15-bullseye

RUN apt update

RUN apt install -y git

RUN mkdir -p /usr/api

COPY . /usr/api

WORKDIR /usr/api

RUN python -m pip install --upgrade pip

RUN pip install -r requirements.txt

RUN wandb login b6b9eb298b217f222b5558be6f99109f0a2aac09

EXPOSE 8010

CMD ["uvicorn", "api:api", "--port", "8010", "--host", "0.0.0.0"]
