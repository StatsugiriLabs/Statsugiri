# Deployment Checklist

## Data Pipeline Source Checklist

-   [ ] Verify formats in `constants` is updated

## Data Pipeline Deployment Checklist

-   [ ] Build Docker image using `push_data_extractor_image.sh`
-   [ ] Ensure an ECR repository is created for the Docker image
-   [ ] Deploy the new Docker image on AWS Lambda
-   [ ] Ensure environment variables `MONGOURI` and `ENV` (`DEV`, `QA`, `PROD`) are set

## Server Source Checklist

-   [ ] Verify formats in `constants` is updated

## Miscellaneous Tips

-   To SSH into a container, use `docker exec -it [CONTAINER] sh`
