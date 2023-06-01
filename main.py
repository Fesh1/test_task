from fastapi import FastAPI, UploadFile, File
from utils.services import SoftceryQueue
import logging
import uvicorn
from typing import Optional
from starlette.responses import JSONResponse

app = FastAPI()
logging.info('Start image processing api!')




@app.post('/add_image')
def add_image_to_queue(filename: str,file: UploadFile = File(...)):
    return SoftceryQueue(produce_message=True).add_image_to_processing_queue(filename=filename, file=file.file.read())


@app.post('/get_image')
def get_image_by_id(file_id: str, quality: Optional[int] = 100):
    if quality not in [25, 50, 75, 100]:
        return JSONResponse(status_code=400, content={
                "success": False,
                "status": 400,
                "error": "varible has incorrect value",
                "report": "Incorrect quality is given. only 25/50/75/100 value is valid",
                "message": "Incorrect quality param."
            })
    return SoftceryQueue(produce_message=False).return_image(file_id, quality/100)



if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1:15672", port=8008)