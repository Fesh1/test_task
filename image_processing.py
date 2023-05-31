import cv2
import os
import io
import time




def downscale_images(image_path: str, persent_resice):
    img = open_image(image_path)
    height, width = img.shape[:2]
    resized_img = cv2.resize(img, (round(width*persent_resice),
                    round(height*persent_resice)), interpolation=cv2.INTER_AREA)
    resized_image_path = os.path.join(os.getenv('storage_path'),
                    str(persent_resice)+'-'+os.path.basename(image_path))
    save_image(resized_image_path,
            resized_img)


def open_image(image_path: str):
    return cv2.imread(image_path)


def create_image(file: io.FileIO, file_name):
    storage_path = os.getenv('storage_path')
    t = str(time.time())
    image_path = os.path.join(storage_path, t+'-'+file_name)
    try:
        contents = file.read()
        with open(image_path, 'wb') as f:
            f.write(contents)
    except Exception:
        return {"message": "There was an error uploading the file"}
    finally:
            file.close()
    return image_path, t


def save_image(image_path: str, img):
    cv2.imwrite(image_path, img)


def delete_image(image_path: str):
    os.remove(image_path)