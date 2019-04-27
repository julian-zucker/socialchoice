#!/bin/bash

gcloud functions deploy $1 \
  --source . \
  --entry-point $1 \
  --project sharkhacks \
  --runtime python37 \
  --trigger-http \
  --memory 128MB \
  --region us-east1 \
  --env-vars-file .env.yaml

# --source  https://source.developers.google.com/projects/sharkhacks/repos/github_julian-zucker_socialchoice/moveable-aliases/master/paths/src/ \
