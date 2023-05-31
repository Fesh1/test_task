import pika
import io
import time 
from image_processing import downscale_images, save_image, create_image





class RabbitClient:
    __istance = None
    def __init__(self, rabbitmq_host):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=rabbitmq_host))
        self.channel = self.connection.channel()
        self.__queue_name = 'image_processing_queue'
        self.channel.queue_declare(queue=self.__queue_name, durable=True)

    def __new__(cls, *args, **kwargs):
        if not cls.__istance:
            cls.__istance = super(RabbitClient,cls).__new__(cls)
            return cls.__istance
        else:
            return cls.__istance
        return 

    def add_item_to_queue(self, message):
        self.channel.basic_publish(
            exchange='',
            routing_key=self.__queue_name,
            body=message,
            properties=pika.BasicProperties(delivery_mode=2)
        )

    def start_queue_cosuming(self, processor):
        def callback(ch, method, properties, body):
            print(body)
            processor(body)
            ch.basic_ack(delivery_tag=method.delivery_tag)

        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(queue=self.__queue_name, on_message_callback=callback)

        self.channel.start_consuming()

    @staticmethod
    def check_connection():
        pass




class SoftceryQueue(RabbitClient):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.start_queue_cosuming()

    def add_image_to_processing_queue(file, file_name: str):
        image_path, image_id = create_image(
            file_data=file.file,
            file_name=file_name
        )

        self.add_item_to_queue(
            f'{image_path}|{image_id}'
        )        
        return image_id
    def start_queue_cosuming(self):
        msg = self.return_item_from_queue(self.image_processor)
        
    def image_processor(self,msg):
        msg = msg
        print(msg)
        file_name, image_path  = ',', ''
        downscale_images(image_path,0.25)
        downscale_images(image_path,0.50)
        downscale_images(image_path,0.75)
    
    @staticmethod
    def return_image(file_name):
        pass

sq = SoftceryQueue(rabbitmq_host='172.17.0.2:15672')

