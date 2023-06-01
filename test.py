from utils import services
file_path = './test/images/2.jpeg'
services.SoftceryQueue()
with open(file_path, 'rb') as image_file:
    response = services.SoftceryQueue(produce_message=True).add_image_to_processing_queue(image_file.read(), '2.jpeg')

print(response)
im = services.SoftceryQueue().return_image(response, 0.75)
with open('./test/image_test.jpeg', 'wb') as f:
    f.write(im)


