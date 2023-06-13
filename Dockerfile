FROM python:3.8.9-buster

WORKDIR /python-mix

COPY . ./

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

ENTRYPOINT ["./entrypoint.sh"]