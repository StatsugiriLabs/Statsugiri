# Deployment Docs

## Server Deployment

The server is run on an AWS EC2 instance. Nginx is used as a reverse proxy for port forwarding and HTTPS, which is detailed [here](<https://www.digitalocean.com/community/tutorials/how-to-install-nginx-on-ubuntu-20-04#step-5-%E2%80%93-setting-up-server-blocks-(recommended)>) and [here](https://www.digitalocean.com/community/tutorials/how-to-secure-nginx-with-let-s-encrypt-on-ubuntu-20-04).

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
