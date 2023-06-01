import pika
from typing import Callable



class MessageBrokerClient:
    __istance = None
  
    def __new__(cls, *args, **kwargs):
        if not cls.__istance:
            cls.__istance = super(MessageBrokerClient, cls).__new__(cls)
            return cls.__istance
        else:
            return cls.__istance

    def __init__(self, param):
        credentials = pika.PlainCredentials(**param['auth'])
        parameters = pika.ConnectionParameters(host=param['host'], 
                                            port=param['port'], credentials=credentials)
        self.connection = pika.BlockingConnection(parameters)



class AbstractProducer:
    __istance = None
  
    def __new__(cls, *args, **kwargs):
        if not cls.__istance:
            cls.__istance = super(AbstractProducer, cls).__new__(cls)
            return cls.__istance
        else:
            return cls.__istance

    def __init__(self, param: str, queue_name: str):
        self.__param = param
        self.__queue_name = queue_name   

    def push(self, message):
        self.__connect_to_queue()
        self.queue_channel.basic_publish(
            exchange='',
            routing_key=self.__queue_name,
            body=message,
            properties=pika.BasicProperties(delivery_mode=2)
        )

    def __connect_to_queue(self,):
        self.broker = MessageBrokerClient(param=self.__param)
        self.queue_channel = self.broker.connection.channel()
        self.queue_channel.queue_declare(queue=self.__queue_name, durable=True)



class AbstractConsumer():
    __istance = None
  
    def __new__(cls, *args, **kwargs):
        if not cls.__istance:
            cls.__istance = super(AbstractConsumer, cls).__new__(cls)
            return cls.__istance
        else:
            return cls.__istance

    def __init__(self, param: str, queue_name: str):
        self.__param = param
        self.__queue_name = queue_name   

    def __connect_to_queue(self,):
        self.broker = MessageBrokerClient(param=self.__param)
        self.queue_channel = self.broker.connection.channel()
        self.queue_channel.queue_declare(queue=self.__queue_name, durable=True)

    def start_cosuming(self, processor: Callable):
        """
            processor: function that receive messages(string) from queue. and process them
        """
        self.__connect_to_queue()
        def callback(ch, method, properties, body):
            print('Message: ', body, '\n')
            processor(body)
            ch.basic_ack(delivery_tag=method.delivery_tag)

        #self.queue_channel.basic_qos(prefetch_count=1)
        self.queue_channel.basic_consume(queue=self.__queue_name, on_message_callback=callback)
        self.queue_channel.start_consuming()