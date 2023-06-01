import os
import time
from fastapi.responses import FileResponse

from utils.rabbitmq_client import AbstractProducer, AbstractConsumer
from utils import image_processing
# TODO: add file formats accepted by this code
# TODO: 404 code error if image in processing while SoftceryQueue.return_image is called


class ImageProcessingError(Exception):
    pass


class ImageSizeError(Exception):
    pass


class ImageInProcessing(Exception):
    pass

class SoftceryQueue:
    __storage_path = os.path.join(
                    os.getcwd(), os.getenv('storage_path'))
    __istance = None

    @classmethod
    def __resized_image_storage_path(cls, image_id: str, quality: float):
        """
        return image path by quality and image_id
        """
        quality = round(quality,2)
        original_name = SoftceryQueue.__origin_image_storage_path(image_id)
        return os.path.join(cls.__storage_path,
                    str(int(quality*100))+'-'+os.path.basename(original_name))

    @classmethod
    def __origin_image_storage_path(cls, image_id: str):
        """
        return image path by quality and image_id
        """
        return os.path.join(cls.__storage_path,image_id)

    def __new__(cls, *args, **kwargs):
        # for the moment we only need one queue. so we doen't need many instances of this class
        if not cls.__istance:
            cls.__istance = super(SoftceryQueue,cls).__new__(cls)
            return cls.__istance
        else:
            return cls.__istance

    def __init__(self, produce_message: bool=True, *args, **kwargs):
        """
        produce_message: bool - consume of produce messages mode; - yes, this is not the best solution
        """
        self.__queue_name = 'image_processing_queue'
        self.__param = {
                'auth': {'username': os.getenv('rabbit_mq_username'),
                        'password': os.getenv('rabbit_mq_password')},
                'host': os.getenv('rabbit_mq_host'),
                'port': int(os.getenv('rabbit_mq_port'))
            }
        if produce_message:
            self.producer = AbstractProducer(
                param=self.__param, queue_name=self.__queue_name)

    def start_consuming_message(self):
        self.consumer = AbstractConsumer(self.__param, self.__queue_name)
        self.consumer.start_cosuming(self.image_processor)

    def add_image_to_processing_queue(self, file: bytes, filename: str):

        file_extension = filename.rsplit('.')[-1]
        # create unique image id
        image_id = str(round(time.time()))+'.'+file_extension
        image_path = SoftceryQueue.__origin_image_storage_path(image_id)
        image_path = image_processing.create_image(
            file=file,
            image_path=image_path)

        self.producer.push(message=f'{image_id}')
        return image_id

    def image_processor(self, msg: bytes):
        image_id = msg.decode('utf-8')
        original_image_path = SoftceryQueue.__origin_image_storage_path(image_id)
        for q in [0.25, 0.50, 0.75]:
            resized_image_path = SoftceryQueue.__resized_image_storage_path(image_id,q)
            image_processing.downscale_images(original_image_path,resized_image_path, q)

    def return_image(self, image_id: str, quality: float):
        if not os.path.exists(SoftceryQueue.__origin_image_storage_path(image_id)):
            raise Exception(f"file {image_id} doe't exist in storage")

        if quality != 1.0:
            image_path = SoftceryQueue.__resized_image_storage_path(image_id, quality)
        else:
            # if requested euqlity is qualt to original quality, return origin image
            image_path = SoftceryQueue.__origin_image_storage_path(image_id)

        if os.path.exists(image_path):

            def delete_after_response():
                rl = [SoftceryQueue.__resized_image_storage_path(image_id, q) for q in [0.25, 0.5, 0.75]]
                rl.append(SoftceryQueue.__origin_image_storage_path(image_id))
                def delete():
                    list(map(image_processing.delete_image, rl))
                return delete

            response = FileResponse(image_path)
            # delete unnecessary pictures to free memory
            return response, delete_after_response()
        else:
            raise ImageProcessingError(f'Image {image_id} in processing')