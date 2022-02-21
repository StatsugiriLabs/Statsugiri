# Infrastructure Architecture

The infrastructure is hosted using [Amazon Web Services](https://aws.amazon.com/) (AWS) and their various cloud computing services.

## Application Infrastructure

#### Architecture Overview Diagram

![High Level Application Architecture Diagram](images/svg/App_Architecture.svg)

### Backend / Storage Architecture

The [Go](https://go.dev/) backend is responsible for serving the aggregation stats API. [Nginx](https://www.nginx.com/) sits at the front of the server to provide port forwarding (ie. mapping to Port 80/443) and providing HTTPS. Certificates are generated using [Certbot](https://certbot.eff.org/). Both of these are hosted on an [AWS EC2](https://aws.amazon.com/ec2/) instance.

The MongoDB storage is hosted using [MongoDB Atlas](https://www.mongodb.com/atlas/database). The Go server will access the database if the result has not been recorded in the in-memory cache. Otherwise, it will retrieve the value in the cache to minimize number of database reads.

## Data Pipeline Infrastructure

### Invoking Lambda Functions

The payload for invoking the private lambda function contains a parameter specifying the format to extract information from.

```
{"format": "gen8vgc2022"}
```

The lambda function is scheduled with a cron job trigger using AWS EventBridge. The cron expression used is `0 9 * * ? *`, meaning it will trigger at 09:00:00 GMT everyday.
