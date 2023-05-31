import requests
import unittest
import time
import matplotlib.pyplot as plt
from unittest.mock import MagicMock
import os
import numpy as np
import cv2 

from rabbitmq_client import RabbitClient
from image_processing import open_image, delete_image, downscale_images, save_image, create_image





class RabbitClientTestCase(unittest.TestCase):
    def setUp(self):
        # Create a mock RabbitClient instance
        self.rabbit_client = RabbitClient()

    def test_singleton_instance(self):
        # Test that only one instance of RabbitClient is created
        rabbit_client_1 = RabbitClient()
        rabbit_client_2 = RabbitClient()
        self.assertIs(rabbit_client_1, rabbit_client_2)

    def test_connect(self):
        # Test the connect method
        # Mock the underlying RabbitMQ client's connect method
        self.rabbit_client.client.connect = MagicMock()
        self.rabbit_client.connect()

        # Assert that the underlying connect method is called
        self.rabbit_client.client.connect.assert_called_once()

    def test_add_item_to_queue(self):
        # Test the add_item_to_queue method
        key = "key"
        value = "value"

        # Mock the underlying RabbitMQ client's add_item_to_queue method
        self.rabbit_client.client.add_item_to_queue = MagicMock()
        self.rabbit_client.add_item_to_queue(key, value)

        # Assert that the underlying add_item_to_queue method is called with the correct arguments
        self.rabbit_client.client.add_item_to_queue.assert_called_once_with(key, value)

    def test_return_item_from_queue(self):
        # Test the return_item_from_queue method
        # Mock the underlying RabbitMQ client's return_item_from_queue method
        self.rabbit_client.client.return_item_from_queue = MagicMock()
        self.rabbit_client.return_item_from_queue()

        # Assert that the underlying return_item_from_queue method is called
        self.rabbit_client.client.return_item_from_queue.assert_called_once()



class APITestCase(unittest.TestCase):
    API_URL = "http://example.com/api"  # Replace with your API endpoint

    def test_response_time(self):
        num_requests = 10  # Number of requests to test
        response_times = []

        for _ in range(num_requests):
            start_time = time.time()
            response = requests.get(self.API_URL)
            end_time = time.time()
            response_time = end_time - start_time
            response_times.append(response_time)

        average_response_time = sum(response_times) / num_requests

        print(f"Average response time for {num_requests} requests: {average_response_time} seconds")

        # Add your assertion here
        # For example, assert that the average response time is less than a certain threshold
        self.assertLess(average_response_time, 1.0)  # Adjust the threshold as needed

        # Plotting the chart
        plt.plot(range(1, num_requests + 1), response_times)
        plt.xlabel('Number of Requests')
        plt.ylabel('Response Time (seconds)')
        plt.title('API Response Time vs Number of Requests')
        plt.show()



class ImageProcessingTestCase(unittest.TestCase):
    def set_up(self):
        self.test_images_dir = "./storage/"
        self.test_image_path =  "./test/images/9.jpeg"
        self.test_destination_path = os.path.join("./storage",os.path.basename(self.test_image_path))
    def test_open_image(self):
        self.set_up()
        # Test open_image function
        result = open_image(self.test_destination_path)
        # Assert that the result is a valid image
        self.assertIsInstance(result, np.ndarray)

    def test_save_image(self):
        self.set_up()
        result = open_image(self.test_image_path)
        # Test save_image function
        save_image(self.test_destination_path, result)

        # Assert that the image is saved successfully
        self.assertTrue(os.path.exists(self.test_destination_path))

    def test_delete_image(self):
        self.set_up()
        delete_image(self.test_destination_path)

    def test_downscale_image(self):
        self.set_up()
        downscale_images(self.test_destination_path, 0.25)


if __name__ == '__main__':
    unittest.main()

# python -m unittest test_module1 test_module2