# Predict Digit API

Deployment of a simple digit predictor ML model using GCP Cloud Run and exposing it via an FastAPI.

## Running the API locally

Install the required packages:

`$ pip install -r requirements.txt`

Make sure to be in the root folder of the project and:

` $ uvicorn app.main:app --reload `

## Deploying to Cloud

Authenticate to Application Default Credentials locally:

`$ gcloud auth login --update-adc`

Get your project id from GCP:

`$ gcloud projects list`

Get your project ID and use it to build the container using Cloud Build (can be done locally and pushed to Google Container Registry [GCR] instead):

` $ gcloud builds submit --tag gcr.io/PROJECT_ID/digit_predictor`

Deploy image from GCR to Cloud Run:

`$ gcloud deploy --image gcr.io/PROJECT_ID/digit_predictor`

## Troubleshooting

While running `tensorflow-cpu=2.9.2` there was a conflict regarding protobuf version against `google-cloud-storage` protobuf's version, while GCS used a newer version of protobuf, tensorflow-cpu used an older one. The solution was found under [this issue](https://github.com/protocolbuffers/protobuf/issues/10051) in the protobuf repository.

```
ERROR: tensorflow-cpu 2.9.2 has requirement protobuf<3.20,>=3.9.2, but you'll have protobuf 4.21.5 which is incompatible.
ERROR: tensorboard 2.9.1 has requirement protobuf<3.20,>=3.9.2, but you'll have protobuf 4.21.5 which is incompatible.
```

While the solution was using Python 3.10 and by **downgrading protobuf to version 3.20.1**:

`$ pip install --no-cache-dir protobuf==3.20.1`

When piping still the conflict will be there, but when running the API it will work normally.

One important reminder is to create the virtual environment properly in the Linux environment, make sure to install:

`$ sudo apt-get install python3.10-venv`

## Resources

Useful resources consulted while developing this API:
- https://stackoverflow.com/questions/71858816/error-uploading-file-to-google-cloud-storage
- https://cloud.google.com/python/docs/reference/storage/latest/google.cloud.storage.blob.Blob
- https://github.com/protocolbuffers/protobuf/issues/10051
