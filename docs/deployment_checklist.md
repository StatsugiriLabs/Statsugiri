# Deployment Checklist

## Data Pipeline Source Checklist

-   [ ] Verify formats in `constants` is updated

## Data Pipeline Deployment Checklist

-   [ ] Build Docker image using `push_data_extractor_image.sh`
-   [ ] Deploy the new Docker image on AWS Lambda
-   [ ] Ensure environment variables `MONGOURI` and `ENV` (`DEV`, `QA`, `PROD`) are set

## Server Source Checklist

-   [ ] Verify formats in `constants` is updated
