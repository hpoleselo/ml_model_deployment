import os
from fastapi import FastAPI, File, UploadFile
from matplotlib import image
from pydantic import BaseModel
from keras.models import load_model
from utils.predict import predict_digit
from utils.gcs_interface import read_from_gcs, write_to_gcs

# Loading the model
model = load_model('weights/best.h5')

app = FastAPI()

# TODO: Redirect in FastAPI to accomplish image upload and prediction in one shot
# TODO: Support Multi File Upload

@app.get('/')
async def main():
    return "Welcome to the API Demo!"

@app.get('/predicted_image_gcs')
async def predict(img_name : str):
    file_location = read_from_gcs(img_name)
    pred = predict_digit(model, file_location)

    return {"predicted_digit": pred}

@app.post('/upload_to_gcs/')
async def create_upload_file(file : UploadFile = File(default=None)):
    #print(file.file.read())
    #print(type(file.file.read()))
    #print(type(file.read()))
    content = await file.read()
    #! testar
    #print(type(content))
    blob_id = write_to_gcs(file.filename, content)
    return {"blob_id": blob_id, "img_name": file.filename}


# ! Deprecated for now, we'll be using in-memory storage to save the image

"""@app.post('/upload/')
async def create_upload_file(file : UploadFile = File(default=None)):
    file_location = f'images/{file.filename}'
    if not os.path.exists('images/'):
        os.makedirs('images/')
    with open(file_location, "wb+") as f:
        f.write(file.file.read())
    return {"info": f'file {file.filename} saved at {file_location}'}

@app.get('/predicted_image')
async def predict(img_name : str):

    # Create folder to save images
    if not os.path.exists('results/'):
        os.makedirs('results/')

    pred = predict_digit(model, img_name)

    return {img_name: "pred"}
    """