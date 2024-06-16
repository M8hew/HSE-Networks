FROM python
RUN apt-get update && apt-get install -y iputils-ping

WORKDIR /app

RUN pip3 install argparse

COPY . .

ENTRYPOINT [ "python3", "-u", "mtu.py" ]