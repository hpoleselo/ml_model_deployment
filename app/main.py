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

@app.get('/')
async def main():
    return "Welcome to the API Demo!"

@app.post('/upload/')
async def create_upload_file(file : UploadFile = File(default=None)):
    file_location = f'images/{file.filename}'
    if not os.path.exists('images/'):
        os.makedirs('images/')
    with open(file_location, "wb+") as f:
        f.write(file.file.read())
    return {"info": f'file {file.filename} saved at {file_location}'}

@app.post('/upload_to_gcs/')
async def create_upload_file(file : UploadFile = File(default=None)):
    bucket_id = write_to_gcs(file.filename)
    return {"file_location": bucket_id}

@app.get('/predicted_image')
async def predict(img_name : str):

    # Create folder to save images
    if not os.path.exists('results/'):
        os.makedirs('results/')

    pred = predict_digit(model, img_name)

    return {img_name: "pred"}
