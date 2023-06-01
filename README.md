# Documenation

## To start

### using your device
1. 
```bash
python3.10 -m pip install -r requirements.txt
```
2. then istall RabbitMQ


3. In new window start brocker
```bash
docket-compose up -d
```
4. set next env var for api and consumer
```yaml
 environment:
     - rabbit_mq_host=127.0.0.1
     - rabbit_mq_port=5672
     - rabbit_mq_username=admin
     - rabbit_mq_password=admin
     - storage_path=./storage/
```

4. In new window start consumer
```bash
python3.10 -c 'from utils import services; services.SoftceryQueue(produce_message=False).start_consuming_message()
```

5. Start api in the new window
```bash
python3.10 -m uvicorn main:app --host 0.0.0.0 --port 80
```

### Test

```bash
python3.10 test.py
```

## API Documentation


<details>
<summary>Endpoint: Add Image to Queue /add_image</summary>

Adds an image file to the processing queue.

***Method***: POST

Request Parameters

file (file) - The image file to be added to the queue.
Response

200 OK - The image file has been successfully added to the processing queue.


</details>


<details>
<summary>Get Image by ID /get_image</summary>

Retrieves an image from the processing queue by its ID.

***Method***: POST

Request Parameters

file_id (string) - The ID of the image to retrieve.
quality (integer, optional) - The quality of the returned image. If not provided, the default value is 100.
Response

200 OK - The image has been successfully retrieved.

400 Bad Request - The request is invalid.
Example Response:
json
```json
{
    "success": false,
    "status": 400,
    "error": "varible has incorrect value",
    "report": "Incorrect quality is given. only 25/50/75/100 value is valid",
    "message": "Incorrect quality param."
}
```
</details>