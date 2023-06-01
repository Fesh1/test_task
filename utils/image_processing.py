import cv2
import os




def downscale_images(
        image_path: str,
        resized_image_path: str,
        persent_resice: float
    ):
    img = open_image(image_path)
    height, width = img.shape[:2]
    resized_img = cv2.resize(
                    img, 
                    (round(width*persent_resice), round(height*persent_resice)), 
                    interpolation=cv2.INTER_AREA
                    )
    save_image(resized_image_path,resized_img)


def open_image(image_path: str):
    return cv2.imread(image_path)


def create_image(file: bytes, image_path):
    with open(image_path, 'wb') as f:
        f.write(file)
    return image_path


def save_image(image_path: str, img):
    cv2.imwrite(image_path, img)


def delete_image(image_path: str):
    os.remove(image_path)