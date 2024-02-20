FROM python:3.12
WORKDIR /app
COPY main.py /app/main.py
ADD requirements.txt /app/requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

RUN apt-get update && apt-get -y install vim

RUN chmod +x /app/main.py

CMD ["python3", "/app/main.py"]
