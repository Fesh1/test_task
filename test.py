from fastapi.testclient import TestClient
import requests
import os
import time

def test_post_image():
    file_path = './test/images/2.jpeg'
    r = requests.post('http://0.0.0.0:80/add_image', 
        files={"file": (os.path.basename(file_path), open(file_path, "rb"), "image/jpeg")},params={'filename': os.path.basename(file_path)}
       )
    return r.content.decode('utf-8')[1:][:-1] # :)))

def test_get_image(file_id):
    r = requests.post('http://0.0.0.0:80/get_image',
        params={'file_id': file_id,'quality': 75}
       )
    print(r.content)


f_id = test_post_image()
time.sleep(1)
test_get_image(f_id)