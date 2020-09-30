FROM python:3
COPY . /app
WORKDIR /app
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 80
CMD  ["python","app.py"]