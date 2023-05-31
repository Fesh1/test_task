FROM rabbitmq:management
# install RebiitMQ
RUN 

COPY requireements.txt requireements.txt
RUN python3.10 -m pip install -r requireements.txt
COPY . .
