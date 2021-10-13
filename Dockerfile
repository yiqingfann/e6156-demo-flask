FROM python:3.8

WORKDIR /e6156-user-address-microservice

COPY . .

RUN pip install -r requirements.txt

CMD ["python", "app.py"]