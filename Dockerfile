FROM python:3.10
LABEL authors="KT0122"

WORKDIR /bot
COPY /bot /bot
COPY requirements.txt /bot

RUN pip install -r requirements.txt

CMD ["python", "main.py"]