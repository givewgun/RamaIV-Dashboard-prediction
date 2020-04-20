1. check credentials (need verification) if cloud run requires or not

2. run this to build and push docker imaage
```
gcloud builds submit --tag gcr.io/taxi-272612/ramaivpredict
```

3.run this to deploy (or use ui in google cloud)
```
gcloud run deploy ramaivdashboard --image gcr.io/taxi-272612/ramaivpredict --platform managed --allow-unauthenticated
```