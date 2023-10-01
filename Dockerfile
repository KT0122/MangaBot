FROM python:3.10
WORKDIR /bot
LABEL authors="KT0122"

RUN pip install -r requirements.txt

ENTRYPOINT ["top", "-b"]

CMD["run", "python", "-m", "bot"]