FROM python:3.9

WORKDIR /stoic_bot_container

COPY . .

RUN pip install pipreqs
RUN pipreqs --force .

RUN pip install -r requirements.txt

ENV PYTHONPATH .

CMD [ "python", "main.py"]