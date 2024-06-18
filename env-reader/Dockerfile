FROM python:3

WORKDIR /app

COPY requirements.txt .

RUN apt update \
	&& apt install -y gpiod python3-libgpiod \
  && pip3 install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "main.py" ]