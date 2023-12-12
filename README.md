# README (please)

## How to publish ?
```gcloud builds submit --tag gcr.io/ace-charter-310713/ingredient```

## How to deploy ?
```gcloud run deploy ingredient --image gcr.io/ace-charter-310713/ingredient --platform managed --region=europe-west1 --allow-unauthenticated --cpu-boost```

## How to update revision
```
gcloud run deploy ingredient \
--image=gcr.io/ace-charter-310713/ingredient \
--region=europe-west1 \
--project=ace-charter-310713 \
 && gcloud run services update-traffic ingredient --to-latest
```

Cette solution est transitoire. 